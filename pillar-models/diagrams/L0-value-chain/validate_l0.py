"""Independent validation of the L0 value chain map.

Parses the SVG, draw.io and PNG outputs without using the build script, then checks:
  A register integrity        B SVG hygiene (PowerPoint-safe)    C draw.io strictness (Lucid import)
  D SVG vs draw.io agreement  E register coverage both ways      F layout (fit, overlap, routing)
  G PNG matches the SVG
Exit code 1 on any error.
"""
import json
import math
import os
import re
import sys
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
STEM = 'L0_value-chain-map'
SVG_P, DIO_P, PNG_P = [os.path.join(HERE, STEM + e) for e in ('.svg', '.drawio', '.png')]
W, H = 1920, 1080
NS = '{http://www.w3.org/2000/svg}'
REG = json.load(open(os.path.join(HERE, 'l0-register.json'), encoding='utf-8'))
ERR, INFO = [], []


def err(m):
    ERR.append(m)


def close(a, b, tol=0.02):
    return abs(float(a) - float(b)) <= tol


def tw(text, size, bold=False):
    return len(text) * size * (0.62 if bold else 0.56)


# ---------------------------------------------------------------- A register
def check_register():
    raw = open(os.path.join(HERE, 'l0-register.json'), encoding='utf-8').read()
    if '—' in raw or '–' in raw:
        err('A register: contains an em or en dash')
    ids = [p['id'] for p in REG['pillars']] + [f['id'] for f in REG['flows']] + [c['id'] for c in REG['ctps']]
    if len(ids) != len(set(ids)):
        err('A register: duplicate ids')
    pids = {p['id'] for p in REG['pillars']} | {'out'}
    for f in REG['flows']:
        if f['from'] not in pids or f['to'] not in pids:
            err('A register: flow %s has unknown endpoint' % f['id'])
        if f['type'] not in ('material', 'information', 'gate', 'support'):
            err('A register: flow %s has unknown type %s' % (f['id'], f['type']))
    fids = {f['id'] for f in REG['flows']}
    for c in REG['ctps']:
        if c['flow'] not in fids:
            err('A register: ctp %s points at unknown flow' % c['id'])
    # canonical stance: P6 must link to P1..P4 and P5 (to confirm counts), P5 to P1..P4 and P6
    for target in ('p1', 'p2', 'p3', 'p4'):
        if not any(f['from'] == 'p6' and f['to'] == target for f in REG['flows']):
            err('A register: no Pillar 6 link recorded for %s' % target)
        if not any(f['from'] == 'p5' and f['to'] == target for f in REG['flows']):
            err('A register: no Pillar 5 link recorded for %s' % target)


# ---------------------------------------------------------------- B SVG
FORBIDDEN_TAGS = {'style', 'marker', 'filter', 'mask', 'image', 'use', 'defs', 'script', 'foreignObject', 'clipPath',
                  'linearGradient', 'radialGradient', 'pattern', 'symbol', 'switch', 'animate', 'set'}
LAYERS = ['layer-diagram', 'layer-status', 'layer-inflight', 'layer-annotation', 'layer-legend']


def local(tag):
    return tag.split('}')[-1]


def load_svg():
    tree = ET.parse(SVG_P)
    root = tree.getroot()
    if local(root.tag) != 'svg':
        err('B svg: root is not svg')
    if root.get('viewBox') != '0 0 %d %d' % (W, H) or root.get('width') != str(W) or root.get('height') != str(H):
        err('B svg: canvas is not %dx%d' % (W, H))
    ids = []
    for el in root.iter():
        t = local(el.tag)
        if t in FORBIDDEN_TAGS:
            err('B svg: forbidden element <%s>' % t)
        for a in ('class', 'style'):
            if el.get(a) is not None:
                err('B svg: forbidden attribute %s on %s' % (a, el.get('id') or t))
        if el.get('id'):
            ids.append(el.get('id'))
        if t == 'text':
            if not el.get('font-family'):
                err('B svg: text %s has no font-family' % el.get('id'))
            if not (el.text or '').strip():
                err('B svg: text %s is empty' % el.get('id'))
            if '—' in el.text or '–' in el.text:
                err('B svg: dash in text %s' % el.get('id'))
    if len(ids) != len(set(ids)):
        err('B svg: duplicate ids %s' % sorted({i for i in ids if ids.count(i) > 1}))
    tops = [c.get('id') for c in root if local(c.tag) == 'g']
    if tops != LAYERS:
        err('B svg: top-level layers are %s, expected %s' % (tops, LAYERS))
    return root


