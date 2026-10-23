"""Build the L0 value chain map (SVG, draw.io, PNG) from l0-register.json.

Every view is generated from one layout model, so the SVG and the draw.io file
cannot disagree. Run validate_l0.py afterwards.
"""
import json
import os
import subprocess
import sys
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
REG = json.load(open(os.path.join(HERE, 'l0-register.json'), encoding='utf-8'))
STEM = 'L0_value-chain-map'
FONT = 'Helvetica, Arial, sans-serif'
W, H = 1920, 1080

INK, MUTED, FAINT = '#0F172A', '#475569', '#64748B'
VALUE = ('#DCFCE7', '#22C55E', '#166534')
FOUND = ('#E2E8F0', '#94A3B8', '#334155')
GOVERN = ('#F8FAFC', '#64748B', '#334155')
CARD_BORDER, CELL_BORDER = '#94A3B8', '#CBD5E1'
RIBBON = '#F1F5F9'
HEAD = 9


def tw(text, size, bold=False):
    """Conservative width estimate for Helvetica."""
    return len(text) * size * (0.62 if bold else 0.56)


def wrap(text, width, size, bold=False):
    lines, cur = [], ''
    for word in text.split():
        trial = (cur + ' ' + word).strip()
        if cur and tw(trial, size, bold) > width:
            lines.append(cur)
            cur = word
        else:
            cur = trial
    if cur:
        lines.append(cur)
    return lines


EL = []  # model elements in z-order


def rect(i, x, y, w, h, fill, stroke, sw=1.2, rx=8, dash=False, layer='diagram'):
    EL.append(dict(t='rect', id=i, x=x, y=y, w=w, h=h, fill=fill, stroke=stroke, sw=sw, rx=rx, dash=dash, layer=layer))


def ellipse(i, cx, cy, r, fill, stroke, sw=1.5, dash=False, layer='diagram', group=None):
    EL.append(dict(t='ellipse', id=i, x=cx - r, y=cy - r, w=2 * r, h=2 * r, fill=fill, stroke=stroke, sw=sw, dash=dash, layer=layer, group=group))


def text(i, x, y, w, s, size, color, bold=False, anchor='start', layer='diagram', group=None):
    EL.append(dict(t='text', id=i, x=x, y=y, w=w, h=round(size * 1.3), s=s, size=size, color=color, bold=bold, anchor=anchor, layer=layer, group=group))


def edge(i, pts, color, sw, dash, end, start, src, tgt, layer='diagram'):
    EL.append(dict(t='edge', id=i, pts=pts, color=color, sw=sw, dash=dash, end=end, start=start, src=src, tgt=tgt, layer=layer))


def lines_block(prefix, x, y, w, lines, size, color, bold=False, anchor='start', step=None, layer='diagram'):
    step = step or round(size * 1.3)
    for n, ln in enumerate(lines):
        text('%s_%d' % (prefix, n), x, y + n * step, w, ln, size, color, bold, anchor, layer)


