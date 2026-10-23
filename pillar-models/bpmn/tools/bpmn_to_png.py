"""Render BPMN 2.0 files (with diagram information) to SVG and PNG.

usage: python bpmn_to_png.py <input folder> <output folder> [--scale 2]

Reads the diagram information (shape bounds, waypoints, label bounds) exactly as
drawn, so the picture matches what a BPMN modeler shows. Output is a PNG per
file for document management, plus a check that every modeled element was drawn.
Needs Microsoft Edge for the PNG step.
"""
import glob
import math
import os
import subprocess
import shutil
import sys
import tempfile
import time
import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape

B = '{http://www.omg.org/spec/BPMN/20100524/MODEL}'
DI = '{http://www.omg.org/spec/BPMN/20100524/DI}'
DC = '{http://www.omg.org/spec/DD/20100524/DC}'
DD = '{http://www.omg.org/spec/DD/20100524/DI}'
FONT = 'Helvetica, Arial, sans-serif'
INK, MUTED = '#0F172A', '#475569'
EDGE = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
FS = 13  # 10 pt
LFS, LSTEP = 12, 14  # event and gateway labels: the diagram files reserve 14 px a line


def wrap(text, width, size=FS, bold=False):
    cw = size * (0.56 if bold else 0.5)
    lines, cur = [], ''
    for w in text.split():
        t = (cur + ' ' + w).strip()
        if cur and len(t) * cw > width:
            lines.append(cur)
            cur = w
        else:
            cur = t
    if cur:
        lines.append(cur)
    return lines or ['']


class Svg:
    def __init__(self):
        self.parts = []
        self.drawn = {}

    def add(self, s):
        self.parts.append(s)

    def text(self, x, y, s, size=FS, bold=False, anchor='middle', fill=INK, rotate=None):
        a = ' transform="rotate(%s %s %s)"' % (rotate, x, y) if rotate is not None else ''
        self.add('<text x="%s" y="%s" font-family="%s" font-size="%s" fill="%s" text-anchor="%s"%s%s>%s</text>' % (
            f(x), f(y), FONT, size, fill, anchor, ' font-weight="bold"' if bold else '', a, escape(s)))

    def block(self, cx, top, lines, size=FS, bold=False, step=None, fill=INK):
        step = step or size * 1.2
        for i, ln in enumerate(lines):
            self.text(cx, top + size * 0.95 + i * step, ln, size, bold, 'middle', fill)


def f(v):
    return ('%.2f' % v).rstrip('0').rstrip('.')


def gear(svg, x, y):
    cx, cy = x + 14, y + 14
    for k in range(8):
        a = k * math.pi / 4
        svg.add('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width="2.4"/>' % (
            f(cx + 5.5 * math.cos(a)), f(cy + 5.5 * math.sin(a)), f(cx + 8 * math.cos(a)), f(cy + 8 * math.sin(a)), INK))
    svg.add('<circle cx="%s" cy="%s" r="6" fill="#FFFFFF" stroke="%s" stroke-width="1.4"/>' % (f(cx), f(cy), INK))
    svg.add('<circle cx="%s" cy="%s" r="2.3" fill="#FFFFFF" stroke="%s" stroke-width="1.2"/>' % (f(cx), f(cy), INK))


def envelope(svg, cx, cy, filled):
    fill, stroke = (INK, '#FFFFFF') if filled else ('#FFFFFF', INK)
    svg.add('<rect x="%s" y="%s" width="20" height="14" fill="%s" stroke="%s" stroke-width="1.3"/>' % (f(cx - 10), f(cy - 7), fill, INK if not filled else INK))
    svg.add('<polyline points="%s,%s %s,%s %s,%s" fill="none" stroke="%s" stroke-width="1.3"/>' % (
        f(cx - 10), f(cy - 7), f(cx), f(cy + 1), f(cx + 10), f(cy - 7), stroke))


def arrow_head(svg, tip, frm, color, open_head=False):
    dx, dy = tip[0] - frm[0], tip[1] - frm[1]
    n = math.hypot(dx, dy) or 1
    ux, uy = dx / n, dy / n
    bx, by = tip[0] - ux * 10, tip[1] - uy * 10
    px, py = -uy * 4.5, ux * 4.5
    pts = '%s,%s %s,%s %s,%s' % (f(tip[0]), f(tip[1]), f(bx + px), f(by + py), f(bx - px), f(by - py))
    if open_head:
        svg.add('<polyline points="%s,%s %s,%s %s,%s" fill="none" stroke="%s" stroke-width="1.5"/>' % (
            f(bx + px), f(by + py), f(tip[0]), f(tip[1]), f(bx - px), f(by - py), color))
    else:
        svg.add('<polygon points="%s" fill="%s" stroke="%s" stroke-width="1"/>' % (pts, color, color))