def parse_path(d):
    return [tuple(float(v) for v in m.split(',')) for m in re.findall(r'[ML]\s*(-?[\d.]+,-?[\d.]+)', d)]


def svg_model(root):
    m = {'rect': {}, 'ellipse': {}, 'text': {}, 'edge': {}, 'layer': {}}
    for lg in root:
        if local(lg.tag) != 'g':
            continue
        for el in lg.iter():
            t = local(el.tag)
            i = el.get('id')
            m['layer'][i] = lg.get('id')
            if t == 'rect':
                m['rect'][i] = dict(x=float(el.get('x')), y=float(el.get('y')), w=float(el.get('width')), h=float(el.get('height')),
                                    fill=el.get('fill').upper(), stroke=el.get('stroke').upper(), sw=float(el.get('stroke-width')),
                                    rx=float(el.get('rx', 0)), dash=bool(el.get('stroke-dasharray')))
            elif t == 'ellipse':
                rx, ry = float(el.get('rx')), float(el.get('ry'))
                m['ellipse'][i] = dict(x=float(el.get('cx')) - rx, y=float(el.get('cy')) - ry, w=2 * rx, h=2 * ry,
                                       fill=el.get('fill').upper(), stroke=el.get('stroke').upper(), sw=float(el.get('stroke-width')),
                                       dash=bool(el.get('stroke-dasharray')))
            elif t == 'text':
                m['text'][i] = dict(s=el.text, x=float(el.get('x')), y=float(el.get('y')), size=float(el.get('font-size')),
                                    color=el.get('fill').upper(), bold=el.get('font-weight') == 'bold', anchor=el.get('text-anchor'))
            elif t == 'g' and i and not i.startswith(('layer-', 'status_')):
                line = el.find(NS + 'path')
                pts = parse_path(line.get('d'))
                heads = {}
                for hp in el.findall(NS + 'path')[1:]:
                    heads[hp.get('id').rsplit('_', 1)[1]] = parse_path(hp.get('d'))
                if 'end' in heads:
                    pts[-1] = heads['end'][0]
                if 'start' in heads:
                    pts[0] = heads['start'][0]
                m['edge'][i] = dict(pts=pts, color=line.get('stroke').upper(), sw=float(line.get('stroke-width')),
                                    dash=bool(line.get('stroke-dasharray')), end='end' in heads, start='start' in heads)
    return m


# ---------------------------------------------------------------- C draw.io
ALLOWED_STYLE_KEYS = {'text', 'ellipse', 'rounded', 'whiteSpace', 'html', 'fillColor', 'strokeColor', 'strokeWidth', 'absoluteArcSize',
                      'arcSize', 'dashed', 'dashPattern', 'align', 'verticalAlign', 'spacing', 'spacingTop', 'spacingLeft',
                      'spacingRight', 'spacingBottom', 'fontFamily', 'fontSize', 'fontColor', 'fontStyle', 'endArrow', 'endFill',
                      'endSize', 'startArrow', 'startFill', 'startSize', 'exitX', 'exitY', 'exitDx', 'exitDy', 'exitPerimeter',
                      'entryX', 'entryY', 'entryDx', 'entryDy', 'entryPerimeter'}
COLOR = re.compile(r'^#[0-9A-Fa-f]{6}$')