# ------------------------------------------------------------------ layout
P = {p['id']: p for p in REG['pillars']}
F = {f['id']: f for f in REG['flows']}
BX = {'p1': 300, 'p2': 700, 'p3': 1100, 'p4': 1500}
BY, BW, BH = 360, 290, 180
CX = {k: v + BW // 2 for k, v in BX.items()}
CY = BY + BH // 2
B6Y, B5Y, BANDH = 112, 736, 84
T6Y, T5Y, TAGH, TAGW = 232, 640, 60, 270

rect('bg', 0, 0, W, H, '#FFFFFF', '#FFFFFF', 0, 0)

# title block
text('title', 32, 36, 1000, REG['title'], 28, INK, True)
text('subtitle', 32, 76, 1856, REG['headline'], 14, MUTED)

# bands
for pid, by, colors in (('p6', B6Y, GOVERN), ('p5', B5Y, FOUND)):
    p = P[pid]
    rect('band_' + pid, 32, by, 1856, BANDH, colors[0], colors[1], 1.5, 14)
    text('band_%s_name' % pid, 56, by + 10, 900, '%d %s' % (p['num'], p['name'].upper()), 15, colors[2], True)
    text('band_%s_role' % pid, 56, by + 32, 1780, p['role'], 12, colors[2])
    areas = ' · '.join('%s %s' % (a, n) for a, n in p['areas'])
    text('band_%s_areas' % pid, 56, by + 54, 1780, areas, 11, MUTED)

# pillar boxes
for pid in ('p1', 'p2', 'p3', 'p4'):
    p = P[pid]
    x = BX[pid]
    rect('box_' + pid, x, BY, BW, BH, VALUE[0], VALUE[1], 1.5, 12)
    tl = wrap('%d %s' % (p['num'], p['name']), BW - 28, 15, True)
    lines_block('box_%s_name' % pid, x + 14, BY + 14, BW - 28, tl, 15, VALUE[2], True, step=20)
    lines_block('box_%s_area' % pid, x + 14, BY + 64, BW - 28, ['%s %s' % (a, n) for a, n in p['areas']], 11, INK, step=15)
    if p.get('note'):
        text('box_%s_note' % pid, x + 14, BY + BH - 30, BW - 28, p['note'], 11, VALUE[2], True)

# ---- flows
def tag(fid, cx, ty, label, confirm=False):
    x = cx - TAGW // 2
    rect('tag_' + fid, x, ty, TAGW, TAGH, '#FFFFFF', CARD_BORDER if not confirm else FAINT, 1.2, 8, dash=confirm)
    if confirm:
        ellipse('ring_' + fid, x + 26, ty + TAGH // 2, 11, '#FFFFFF', FAINT, 1.5, True, 'status', 'status_' + fid)
        text('ringq_' + fid, x + 26 - 8, ty + TAGH // 2 - 9, 16, '?', 13, FAINT, True, 'middle', 'status', 'status_' + fid)
        lines = wrap(label, TAGW - 66, 11.5)
        lx, lw = x + 48, TAGW - 58
        anchor = 'start'
        tx = lx
    else:
        lines = wrap(label, TAGW - 24, 11.5)
        lx, lw, anchor, tx = x + 12, TAGW - 24, 'middle', x + 12
    n = len(lines)
    y0 = ty + (TAGH - n * 15) // 2
    lines_block('tag_%s_t' % fid, tx, y0, lw, lines, 11.5, FAINT if confirm else INK, False, anchor, step=15)
    return n


def head_flag(f):
    return bool(f.get('bidirectional'))


for f in REG['flows']:
    fid = f['id']
    t = f['type']
    if fid.startswith('g_') or fid.startswith('s_'):
        tgt = f['to'] if fid.startswith('g_') else f['to']
        cx = CX[tgt]
        if fid.startswith('g_'):
            pts = [(cx, B6Y + BANDH), (cx, BY)]
            src, dst = 'band_p6', 'box_' + tgt
            ty = T6Y
        else:
            pts = [(cx, B5Y), (cx, BY + BH)]
            src, dst = 'band_p5', 'box_' + tgt
            ty = T5Y
        confirm = f.get('status') == 'to_confirm'
        edge('flow_' + fid, pts, FAINT if confirm else MUTED, 1.5, confirm, not confirm, head_flag(f), src, dst)
for f in REG['flows']:
    fid = f['id']
    if fid.startswith('g_') or fid.startswith('s_'):
        cx = CX[f['to']]
        tag(fid, cx, T6Y if fid.startswith('g_') else T5Y, f['label'], f.get('status') == 'to_confirm')

# left card: Pillar 6 <-> Pillar 5
f = F['x_p6_p5']
LX = 130
edge('flow_x_p6_p5', [(LX, B6Y + BANDH), (LX, B5Y)], MUTED, 1.5, False, True, True, 'band_p6', 'band_p5')
cl = wrap(f['label'], 134, 11.5)
ch = len(cl) * 15 + 22
cy0 = (B6Y + BANDH + B5Y) // 2 - ch // 2
rect('tag_x_p6_p5', LX - 78, cy0, 156, ch, '#FFFFFF', CARD_BORDER, 1.2, 8)
lines_block('tag_x_p6_p5_t', LX - 67, cy0 + 11, 134, cl, 11.5, INK, False, 'middle', step=15)

# chain arrows
GAP = (BX['p1'] + BW, BX['p2'])
edge('flow_f_p1_p2', [(BX['p1'] + BW, CY), (BX['p2'], CY)], MUTED, 1.5, True, True, False, 'box_p1', 'box_p2')
gcx = (BX['p1'] + BW + BX['p2']) // 2
text('lbl_f_p1_p2', gcx - 55, CY - 22, 110, F['f_p1_p2']['label'], 11, MUTED, False, 'middle')
for fid, a, b in (('f_p2_p3', 'p2', 'p3'), ('f_p3_p4', 'p3', 'p4')):
    x1, x2 = BX[a] + BW, BX[b]
    edge('flow_' + fid, [(x1, CY), (x2, CY)], INK, 2, False, True, False, 'box_' + a, 'box_' + b)
    c = next(c for c in REG['ctps'] if c['flow'] == fid)
    mx = (x1 + x2) // 2
    rect('pill_' + c['id'], mx - 28, CY - 11, 56, 22, '#FFFFFF', INK, 1.8, 11)
    text('pill_%s_t' % c['id'], mx - 28, CY - 7, 56, c['label'], 11, INK, True, 'middle')
    text('detail_' + c['id'], mx - 50, CY + 16, 100, c['detail'], 11, MUTED, False, 'middle')
# exit arrow
c = next(c for c in REG['ctps'] if c['flow'] == 'f_p4_out')
x1, x2 = BX['p4'] + BW, 1872
edge('flow_f_p4_out', [(x1, CY), (x2, CY)], INK, 2, False, True, False, 'box_p4', None)
mx = (x1 + x2) // 2
rect('pill_' + c['id'], mx - 28, CY - 11, 56, 22, '#FFFFFF', INK, 1.8, 11)
text('pill_%s_t' % c['id'], mx - 28, CY - 7, 56, c['label'], 11, INK, True, 'middle')
lines_block('detail_' + c['id'], mx - 48, CY + 16, 96, wrap(c['detail'], 96, 11), 11, MUTED, False, 'middle', step=14)

# information arcs
ARC_TOP = BY - 34
arcs = [
    ('f_p2_p1', [(BX['p2'] + 60, BY), (BX['p2'] + 60, ARC_TOP), (BX['p1'] + BW - 60, ARC_TOP), (BX['p1'] + BW - 60, BY)], 'box_p2', 'box_p1', 'above'),
    ('f_p4_p3', [(BX['p4'] + 60, BY), (BX['p4'] + 60, ARC_TOP), (BX['p3'] + BW - 60, ARC_TOP), (BX['p3'] + BW - 60, BY)], 'box_p4', 'box_p3', 'above'),
    ('f_p3_p1', [(BX['p3'] + 60, BY + BH), (BX['p3'] + 60, BY + BH + 30), (BX['p1'] + BW - 60, BY + BH + 30), (BX['p1'] + BW - 60, BY + BH)], 'box_p3', 'box_p1', 'above'),
    ('f_p4_p1', [(BX['p4'] + 60, BY + BH), (BX['p4'] + 60, BY + BH + 60), (BX['p1'] + BW - 90, BY + BH + 60), (BX['p1'] + BW - 90, BY + BH)], 'box_p4', 'box_p1', 'above'),
]
for fid, pts, s, d, _ in arcs:
    edge('flow_' + fid, pts, MUTED, 1.5, True, True, False, s, d)
    lab = F[fid]['label']
    lw = round(tw(lab, 11)) + 8
    ly = pts[1][1] - 20
    x0, x1 = min(p[0] for p in pts), max(p[0] for p in pts)
    if fid == 'f_p3_p1':
        lcx = 1000
    elif fid == 'f_p4_p1':
        lcx = 1400
    else:
        lcx = (x0 + x1) // 2
    text('lbl_' + fid, lcx - lw // 2, ly, lw, lab, 11, MUTED, False, 'middle')

# join-key strip
SY = 860
rect('keys_card', 32, SY, 1856, 84, '#FFFFFF', CARD_BORDER, 1.2, 8)
text('keys_title', 56, SY + 12, 1500, REG['join_keys_title'].upper(), 10.5, FAINT, True)
kx = 56
for n, k in enumerate(REG['join_keys']):
    label = '%s (%s)' % (k['key'], ', '.join(str(p) for p in k['pillars']))
    w = round(tw(label, 11.5)) + 22
    rect('key_%d' % n, kx, SY + 40, w, 28, '#FFFFFF', CELL_BORDER, 1.2, 8)
    text('key_%d_t' % n, kx + 11, SY + 47, w - 22, label, 11.5, INK)
    kx += w + 14
assert kx - 14 <= 1888 - 24, 'key strip too wide'

# legend ribbon (fixed layer)
rect('legend_bg', 32, 6, 1856, 22, RIBBON, CELL_BORDER, 1, 4, layer='legend')
lx = 44
text('legend_key', lx, 10, 40, 'KEY', 10.5, FAINT, True, layer='legend')
lx += 50
L = REG['legend']
edge('legend_material', [(lx, 17), (lx + 30, 17)], INK, 2, False, True, False, None, None, 'legend')
text('legend_material_t', lx + 40, 10, 150, L['material'], 11, MUTED, layer='legend')
lx += 40 + round(tw(L['material'], 11)) + 24
edge('legend_information', [(lx, 17), (lx + 30, 17)], MUTED, 1.5, True, True, False, None, None, 'legend')
text('legend_information_t', lx + 40, 10, 150, L['information'], 11, MUTED, layer='legend')
lx += 40 + round(tw(L['information'], 11)) + 24
rect('legend_tag', lx, 11, 20, 12, '#FFFFFF', CARD_BORDER, 1.2, 3, layer='legend')
text('legend_tag_t', lx + 28, 10, 220, L['tag'], 11, MUTED, layer='legend')
lx += 28 + round(tw(L['tag'], 11)) + 24
ellipse('legend_ring', lx + 7, 17, 7, '#FFFFFF', FAINT, 1.5, True, 'legend')
text('legend_to_confirm_t', lx + 20, 10, 120, L['to_confirm'], 11, MUTED, layer='legend')
lx += 20 + round(tw(L['to_confirm'], 11)) + 24
rect('legend_pill', lx, 10, 34, 14, '#FFFFFF', INK, 1.5, 7, layer='legend')
text('legend_pill_t', lx, 11, 34, 'CTP', 9, INK, True, 'middle', layer='legend')
text('legend_ctp_t', lx + 42, 10, 180, L['ctp'], 11, MUTED, layer='legend')
lx += 42 + round(tw(L['ctp'], 11))
assert lx <= 1880, 'legend too wide'

# ------------------------------------------------------------------ emitters
LAYERS = ['diagram', 'status', 'inflight', 'annotation', 'legend']


def prec(v):
    return ('%.8f' % v).rstrip('0').rstrip('.') or '0'


def fmt(v):
    return ('%g' % round(v, 2))


def endpoints(e):
    """Return line points shortened for arrowheads, and head triangles (tip first)."""
    pts = [tuple(p) for p in e['pts']]
    heads = []

    def tri(tip, frm):
        dx, dy = tip[0] - frm[0], tip[1] - frm[1]
        n = (dx * dx + dy * dy) ** 0.5
        ux, uy = dx / n, dy / n
        bx, by = tip[0] - ux * HEAD, tip[1] - uy * HEAD
        px, py = -uy * 4.5, ux * 4.5
        return [tip, (bx + px, by + py), (bx - px, by - py)], (bx, by)

    line = list(pts)
    if e['end']:
        tr, base = tri(pts[-1], pts[-2])
        heads.append(('end', tr))
        line[-1] = base
    if e['start']:
        tr, base = tri(pts[0], pts[1])
        heads.append(('start', tr))
        line[0] = base
    return line, heads


def svg_text_attrs(e):
    anchor = e['anchor']
    x = e['x'] if anchor == 'start' else (e['x'] + e['w'] / 2 if anchor == 'middle' else e['x'] + e['w'])
    return x, e['y'] + round(e['size'] * 0.95)


def build_svg():
    root = ET.Element('svg', {'xmlns': 'http://www.w3.org/2000/svg', 'width': str(W), 'height': str(H), 'viewBox': '0 0 %d %d' % (W, H)})
    ET.SubElement(root, 'title').text = REG['title']
    layer_g = {}
    for ly in LAYERS:
        layer_g[ly] = ET.SubElement(root, 'g', {'id': 'layer-' + ly})
    groups = {}

    def parent(e):
        if e.get('group'):
            if e['group'] not in groups:
                groups[e['group']] = ET.SubElement(layer_g[e['layer']], 'g', {'id': e['group']})
            return groups[e['group']]
        return layer_g[e['layer']]

    for e in EL:
        par = parent(e)
        if e['t'] == 'rect':
            a = {'id': e['id'], 'x': fmt(e['x']), 'y': fmt(e['y']), 'width': fmt(e['w']), 'height': fmt(e['h']),
                 'fill': e['fill'], 'stroke': e['stroke'], 'stroke-width': fmt(e['sw'])}
            if e['rx']:
                a['rx'] = a['ry'] = fmt(e['rx'])
            if e['dash']:
                a['stroke-dasharray'] = '6,4'
            ET.SubElement(par, 'rect', a)
        elif e['t'] == 'ellipse':
            a = {'id': e['id'], 'cx': fmt(e['x'] + e['w'] / 2), 'cy': fmt(e['y'] + e['h'] / 2), 'rx': fmt(e['w'] / 2), 'ry': fmt(e['h'] / 2),
                 'fill': e['fill'], 'stroke': e['stroke'], 'stroke-width': fmt(e['sw'])}
            if e['dash']:
                a['stroke-dasharray'] = '6,4'
            ET.SubElement(par, 'ellipse', a)
        elif e['t'] == 'text':
            x, y = svg_text_attrs(e)
            a = {'id': e['id'], 'x': fmt(x), 'y': fmt(y), 'font-family': FONT, 'font-size': fmt(e['size']),
                 'fill': e['color'], 'text-anchor': e['anchor']}
            if e['bold']:
                a['font-weight'] = 'bold'
            ET.SubElement(par, 'text', a).text = e['s']
        elif e['t'] == 'edge':
            line, heads = endpoints(e)
            g = ET.SubElement(par, 'g', {'id': e['id']})
            d = 'M' + ' L'.join('%s,%s' % (fmt(p[0]), fmt(p[1])) for p in line)
            a = {'id': e['id'] + '_line', 'd': d, 'fill': 'none', 'stroke': e['color'], 'stroke-width': fmt(e['sw']), 'stroke-linejoin': 'round'}
            if e['dash']:
                a['stroke-dasharray'] = '6,4'
            ET.SubElement(g, 'path', a)
            for which, tr in heads:
                dd = 'M%s,%s L%s,%s L%s,%s Z' % tuple(fmt(v) for p in tr for v in p)
                ET.SubElement(g, 'path', {'id': '%s_head_%s' % (e['id'], which), 'd': dd, 'fill': e['color'], 'stroke': 'none'})
    indent(root)
    return ET.ElementTree(root)


def indent(el, level=0):
    pad = '\n' + level * '  '
    if len(el):
        if not (el.text or '').strip():
            el.text = pad + '  '
        for child in el:
            indent(child, level + 1)
            if not (child.tail or '').strip():
                child.tail = pad + '  '
        child.tail = pad
    if level and not (el.tail or '').strip():
        el.tail = pad


def drawio_style(parts):
    return ';'.join(parts) + ';'


def build_drawio():
    mxfile = ET.Element('mxfile', {'host': 'app.diagrams.net', 'agent': 'build_l0.py', 'version': '24.0.0', 'type': 'device'})
    dia = ET.SubElement(mxfile, 'diagram', {'id': 'l0-value-chain-map', 'name': 'L0 Value Chain Map'})
    model = ET.SubElement(dia, 'mxGraphModel', {'dx': str(W), 'dy': str(H), 'grid': '0', 'gridSize': '10', 'guides': '1', 'tooltips': '1',
                                                  'connect': '1', 'arrows': '1', 'fold': '1', 'page': '1', 'pageScale': '1',
                                                  'pageWidth': str(W), 'pageHeight': str(H), 'math': '0', 'shadow': '0', 'background': '#FFFFFF'})
    root = ET.SubElement(model, 'root')
    ET.SubElement(root, 'mxCell', {'id': '0'})
    for ly in LAYERS:
        ET.SubElement(root, 'mxCell', {'id': 'layer-' + ly, 'value': ly, 'parent': '0'})

    shapes = {e['id']: e for e in EL if e['t'] in ('rect', 'ellipse')}

    def cell_id(e):
        return e['id']

    for e in EL:
        parent = 'layer-' + e['layer']
        if e['t'] in ('rect', 'ellipse'):
            st = ['ellipse' if e['t'] == 'ellipse' else ('rounded=1' if e['rx'] else 'rounded=0'), 'whiteSpace=wrap', 'html=0',
                  'fillColor=' + e['fill'], 'strokeColor=' + e['stroke'], 'strokeWidth=' + fmt(e['sw'])]
            if e['t'] == 'rect' and e['rx']:
                st += ['absoluteArcSize=1', 'arcSize=' + fmt(e['rx'])]
            if e['dash']:
                st += ['dashed=1', 'dashPattern=6 4']
            c = ET.SubElement(root, 'mxCell', {'id': e['id'], 'value': '', 'style': drawio_style(st), 'vertex': '1', 'parent': parent})
            ET.SubElement(c, 'mxGeometry', {'x': fmt(e['x']), 'y': fmt(e['y']), 'width': fmt(e['w']), 'height': fmt(e['h']), 'as': 'geometry'})
        elif e['t'] == 'text':
            al = {'start': 'left', 'middle': 'center', 'end': 'right'}[e['anchor']]
            st = ['text', 'html=0', 'whiteSpace=nowrap', 'strokeColor=none', 'fillColor=none', 'align=' + al, 'verticalAlign=top',
                  'spacing=0', 'spacingTop=0', 'spacingLeft=0', 'spacingRight=0', 'spacingBottom=0', 'fontFamily=Helvetica',
                  'fontSize=' + fmt(e['size']), 'fontColor=' + e['color'], 'fontStyle=' + ('1' if e['bold'] else '0')]
            c = ET.SubElement(root, 'mxCell', {'id': e['id'], 'value': e['s'], 'style': drawio_style(st), 'vertex': '1', 'parent': parent})
            ET.SubElement(c, 'mxGeometry', {'x': fmt(e['x']), 'y': fmt(e['y']), 'width': fmt(e['w']), 'height': fmt(e['h']), 'as': 'geometry'})
        elif e['t'] == 'edge':
            pts = e['pts']
            st = ['html=0', 'rounded=0', 'strokeColor=' + e['color'], 'strokeWidth=' + fmt(e['sw']),
                  'endArrow=' + ('block' if e['end'] else 'none'), 'endFill=1', 'endSize=5',
                  'startArrow=' + ('block' if e['start'] else 'none'), 'startFill=1', 'startSize=5']
            if e['dash']:
                st += ['dashed=1', 'dashPattern=6 4']

            def frac(shape_id, pt, kind):
                s = shapes[shape_id]
                fx, fy = (pt[0] - s['x']) / s['w'], (pt[1] - s['y']) / s['h']
                assert abs(fx - round(fx)) < 1e-6 or abs(fy - round(fy)) < 1e-6, (e['id'], shape_id, pt)
                return ['%sX=%s' % (kind, prec(fx)), '%sY=%s' % (kind, prec(fy)), '%sDx=0' % kind, '%sDy=0' % kind, '%sPerimeter=0' % kind]

            attrs = {'id': e['id'], 'value': '', 'edge': '1', 'parent': parent}
            if e['src']:
                attrs['source'] = e['src']
                st += frac(e['src'], pts[0], 'exit')
            if e['tgt']:
                attrs['target'] = e['tgt']
                st += frac(e['tgt'], pts[-1], 'entry')
            attrs['style'] = drawio_style(st)
            c = ET.SubElement(root, 'mxCell', attrs)
            g = ET.SubElement(c, 'mxGeometry', {'relative': '1', 'as': 'geometry'})
            if not e['src']:
                ET.SubElement(g, 'mxPoint', {'x': fmt(pts[0][0]), 'y': fmt(pts[0][1]), 'as': 'sourcePoint'})
            if not e['tgt']:
                ET.SubElement(g, 'mxPoint', {'x': fmt(pts[-1][0]), 'y': fmt(pts[-1][1]), 'as': 'targetPoint'})
            if len(pts) > 2:
                arr = ET.SubElement(g, 'Array', {'as': 'points'})
                for p in pts[1:-1]:
                    ET.SubElement(arr, 'mxPoint', {'x': fmt(p[0]), 'y': fmt(p[1])})
    indent(mxfile)
    return ET.ElementTree(mxfile)


def main():
    svg_path = os.path.join(HERE, STEM + '.svg')
    dio_path = os.path.join(HERE, STEM + '.drawio')
    png_path = os.path.join(HERE, STEM + '.png')
    t = build_svg()
    t.write(svg_path, encoding='utf-8', xml_declaration=True)
    t = build_drawio()
    t.write(dio_path, encoding='utf-8', xml_declaration=True)
    edge_exe = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
    if os.path.exists(edge_exe):
        uri = 'file:///' + svg_path.replace('\\', '/')
        if os.path.exists(png_path):
            os.remove(png_path)
        subprocess.run([edge_exe, '--headless=new', '--disable-gpu', '--hide-scrollbars', '--force-device-scale-factor=2',
                        '--window-size=%d,%d' % (W, H), '--screenshot=' + png_path, uri], check=False,
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=120)
        import time
        for _ in range(60):
            if os.path.exists(png_path) and os.path.getsize(png_path) > 0:
                break
            time.sleep(1)
    print('built', STEM, 'elements:', len(EL))


if __name__ == '__main__':
    main()