def render(path):
    root = ET.parse(path).getroot()
    model = {}
    for el in root.iter():
        if el.get('id'):
            model[el.get('id')] = el
    plane = root.find('.//' + DI + 'BPMNPlane')
    shapes, edges = [], []
    for s in plane.findall(DI + 'BPMNShape'):
        b = s.find(DC + 'Bounds')
        lab = s.find(DI + 'BPMNLabel/' + DC + 'Bounds')
        shapes.append(dict(el=model[s.get('bpmnElement')], x=float(b.get('x')), y=float(b.get('y')), w=float(b.get('width')), h=float(b.get('height')),
                           lab=None if lab is None else tuple(float(lab.get(k)) for k in ('x', 'y', 'width', 'height')),
                           expanded=s.get('isExpanded'), marker=s.get('isMarkerVisible')))
    for e in plane.findall(DI + 'BPMNEdge'):
        pts = [(float(w.get('x')), float(w.get('y'))) for w in e.findall(DD + 'waypoint')]
        lab = e.find(DI + 'BPMNLabel/' + DC + 'Bounds')
        edges.append(dict(el=model[e.get('bpmnElement')], pts=pts, lab=None if lab is None else tuple(float(lab.get(k)) for k in ('x', 'y', 'width', 'height'))))
    # extent
    xs, ys = [], []
    for s in shapes:
        xs += [s['x'], s['x'] + s['w']]
        ys += [s['y'], s['y'] + s['h']]
        if s['lab']:
            xs += [s['lab'][0], s['lab'][0] + s['lab'][2]]
            ys += [s['lab'][1], s['lab'][1] + s['lab'][3]]
    for e in edges:
        xs += [p[0] for p in e['pts']]
        ys += [p[1] for p in e['pts']]
        if e['lab']:
            xs += [e['lab'][0], e['lab'][0] + e['lab'][2]]
            ys += [e['lab'][1], e['lab'][1] + e['lab'][3]]
    m = 28
    ox, oy = min(xs) - m, min(ys) - m
    W, H = math.ceil(max(xs) + m - ox), math.ceil(max(ys) + m - oy)
    svg = Svg()
    T = lambda x, y: (x - ox, y - oy)

    def local(el):
        return el.tag.split('}')[-1]

    # containers first
    pools = [s for s in shapes if local(s['el']) == 'participant']
    lanes = [s for s in shapes if local(s['el']) == 'lane']
    for s in pools:
        x, y = T(s['x'], s['y'])
        svg.add('<rect x="%s" y="%s" width="%s" height="%s" fill="#FFFFFF" stroke="%s" stroke-width="1.5"/>' % (f(x), f(y), f(s['w']), f(s['h']), INK))
        svg.add('<rect x="%s" y="%s" width="40" height="%s" fill="#E2E8F0" stroke="%s" stroke-width="1.5"/>' % (f(x), f(y), f(s['h']), INK))
        name = s['el'].get('name')
        size = 15
        lines = wrap(name, s['h'] - 20, size, True)
        for i, ln in enumerate(lines):
            cx = x + 20 + (i - (len(lines) - 1) / 2) * size * 1.2
            svg.text(cx + size * 0.35, y + s['h'] / 2, ln, size, True, 'middle', INK, -90)
        svg.drawn[s['el'].get('id')] = 1
    for s in lanes:
        x, y = T(s['x'], s['y'])
        svg.add('<rect x="%s" y="%s" width="%s" height="%s" fill="#FFFFFF" stroke="%s" stroke-width="1.2"/>' % (f(x), f(y), f(s['w']), f(s['h']), INK))
        svg.add('<rect x="%s" y="%s" width="36" height="%s" fill="#F1F5F9" stroke="%s" stroke-width="1.2"/>' % (f(x), f(y), f(s['h']), INK))
        name = s['el'].get('name')
        for size in (13, 12, 11, 10):
            lines = wrap(name, s['h'] - 16, size, True)
            if len(lines) * size * 1.2 <= 32:
                break
        for i, ln in enumerate(lines):
            cx = x + 18 + (i - (len(lines) - 1) / 2) * size * 1.2
            svg.text(cx + size * 0.35, y + s['h'] / 2, ln, size, True, 'middle', INK, -90)
        svg.drawn[s['el'].get('id')] = 1

    # edges
    for e in edges:
        pts = [T(*p) for p in e['pts']]
        kind = local(e['el'])
        assoc = kind == 'association'
        d = 'M' + ' L'.join('%s,%s' % (f(p[0]), f(p[1])) for p in pts)
        base = list(pts)
        if not assoc:
            # stop the line at the arrow base
            dx, dy = pts[-1][0] - pts[-2][0], pts[-1][1] - pts[-2][1]
            n = math.hypot(dx, dy) or 1
            base[-1] = (pts[-1][0] - dx / n * 9, pts[-1][1] - dy / n * 9)
            d = 'M' + ' L'.join('%s,%s' % (f(p[0]), f(p[1])) for p in base)
        svg.add('<path d="%s" fill="none" stroke="%s" stroke-width="1.5" stroke-linejoin="round"%s/>' % (d, INK if not assoc else MUTED, ' stroke-dasharray="2,3"' if assoc else ''))
        arrow_head(svg, pts[-1], pts[-2], INK if not assoc else MUTED, open_head=assoc)
        if e['lab'] and e['el'].get('name'):
            lx, ly = T(e['lab'][0], e['lab'][1])
            svg.text(lx + e['lab'][2] / 2, ly + 11, e['el'].get('name'), FS, False, 'middle', INK)
        svg.drawn[e['el'].get('id')] = 1

    # shapes
    for s in shapes:
        el, kind = s['el'], local(s['el'])
        if kind in ('participant', 'lane'):
            continue
        x, y = T(s['x'], s['y'])
        w, h = s['w'], s['h']
        cx, cy = x + w / 2, y + h / 2
        name = el.get('name') or ''
        msg = el.find(B + 'messageEventDefinition') is not None
        if kind in ('task', 'serviceTask', 'subProcess'):
            sw = 1.8 if kind == 'subProcess' else 1.5
            svg.add('<rect x="%s" y="%s" width="%s" height="%s" rx="10" ry="10" fill="#FFFFFF" stroke="%s" stroke-width="%s"/>' % (f(x), f(y), f(w), f(h), INK, sw))
            pad = 36 if kind == 'serviceTask' else 16
            lines = wrap(name, w - pad)
            area = h - (22 if kind == 'subProcess' else 0)
            top = y + (area - len(lines) * FS * 1.2) / 2
            svg.block(cx, top, lines)
            if kind == 'serviceTask':
                gear(svg, x + 4, y + 4)
            if kind == 'subProcess':
                svg.add('<rect x="%s" y="%s" width="14" height="14" fill="#FFFFFF" stroke="%s" stroke-width="1.3"/>' % (f(cx - 7), f(y + h - 20), INK))
                svg.add('<path d="M%s,%s L%s,%s M%s,%s L%s,%s" stroke="%s" stroke-width="1.5"/>' % (f(cx - 4), f(y + h - 13), f(cx + 4), f(y + h - 13), f(cx), f(y + h - 17), f(cx), f(y + h - 9), INK))
        elif kind in ('startEvent', 'endEvent', 'intermediateCatchEvent'):
            r = w / 2
            if kind == 'endEvent':
                svg.add('<circle cx="%s" cy="%s" r="%s" fill="#FFFFFF" stroke="%s" stroke-width="4.5"/>' % (f(cx), f(cy), f(r - 2), INK))
            else:
                svg.add('<circle cx="%s" cy="%s" r="%s" fill="#FFFFFF" stroke="%s" stroke-width="1.5"/>' % (f(cx), f(cy), f(r), INK))
                if kind == 'intermediateCatchEvent':
                    svg.add('<circle cx="%s" cy="%s" r="%s" fill="none" stroke="%s" stroke-width="1.5"/>' % (f(cx), f(cy), f(r - 5), INK))
            if msg:
                envelope(svg, cx, cy, filled=(kind == 'endEvent'))
            lb = s['lab']
            if lb and name:
                lx, ly = T(lb[0], lb[1])
                lines = wrap(name, lb[2] - 4, LFS)
                above = lb[1] + lb[3] <= s['y'] + 1
                top = ly + lb[3] - len(lines) * LSTEP if above else ly
                svg.block(lx + lb[2] / 2, top, lines, LFS, step=LSTEP)
        elif kind in ('exclusiveGateway', 'parallelGateway'):
            svg.add('<polygon points="%s,%s %s,%s %s,%s %s,%s" fill="#FFFFFF" stroke="%s" stroke-width="1.5"/>' % (
                f(cx), f(y), f(x + w), f(cy), f(cx), f(y + h), f(x), f(cy), INK))
            if kind == 'exclusiveGateway':
                svg.add('<path d="M%s,%s L%s,%s M%s,%s L%s,%s" stroke="%s" stroke-width="4"/>' % (f(cx - 10), f(cy - 10), f(cx + 10), f(cy + 10), f(cx + 10), f(cy - 10), f(cx - 10), f(cy + 10), INK))
            else:
                svg.add('<path d="M%s,%s L%s,%s M%s,%s L%s,%s" stroke="%s" stroke-width="4"/>' % (f(cx - 12), f(cy), f(cx + 12), f(cy), f(cx), f(cy - 12), f(cx), f(cy + 12), INK))
            lb = s['lab']
            if lb and name:
                lx, ly = T(lb[0], lb[1])
                lines = wrap(name, lb[2] - 4, LFS)
                above = lb[1] + lb[3] <= s['y'] + 1
                svg.block(lx + lb[2] / 2, ly + lb[3] - len(lines) * LSTEP if above else ly, lines, LFS, step=LSTEP)
        else:
            raise ValueError('unsupported element %s' % kind)
        svg.drawn[el.get('id')] = 1

    # coverage: every diagram element drawn, every named model element appears as text
    named = [el for el in model.values() if el.get('name') and local(el) not in ('definitions', 'collaboration', 'process', 'parallelGateway')]
    body = ''.join(svg.parts)
    missing = [el.get('id') for el in named if escape(el.get('name')).split(' ')[0] not in body]
    undrawn = [i for i, el in model.items() if local(el) in ('task', 'serviceTask', 'subProcess', 'startEvent', 'endEvent', 'intermediateCatchEvent',
                                                                'exclusiveGateway', 'parallelGateway', 'sequenceFlow', 'association', 'lane', 'participant') and i not in svg.drawn]
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">' % (W, H, W, H),
           '<rect width="%d" height="%d" fill="#FFFFFF"/>' % (W, H), body, '</svg>']
    return '\n'.join(out), W, H, missing, undrawn