def parse_style(s, where):
    d = {}
    if not s.endswith(';'):
        err('C drawio: style of %s does not end with ;' % where)
    for part in [p for p in s.split(';') if p]:
        if '=' in part:
            k, v = part.split('=', 1)
        else:
            k, v = part, '1'
        if k in d:
            err('C drawio: duplicate style key %s in %s' % (k, where))
        if k not in ALLOWED_STYLE_KEYS:
            err('C drawio: style key %s in %s is outside the allowed set' % (k, where))
        d[k] = v
    for k in ('fillColor', 'strokeColor', 'fontColor'):
        if k in d and d[k] != 'none' and not COLOR.match(d[k]):
            err('C drawio: bad colour %s=%s in %s' % (k, d[k], where))
    return d


def load_drawio():
    raw = open(DIO_P, 'rb').read()
    if raw.startswith(b'\xef\xbb\xbf'):
        err('C drawio: has a BOM')
    if not raw.startswith(b'<?xml version="1.0" encoding="UTF-8"?>'):
        err('C drawio: XML declaration is not the standard double-quoted form')
    if re.search(rb'[\x00-\x08\x0b\x0c\x0e-\x1f]', raw):
        err('C drawio: control characters present')
    root = ET.fromstring(raw)
    if root.tag != 'mxfile':
        err('C drawio: root is not mxfile')
    diagrams = root.findall('diagram')
    if len(diagrams) != 1:
        err('C drawio: expected exactly one diagram, found %d' % len(diagrams))
    model = diagrams[0].find('mxGraphModel')
    if model is None:
        err('C drawio: diagram content is compressed or missing mxGraphModel')
        return None
    r = model.find('root')
    cells = r.findall('mxCell')
    ids = [c.get('id') for c in cells]
    if len(ids) != len(set(ids)):
        err('C drawio: duplicate cell ids')
    if ids[0] != '0':
        err('C drawio: first cell is not id 0')
    byid = {c.get('id'): c for c in cells}
    layers = [c.get('id') for c in cells if c.get('parent') == '0']
    if layers != ['1']:
        err('C drawio: expected the single layer cell id 1, found %s' % layers)
    model_out = {'rect': {}, 'ellipse': {}, 'text': {}, 'edge': {}}
    for c in cells:
        cid = c.get('id')
        if cid == '0' or c.get('parent') == '0':
            continue
        if c.get('parent') != '1':
            err('C drawio: %s is not on the single layer' % cid)
        style = parse_style(c.get('style', ''), cid)
        if c.get('vertex') == '1':
            g = c.find('mxGeometry')
            if g is None or g.get('as') != 'geometry':
                err('C drawio: vertex %s has no geometry' % cid)
                continue
            geo = {k: float(g.get(k)) for k in ('x', 'y', 'width', 'height')}
            if not all(math.isfinite(v) for v in geo.values()):
                err('C drawio: non-finite geometry in %s' % cid)
            if 'text' in style:
                model_out['text'][cid] = dict(geo=geo, s=c.get('value'), style=style)
            elif 'ellipse' in style:
                model_out['ellipse'][cid] = dict(geo=geo, style=style)
            else:
                model_out['rect'][cid] = dict(geo=geo, style=style)
        elif c.get('edge') == '1':
            g = c.find('mxGeometry')
            if g is None or g.get('relative') != '1':
                err('C drawio: edge %s geometry is not relative' % cid)
                continue
            for k in ('source', 'target'):
                if c.get(k) and c.get(k) not in byid:
                    err('C drawio: edge %s %s does not exist' % (cid, k))
            model_out['edge'][cid] = dict(cell=c, geom=g, style=style)
        else:
            err('C drawio: cell %s is neither vertex nor edge' % cid)
        if c.get('value') and ('\n' in c.get('value') or '<' in c.get('value')):
            err('C drawio: value of %s has markup or newline' % cid)
        if c.get('value') and re.search(r'&[A-Za-z#]', c.get('value')):
            err('C drawio: value of %s has an ampersand an HTML label would misread' % cid)
        if style.get('html') != '1':
            err('C drawio: %s is not an html=1 cell' % cid)
    return model_out


def drawio_edge_points(e, shapes):
    c, g, st = e['cell'], e['geom'], e['style']

    def term(which, kind):
        sid = c.get(which)
        if sid:
            s = shapes[sid]['geo']
            return (s['x'] + float(st[kind + 'X']) * s['width'], s['y'] + float(st[kind + 'Y']) * s['height'])
        p = [q for q in g.findall('mxPoint') if q.get('as') == which + 'Point']
        return (float(p[0].get('x')), float(p[0].get('y'))) if p else None

    pts = [term('source', 'exit')]
    arr = g.find('Array')
    if arr is not None:
        pts += [(float(q.get('x')), float(q.get('y'))) for q in arr.findall('mxPoint')]
    pts.append(term('target', 'entry'))
    return pts


# ---------------------------------------------------------------- D agreement
def compare(svg, dio):
    for kind in ('rect', 'ellipse', 'text', 'edge'):
        a, b = set(svg[kind]) - ({'bg'} if kind == 'rect' else set()), set(dio[kind])
        if a != b:
            err('D agree: %s ids differ. only svg=%s only drawio=%s' % (kind, sorted(a - b)[:6], sorted(b - a)[:6]))
    shapes = dict(dio['rect'])
    shapes.update(dio['ellipse'])
    for kind in ('rect', 'ellipse'):
        for i, s in svg[kind].items():
            d = dio[kind].get(i)
            if not d:
                continue
            g = d['geo']
            if not (close(s['x'], g['x']) and close(s['y'], g['y']) and close(s['w'], g['width']) and close(s['h'], g['height'])):
                err('D agree: geometry of %s differs' % i)
            st = d['style']
            if s['fill'] != st['fillColor'].upper() or s['stroke'] != st['strokeColor'].upper() or not close(s['sw'], st['strokeWidth']):
                err('D agree: colours or stroke of %s differ' % i)
            if s['dash'] != (st.get('dashed') == '1'):
                err('D agree: dash of %s differs' % i)
            if kind == 'rect' and s['rx']:
                if st.get('rounded') != '1' or not close(s['rx'], st['arcSize']) or st.get('absoluteArcSize') != '1':
                    err('D agree: corner radius of %s differs' % i)
    for i, s in svg['text'].items():
        d = dio['text'].get(i)
        if not d:
            continue
        g, st = d['geo'], d['style']
        if s['s'] != d['s']:
            err('D agree: text of %s differs' % i)
        al = {'left': 'start', 'center': 'middle', 'right': 'end'}[st['align']]
        if al != s['anchor']:
            err('D agree: anchor of %s differs' % i)
        sx = g['x'] if al == 'start' else (g['x'] + g['width'] / 2 if al == 'middle' else g['x'] + g['width'])
        if not close(sx, s['x']):
            err('D agree: text x of %s differs (%s vs %s)' % (i, sx, s['x']))
        if not close(g['y'] + round(s['size'] * 0.95), s['y']):
            err('D agree: text baseline of %s differs' % i)
        if not close(st['fontSize'], s['size']) or st['fontColor'].upper() != s['color'] or (st['fontStyle'] == '1') != s['bold']:
            err('D agree: font of %s differs' % i)
        if not st['fontFamily'].startswith('Helvetica'):
            err('D agree: font family of %s' % i)
    for i, s in svg['edge'].items():
        d = dio['edge'].get(i)
        if not d:
            continue
        pts = drawio_edge_points(d, shapes)
        if any(p is None for p in pts) or len(pts) != len(s['pts']):
            err('D agree: edge %s point count differs' % i)
            continue
        for p, q in zip(pts, s['pts']):
            if not (close(p[0], q[0], 0.05) and close(p[1], q[1], 0.05)):
                err('D agree: edge %s waypoint differs %s vs %s' % (i, p, q))
        st = d['style']
        if (st['endArrow'] == 'block') != s['end'] or (st['startArrow'] == 'block') != s['start']:
            err('D agree: arrowheads of %s differ' % i)
        if st['strokeColor'].upper() != s['color'] or not close(st['strokeWidth'], s['sw']) or (st.get('dashed') == '1') != s['dash']:
            err('D agree: edge style of %s differs' % i)
        # connected endpoints must sit on their shape boundary
        for which, kind, idx in (('source', 'exit', 0), ('target', 'entry', -1)):
            sid = d['cell'].get(which)
            if sid:
                sg = shapes[sid]['geo']
                x, y = pts[idx]
                on_v = close(x, sg['x']) or close(x, sg['x'] + sg['width'])
                on_h = close(y, sg['y']) or close(y, sg['y'] + sg['height'])
                inside = sg['x'] - 0.02 <= x <= sg['x'] + sg['width'] + 0.02 and sg['y'] - 0.02 <= y <= sg['y'] + sg['height'] + 0.02
                if not (inside and (on_v or on_h)):
                    err('D agree: %s of %s is not on the boundary of %s' % (which, i, sid))