def to_png(svg_path, png_path, W, H, scale):
    uri = 'file:///' + svg_path.replace('\\', '/')
    if os.path.exists(png_path):
        os.remove(png_path)
    subprocess.run([EDGE, '--headless=new', '--disable-gpu', '--hide-scrollbars', '--force-device-scale-factor=%s' % scale,
                    '--window-size=%d,%d' % (W, H), '--screenshot=' + png_path, uri], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=120)
    for _ in range(60):
        if os.path.exists(png_path) and os.path.getsize(png_path) > 0:
            return True
        time.sleep(1)
    return False


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    scale = 2
    if '--scale' in sys.argv:
        scale = float(sys.argv[sys.argv.index('--scale') + 1])
        args = [a for a in args if a != str(sys.argv[sys.argv.index('--scale') + 1])]
    src, dst = os.path.abspath(args[0]), os.path.abspath(args[1])
    os.makedirs(dst, exist_ok=True)
    bad = 0
    tmp = tempfile.mkdtemp(prefix='bpmn_svg_')
    for p in sorted(glob.glob(os.path.join(src, '*.bpmn'))):
        stem = os.path.splitext(os.path.basename(p))[0]
        svg, W, H, missing, undrawn = render(p)
        sp = os.path.join(tmp, stem + '.svg')
        open(sp, 'w', encoding='utf-8').write(svg)
        ok = to_png(sp, os.path.join(dst, stem + '.png'), W, H, scale)
        flag = '' if ok and not missing and not undrawn else '  CHECK missing=%s undrawn=%s png=%s' % (missing, undrawn, ok)
        bad += bool(flag)
        print('%-62s %4dx%-4d%s' % (stem, W, H, flag))
    shutil.rmtree(tmp, ignore_errors=True)
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