# ---------------------------------------------------------------- E coverage
def group_texts(svg):
    groups = {}
    for i, t in svg['text'].items():
        m = re.match(r'^(.*)_(\d+)$', i)
        key, n = (m.group(1), int(m.group(2))) if m else (i, 0)
        groups.setdefault(key, []).append((n, t['s']))
    return {k: ' '.join(s for _, s in sorted(v)) for k, v in groups.items()}, \
           {k: [s for _, s in sorted(v)] for k, v in groups.items()}


def coverage(svg, dio):
    joined, lines = group_texts(svg)
    expected = {'title': REG['title'], 'subtitle': REG['headline'], 'legend_key': 'KEY'}
    P = {p['id']: p for p in REG['pillars']}
    for pid in ('p5', 'p6'):
        p = P[pid]
        expected['band_%s_name' % pid] = '%d %s' % (p['num'], p['name'].upper())
        expected['band_%s_role' % pid] = p['role']
        expected['band_%s_areas' % pid] = ' · '.join('%s %s' % tuple(a) for a in p['areas'])
    for pid in ('p1', 'p2', 'p3', 'p4'):
        p = P[pid]
        expected['box_%s_name' % pid] = '%d %s' % (p['num'], p['name'])
        expected['box_%s_area' % pid] = ' '.join('%s %s' % tuple(a) for a in p['areas'])
        if p.get('note'):
            expected['box_%s_note' % pid] = p['note']
        if lines['box_%s_area' % pid] != ['%s %s' % tuple(a) for a in p['areas']]:
            err('E coverage: area lines of %s are not one per area in order' % pid)
    for f in REG['flows']:
        if 'flow_' + f['id'] not in svg['edge']:
            err('E coverage: flow %s has no edge' % f['id'])
        if f['id'].startswith(('g_', 's_', 'x_')):
            expected['tag_%s_t' % f['id']] = f['label']
            if 'tag_' + f['id'] not in svg['rect']:
                err('E coverage: flow %s has no tag' % f['id'])
        elif f.get('label'):
            expected['lbl_' + f['id']] = f['label']
        if f.get('status') == 'to_confirm':
            if 'ring_' + f['id'] not in svg['ellipse'] or svg['layer'].get('ring_' + f['id']) != 'layer-status':
                err('E coverage: to-confirm mark for %s missing or not in the status layer' % f['id'])
            expected['ringq_' + f['id']] = '?'
        ed = svg['edge'].get('flow_' + f['id'])
        if f['id'] == 'x_p6_p5':
            up = svg['edge'].get('flow_x_p6_p5_up')
            if not up or not ed or ed['start'] or up['start'] or not (ed['pts'][0][1] < ed['pts'][-1][1] and up['pts'][0][1] > up['pts'][-1][1]):
                err('E coverage: the Pillar 5 and 6 link must be two opposite single-headed arrows')
        elif ed and f['type'] in ('gate', 'support') and bool(f.get('bidirectional')) != ed['start']:
            err('E coverage: arrowheads of %s do not match bidirectional=%s' % (f['id'], f.get('bidirectional')))
    for c in REG['ctps']:
        expected['pill_%s_t' % c['id']] = c['label']
        expected['detail_' + c['id']] = c['detail']
    expected['keys_title'] = REG['join_keys_title'].upper()
    for n, k in enumerate(REG['join_keys']):
        expected['key_%d_t' % n] = '%s (%s)' % (k['key'], ', '.join(str(p) for p in k['pillars']))
    L = REG['legend']
    for k in ('material', 'information', 'p6_link', 'p5_link', 'to_confirm'):
        expected['legend_%s_t' % k] = L[k]
    expected['legend_ctp_t'] = L['ctp']
    expected['legend_pill_t'] = 'CTP'
    for key, want in expected.items():
        got = joined.get(key)
        if got != want:
            err('E coverage: text %s is %r, register says %r' % (key, got, want))
    for key in joined:
        if key not in expected:
            err('E coverage: text %s is not derived from the register' % key)
    # every pillar and area name is present
    alltext = ' '.join(joined.values())
    for p in REG['pillars']:
        if p['name'].upper() not in alltext.upper():
            err('E coverage: pillar %s name missing' % p['id'])
    # draw.io carries the same text
    dtexts = sorted(t['s'] for t in dio['text'].values())
    stexts = sorted(t['s'] for t in svg['text'].values())
    if dtexts != stexts:
        err('E coverage: draw.io text set differs from SVG')
    # the register's own claims about the diagram
    if sum(1 for f in REG['flows'] if f.get('status') == 'to_confirm') != 1:
        INFO.append('note: to-confirm count is not 1')


# ---------------------------------------------------------------- colour classes
INK, MUTED, AMBER, VIOLET = '#0F172A', '#475569', '#F59E0B', '#8B5CF6'


def check_classes(svg):
    """Solid ink is material flow only; dashed grey is information; amber is Pillar 6; violet is Pillar 5."""
    E = svg['edge']
    for f in REG['flows']:
        e = E.get('flow_' + f['id'])
        if not e:
            continue
        t = f['type']
        want = {'material': (INK, False), 'information': (MUTED, True),
                'gate': (AMBER, f.get('status') == 'to_confirm'), 'support': (VIOLET, False)}[t]
        if (e['color'], e['dash']) != want:
            err('F classes: %s is %s dash=%s but a %s link must be %s dash=%s' % (f['id'], e['color'], e['dash'], t, want[0], want[1]))
        if (f['id'].startswith('g_') and f['from'] != 'p6') or (f['id'].startswith('s_') and f['from'] != 'p5'):
            err('F classes: %s starts at the wrong pillar' % f['id'])
        tg = svg['rect'].get('tag_' + f['id'])
        if tg and t in ('gate', 'support') and f['id'] != 'x_p6_p5' and tg['stroke'] != want[0]:
            err('F classes: tag of %s is not in the link colour' % f['id'])
    up = E.get('flow_x_p6_p5_up')
    if up and (up['color'], up['dash']) != (VIOLET, False):
        err('F classes: the upward Pillar 5 arrow must be solid violet')
    for i, e in E.items():
        if not e['dash'] and e['color'] == INK and not (i.startswith('flow_f_p') or i == 'legend_material'):
            err('F classes: %s is solid ink but is not a material flow' % i)
        if not e['dash'] and e['color'] in (AMBER, VIOLET) and i.startswith('flow_f_'):
            err('F classes: %s is a chain flow drawn in a Pillar 5 or 6 colour' % i)
    for i, want in (('legend_material', (INK, False)), ('legend_information', (MUTED, True)),
                    ('legend_p6_link', (AMBER, False)), ('legend_p5_link', (VIOLET, False))):
        e = E.get(i)
        if not e or (e['color'], e['dash']) != want or not e['end']:
            err('F classes: legend sample %s is missing or does not match the diagram' % i)


# ---------------------------------------------------------------- F layout
def seg_rect(p, q, r, pad=0.0):
    x0, y0, x1, y1 = r['x'] - pad, r['y'] - pad, r['x'] + r['w'] + pad, r['y'] + r['h'] + pad
    if p[0] == q[0]:
        return x0 < p[0] < x1 and min(p[1], q[1]) < y1 and max(p[1], q[1]) > y0
    if p[1] == q[1]:
        return y0 < p[1] < y1 and min(p[0], q[0]) < x1 and max(p[0], q[0]) > x0
    return True


def segs(pts):
    return list(zip(pts[:-1], pts[1:]))


def layout(svg):
    rects = svg['rect']
    for i, e in svg['edge'].items():
        for p, q in segs(e['pts']):
            if p[0] != q[0] and p[1] != q[1]:
                err('F layout: edge %s has a diagonal segment' % i)
    # content margins (everything except the full-bleed background)
    for i, r in rects.items():
        if i == 'bg':
            continue
        if r['x'] < 32 - 0.01 or r['x'] + r['w'] > W - 32 + 0.01 or r['y'] < 6 - 0.01 or r['y'] + r['h'] > H - 32:
            err('F layout: %s breaks the 32 px margin' % i)
    # rect overlaps among cards, boxes, pills and bands
    cand = [i for i in rects if i.startswith(('box_p', 'tag_', 'pill_', 'band_', 'keys_card'))]
    for a in range(len(cand)):
        for b in range(a + 1, len(cand)):
            r1, r2 = rects[cand[a]], rects[cand[b]]
            if r1['x'] < r2['x'] + r2['w'] and r2['x'] < r1['x'] + r1['w'] and r1['y'] < r2['y'] + r2['h'] and r2['y'] < r1['y'] + r1['h']:
                err('F layout: %s overlaps %s' % (cand[a], cand[b]))
    # edges against boxes and foreign cards
    owner = {}
    for f in REG['flows']:
        owner['flow_' + f['id']] = {'tag_' + f['id']}
    owner['flow_x_p6_p5_up'] = {'tag_x_p6_p5'}
    for c in REG['ctps']:
        owner['flow_' + c['flow']].add('pill_' + c['id'])
    for i, e in svg['edge'].items():
        if i.startswith('flow_legend') or i.startswith('legend_'):
            continue
        for p, q in segs(e['pts']):
            for rid, r in rects.items():
                if rid.startswith('box_p') and seg_rect(p, q, r, -1.0):
                    err('F layout: edge %s passes through %s' % (i, rid))
                if rid.startswith(('tag_', 'pill_', 'key_', 'keys_card')) and rid not in owner.get(i, set()) and seg_rect(p, q, r, 1.0):
                    err('F layout: edge %s touches foreign card %s' % (i, rid))
    # text fit and overlap
    boxes = []
    for i, t in svg['text'].items():
        w = tw(t['s'], t['size'], t['bold'])
        left = t['x'] if t['anchor'] == 'start' else (t['x'] - w / 2 if t['anchor'] == 'middle' else t['x'] - w)
        top, bottom = t['y'] - t['size'] * 0.85, t['y'] + t['size'] * 0.25
        boxes.append((i, left, top, left + w, bottom))
        cx, cy = left + w / 2, (top + bottom) / 2
        inside = [r for r in list(rects.values()) if r is not rects['bg'] and r['x'] <= cx <= r['x'] + r['w'] and r['y'] <= cy <= r['y'] + r['h']]
        if inside:
            r = min(inside, key=lambda z: z['w'] * z['h'])
            if left < r['x'] + 4 or left + w > r['x'] + r['w'] - 4 or top < r['y'] + 1 or bottom > r['y'] + r['h'] - 1:
                if i != 'legend_pill_t':
                    err('F layout: text %s does not fit its container (needs ~%d px)' % (i, w))
        elif left < 32 or left + w > W - 32:
            err('F layout: text %s breaks the margin' % i)
    for a in range(len(boxes)):
        for b in range(a + 1, len(boxes)):
            n1, l1, t1, r1, b1 = boxes[a]
            n2, l2, t2, r2, b2 = boxes[b]
            if l1 < r2 and l2 < r1 and t1 < b2 and t2 < b1:
                err('F layout: text %s overlaps %s' % (n1, n2))
    # free labels against edges
    for i, l, t, r, b in boxes:
        host = [rr for k, rr in rects.items() if k != 'bg' and rr['x'] <= (l + r) / 2 <= rr['x'] + rr['w'] and rr['y'] <= (t + b) / 2 <= rr['y'] + rr['h']]
        if host and min(host, key=lambda z: z['w'] * z['h']) is not None and not i.startswith(('lbl_', 'detail_')):
            continue
        for en, e in svg['edge'].items():
            for p, q in segs(e['pts']):
                if seg_rect(p, q, dict(x=l, y=t, w=r - l, h=b - t), 3.0):
                    err('F layout: label %s touches edge %s' % (i, en))
    # edge crossings: perpendicular only
    items = [(n, s) for n, e in svg['edge'].items() if not n.startswith('legend_') for s in segs(e['pts'])]
    crossings = 0
    for a in range(len(items)):
        for b in range(a + 1, len(items)):
            (n1, (p1, q1)), (n2, (p2, q2)) = items[a], items[b]
            if n1 == n2:
                continue
            v1, v2 = p1[0] == q1[0], p2[0] == q2[0]
            if v1 == v2:
                if v1 and p1[0] == p2[0] and min(p1[1], q1[1]) < max(p2[1], q2[1]) and min(p2[1], q2[1]) < max(p1[1], q1[1]):
                    err('F layout: %s and %s overlap along a line' % (n1, n2))
                if (not v1) and p1[1] == p2[1] and min(p1[0], q1[0]) < max(p2[0], q2[0]) and min(p2[0], q2[0]) < max(p1[0], q1[0]):
                    err('F layout: %s and %s overlap along a line' % (n1, n2))
                continue
            (vp, vq), (hp, hq) = ((p1, q1), (p2, q2)) if v1 else ((p2, q2), (p1, q1))
            if min(hp[0], hq[0]) < vp[0] < max(hp[0], hq[0]) and min(vp[1], vq[1]) < hp[1] < max(vp[1], vq[1]):
                crossings += 1
    INFO.append('edge crossings (all perpendicular): %d' % crossings)


# ---------------------------------------------------------------- G PNG
def check_png(svg):
    try:
        from PIL import Image
    except ImportError:
        err('G png: Pillow not available')
        return
    if not os.path.exists(PNG_P):
        err('G png: missing')
        return
    im = Image.open(PNG_P).convert('RGB')
    sx = im.size[0] / W
    if abs(im.size[0] / im.size[1] - W / H) > 0.01 or im.size[0] < W:
        err('G png: size %s is not 16:9 at or above %dx%d' % (im.size, W, H))
    px = im.load()
    nonwhite = sum(1 for x in range(0, im.size[0], 8) for y in range(0, im.size[1], 8) if px[x, y] != (255, 255, 255))
    frac = nonwhite / ((im.size[0] // 8) * (im.size[1] // 8))
    if not 0.03 < frac < 0.7:
        err('G png: ink fraction %.3f looks wrong' % frac)

    def hexrgb(h):
        return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))
    for rid in ('box_p1', 'box_p2', 'box_p3', 'box_p4', 'band_p5', 'band_p6'):
        r = svg['rect'][rid]
        x, y = int((r['x'] + 12) * sx), int((r['y'] + r['h'] - 8) * sx)
        got, want = px[x, y], hexrgb(r['fill'])
        if max(abs(a - b) for a, b in zip(got, want)) > 6:
            err('G png: %s pixel %s does not match fill %s' % (rid, got, want))
    INFO.append('png %dx%d, ink %.1f%%' % (im.size[0], im.size[1], frac * 100))


def main():
    check_register()
    root = load_svg()
    svg = svg_model(root)
    dio = load_drawio()
    if dio:
        compare(svg, dio)
        coverage(svg, dio)
    check_classes(svg)
    layout(svg)
    check_png(svg)
    for line in INFO:
        print(line)
    if ERR:
        print('FAIL: %d error(s)' % len(ERR))
        for e in ERR:
            print(' -', e)
        sys.exit(1)
    print('PASS: register, svg, drawio and png agree (%d text, %d shapes, %d edges)' % (
        len(svg['text']), len(svg['rect']) + len(svg['ellipse']), len(svg['edge'])))


if __name__ == '__main__':
    main()
