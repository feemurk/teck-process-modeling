"""Shared engine for generating BPMN 2.0 diagrams from a pillar or product model file.

A build script declares diagrams with N() nodes, F() flows and A() associations on a
lane / row / column grid, then calls build_all(). Names and documentation of numbered
steps come from the model file's Process Decomposition tables, so diagrams cannot drift
from the model.

Layout follows the Pillar 3 diagram set and the bpmn-style-guide skill: tasks 170 x 80,
collapsed sub-processes 170 x 96, events 56, gateways 70, 36 px gaps, 170 px rows,
orthogonal flows, gateway labels above-left, Yes / No beside exits.

Also provides:
  sync_docs()  refresh names and documentation of numbered steps in diagrams that are
               not generated (hand-laid diagrams), leaving their layout untouched
  coverage()   check every L2, L3 and L4 row is drawn exactly once in a folder
"""
import os
import re
import sys
import textwrap
from xml.sax.saxutils import escape

TASK_W, TASK_H, SUB_H, EV, GW = 170, 80, 96, 56, 70
GAP, ROW, X0 = 36, 170, 110
MIN_COL = {'event': 120, 'gw': 140}
EV_LABEL_W, GW_LABEL_W = 120, 100  # the style-guide checker fits (width - 6) / 6.5 chars a line
CORRIDOR = 30                      # distance of an over-the-top corridor above the gateway
AUTO_ACTORS = {'DCS Auto-control', 'DCS', 'Automated DCS', 'DCS / SCADA', 'DCS/SCADA'}
NARRATIVE_DOC = ('Derived from the Process Flow Narratives section (not a row in the '
                 'Process Decomposition).')


# ---------------------------------------------------------------- model rows

def parse_model(path):
    """Rows of the decomposition tables: 11 cells, first cell an ID such as 3.2.1.4."""
    rows = {}
    for line in open(path, encoding='utf-8'):
        if not line.startswith('| '):
            continue
        cells = [c.strip() for c in re.split(r'(?<!\\)\|', line.strip())[1:-1]]
        m = re.fullmatch(r'\**(\d(?:\.\d+)*)\**', cells[0]) if cells else None
        if not m or len(cells) != 11:
            continue
        clean = lambda s: s.replace('\\|', '|').strip()
        desc = clean(cells[2])
        if desc.startswith('*') and desc.endswith('*'):
            desc = desc[1:-1]
        rid = m.group(1)
        if rid in rows:
            sys.exit('duplicate row %s' % rid)
        rows[rid] = dict(id=rid, name=clean(cells[1]).strip('*'), desc=desc, isa=clean(cells[3]),
                         actors=clean(cells[7]), std=clean(cells[9]), ddvc=clean(cells[10]))
    return rows


def row_doc(r):
    return '%s\nISA-95 level: %s\nActors: %s\nStandard alignment: %s\nDDVC layer: %s' % (
        r['desc'], r['isa'], r['actors'], r['std'], r['ddvc'])


def kebab(title):
    t = title.lower().replace('&', 'and')
    return re.sub(r'[^a-z0-9]+', '-', t).strip('-')


def file_name(did, title):
    return '%s_%s.bpmn' % (did, kebab(title))


# ---------------------------------------------------------------- spec helpers

def N(key, kind, lane, row, col, name=None, doc=None):
    """kind: start, mstart, end, mend, task, sub, xgw, pgw. Numbered keys take name and doc
    from the model; other tasks are narrative-only steps."""
    return dict(key=key, kind=kind, lane=lane, row=row, col=col, name=name, doc=doc)


def F(src, tgt, label=None, out=None, inn=None, default=False, ch=None, assoc=False):
    """out / inn: side L, R, T or B. ch: channel x (L/R to L/R) or corridor y (T/B to T/B);
    ch='over' runs a corridor above the source gateway, ch='below' under the pool."""
    return dict(src=src, tgt=tgt, label=label, out=out, inn=inn, default=default, ch=ch, assoc=assoc)


def A(src, tgt, out=None, inn=None):
    return F(src, tgt, out=out, inn=inn, assoc=True)


# ---------------------------------------------------------------- layout

def wrap_lines(text, chars):
    return textwrap.wrap(text, chars, break_long_words=False) or ['']


def size(kind):
    if kind == 'task':
        return TASK_W, TASK_H
    if kind == 'sub':
        return TASK_W, SUB_H
    if kind in ('xgw', 'pgw'):
        return GW, GW
    return EV, EV


def col_class(kind):
    return 'gw' if kind in ('xgw', 'pgw') else 'event' if kind in ('start', 'mstart', 'end', 'mend') else 'box'


def layout(d):
    lanes = d['lanes']
    rows = {k: 1 + max([n['row'] for n in d['nodes'] if n['lane'] == k] + [0]) for k, _ in lanes}
    ncol = 1 + max(n['col'] for n in d['nodes'])
    widths = []
    for c in range(ncol):
        w = 0
        for n in d['nodes']:
            if n['col'] == c:
                w = max(w, size(n['kind'])[0], MIN_COL.get(col_class(n['kind']), 0))
        widths.append(w or MIN_COL['event'])
    left, x = [], X0
    for w in widths:
        left.append(x)
        x += w + GAP
    pool_right = x - GAP + 40
    lane_y, y = {}, 20
    for k, _ in lanes:
        lane_y[k] = y
        y += rows[k] * ROW
    for n in d['nodes']:
        w, h = size(n['kind'])
        cx = left[n['col']] + widths[n['col']] / 2
        cy = lane_y[n['lane']] + ROW / 2 + n['row'] * ROW
        n.update(x=round(cx - w / 2), y=round(cy - h / 2), w=w, h=h)
        n['cx'], n['cy'] = n['x'] + w / 2, n['y'] + h / 2
    d.update(rows=rows, lane_y=lane_y, pool_w=pool_right - 20, pool_h=y - 20, col_left=left)


def anchor(n, side):
    return {'L': (n['x'], n['cy']), 'R': (n['x'] + n['w'], n['cy']),
            'T': (n['cx'], n['y']), 'B': (n['cx'], n['y'] + n['h'])}[side]


def route(d, f, s, t):
    out, inn = f['out'], f['inn']
    gw = s['kind'] in ('xgw', 'pgw')
    if not out:
        if s['cy'] == t['cy']:
            out, inn = 'R', inn or 'L'
        elif gw or s['cx'] == t['cx']:
            out = 'T' if t['cy'] < s['cy'] else 'B'
        else:
            out = 'R'
    if not inn:
        if out in 'TB' and s['cx'] == t['cx']:
            inn = 'B' if out == 'T' else 'T'
        else:
            inn = 'L' if t['x'] > s['x'] else 'R'
    p0, p1 = anchor(s, out), anchor(t, inn)
    if out in 'LR' and inn in 'LR':
        if p0[1] == p1[1]:
            pts = [p0, p1]
        else:
            chx = f['ch'] or (d['col_left'][t['col']] - GAP / 2 if inn == 'L' else p1[0] + GAP / 2)
            pts = [p0, (chx, p0[1]), (chx, p1[1]), p1]
    elif out in 'LR':
        pts = [p0, (p1[0], p0[1]), p1]
    elif inn in 'LR':
        pts = [p0, (p0[0], p1[1]), p1]
    else:
        if p0[0] == p1[0] and f['ch'] is None:
            pts = [p0, p1]
        else:
            if f['ch'] == 'over':
                cy = s['y'] - CORRIDOR
            elif f['ch'] == 'below':
                cy = 20 + d['pool_h'] + 16
            else:
                cy = f['ch'] if f['ch'] is not None else (p0[1] + p1[1]) / 2
            pts = [p0, (p0[0], cy), (p1[0], cy), p1]
    lab = None
    if f['label']:
        lw = int(len(f['label']) * 6.5 + 8)
        if out == 'T':
            lab = (s['cx'] + 6, s['y'] - 18, lw, 14)
        elif out == 'B':
            lab = (s['cx'] + 6, s['y'] + s['h'] + 4, lw, 14)
        else:
            lab = (s['x'] + s['w'] + 4, s['cy'] - 20, lw, 14)
    return [(round(x), round(y)) for x, y in pts], lab


# ---------------------------------------------------------------- emit

def build(d, rows, out_dir, ns):
    """Write one diagram. d: dict(id, level, lanes, nodes, flows[, title, doc])."""
    lvl, did = d['level'], d['id']
    sfx = 'L%d_%s' % (lvl, did.replace('.', '_'))
    if 'title' in d:
        title, pdoc = d['title'], d.get('doc', '')
    else:
        title, pdoc = rows[did]['name'], rows[did]['desc']
    pool_name = '%s %s%s' % (did, title, {1: ' (L1)', 2: ' (L2)'}.get(lvl, ''))
    fname = d.get('file') or file_name(did, title)
    layout(d)
    nodes = {n['key']: n for n in d['nodes']}
    prefix = {'start': 'Start', 'mstart': 'Start', 'end': 'End', 'mend': 'End', 'xgw': 'Gw', 'pgw': 'Par', 'sub': 'Sub'}
    drawn = []
    for n in d['nodes']:
        k = n['key']
        if k in rows:
            r = rows[k]
            n['name'] = '%s %s' % (k, r['name'])
            n['doc'] = row_doc(r)
            drawn.append(k)
            if n['kind'] == 'task':
                acts = {a.strip() for a in r['actors'].split(';')}
                n['tag'] = 'serviceTask' if acts <= AUTO_ACTORS else 'task'
        elif n['kind'] == 'task':
            n['doc'] = NARRATIVE_DOC + (' ' + n['doc'] if n['doc'] else '')
            n['tag'] = 'task'
        n['tag'] = n.get('tag') or {'start': 'startEvent', 'mstart': 'startEvent', 'end': 'endEvent',
                                    'mend': 'endEvent', 'xgw': 'exclusiveGateway', 'pgw': 'parallelGateway',
                                    'sub': 'subProcess'}[n['kind']]
        pre = 'Service' if n['tag'] == 'serviceTask' else 'Task' if n['tag'] == 'task' else prefix[n['kind']]
        n['xid'] = '%s_%s_%s' % (pre, sfx, k.replace('.', '_'))
        n['inc'], n['outg'] = [], []
    seq, assoc = [], []
    for i, f in enumerate(d['flows'], 1):
        s, t = nodes[f['src']], nodes[f['tgt']]
        f['xid'] = '%s_%s_%d' % ('Assoc' if f['assoc'] else 'Flow', sfx, i)
        f['pts'], f['lab'] = route(d, f, s, t)
        if f['assoc']:
            assoc.append(f)
        else:
            seq.append(f)
            s['outg'].append(f['xid'])
            t['inc'].append(f['xid'])
    bottom_attached = set()
    for f in seq + assoc:
        for key, pt in ((f['src'], f['pts'][0]), (f['tgt'], f['pts'][-1])):
            if pt[1] == nodes[key]['y'] + nodes[key]['h'] and nodes[key]['h'] == EV:
                bottom_attached.add(key)
    X = []
    a = X.append
    a('<?xml version="1.0" encoding="UTF-8"?>')
    a('<bpmn:definitions xmlns:bpmn="http://www.omg.org/spec/BPMN/20100524/MODEL" '
      'xmlns:bpmndi="http://www.omg.org/spec/BPMN/20100524/DI" xmlns:dc="http://www.omg.org/spec/DD/20100524/DC" '
      'xmlns:di="http://www.omg.org/spec/DD/20100524/DI" id="Defs_%s" targetNamespace="%s">' % (sfx, ns))
    a('  <bpmn:collaboration id="Collab_%s">' % sfx)
    a('    <bpmn:participant id="Pool_%s" name="%s" processRef="Process_%s"/>' % (sfx, escape(pool_name), sfx))
    a('  </bpmn:collaboration>')
    a('  <bpmn:process id="Process_%s" isExecutable="false">' % sfx)
    if pdoc:
        a('    <bpmn:documentation>%s</bpmn:documentation>' % escape(pdoc))
    a('    <bpmn:laneSet id="LaneSet_%s">' % sfx)
    for k, name in d['lanes']:
        a('      <bpmn:lane id="Lane_%s_%s" name="%s">' % (sfx, k, escape(name)))
        for n in d['nodes']:
            if n['lane'] == k:
                a('        <bpmn:flowNodeRef>%s</bpmn:flowNodeRef>' % n['xid'])
        a('      </bpmn:lane>')
    a('    </bpmn:laneSet>')
    for n in d['nodes']:
        attrs = ' id="%s"' % n['xid']
        if n['name']:
            attrs += ' name="%s"' % escape(n['name'], {'"': '&quot;'})
        if n['kind'] == 'xgw':
            dflt = [f['xid'] for f in seq if f['src'] == n['key'] and f['default']]
            if dflt:
                attrs += ' default="%s"' % dflt[0]
        a('    <bpmn:%s%s>' % (n['tag'], attrs))
        if n.get('doc'):
            a('      <bpmn:documentation>%s</bpmn:documentation>' % escape(n['doc']))
        for x in n['inc']:
            a('      <bpmn:incoming>%s</bpmn:incoming>' % x)
        for x in n['outg']:
            a('      <bpmn:outgoing>%s</bpmn:outgoing>' % x)
        if n['kind'] in ('mstart', 'mend'):
            a('      <bpmn:messageEventDefinition id="Msg_%s_%s"/>' % (sfx, n['key'].replace('.', '_')))
        a('    </bpmn:%s>' % n['tag'])
    for f in seq:
        nm = ' name="%s"' % escape(f['label']) if f['label'] else ''
        a('    <bpmn:sequenceFlow id="%s"%s sourceRef="%s" targetRef="%s"/>' % (
            f['xid'], nm, nodes[f['src']]['xid'], nodes[f['tgt']]['xid']))
    for f in assoc:
        a('    <bpmn:association id="%s" associationDirection="One" sourceRef="%s" targetRef="%s"/>' % (
            f['xid'], nodes[f['src']]['xid'], nodes[f['tgt']]['xid']))
    a('  </bpmn:process>')
    a('  <bpmndi:BPMNDiagram id="Diagram_%s">' % sfx)
    a('    <bpmndi:BPMNPlane id="Plane_%s" bpmnElement="Collab_%s">' % (sfx, sfx))
    a('      <bpmndi:BPMNShape id="Pool_%s_di" bpmnElement="Pool_%s" isHorizontal="true"><dc:Bounds x="20" y="20" '
      'width="%d" height="%d"/></bpmndi:BPMNShape>' % (sfx, sfx, d['pool_w'], d['pool_h']))
    for k, _ in d['lanes']:
        a('      <bpmndi:BPMNShape id="Lane_%s_%s_di" bpmnElement="Lane_%s_%s" isHorizontal="true"><dc:Bounds x="60" '
          'y="%d" width="%d" height="%d"/></bpmndi:BPMNShape>' % (
              sfx, k, sfx, k, d['lane_y'][k], d['pool_w'] - 40, d['rows'][k] * ROW))
    for n in d['nodes']:
        extra = ' isExpanded="false"' if n['kind'] == 'sub' else ' isMarkerVisible="true"' if n['kind'] == 'xgw' else ''
        lab = ''
        if n['kind'] in ('start', 'mstart', 'end', 'mend') and n['name']:
            lines = wrap_lines(n['name'], int((EV_LABEL_W - 6) // 6.5))
            if len(lines) > 3:
                sys.exit('%s: event label "%s" needs %d lines' % (did, n['name'], len(lines)))
            hh = 14 * len(lines)
            # below the event, unless a flow attaches to its bottom
            ly = n['y'] - 6 - hh if n['key'] in bottom_attached else n['y'] + n['h'] + 6
            lab = '<bpmndi:BPMNLabel><dc:Bounds x="%d" y="%d" width="%d" height="%d"/></bpmndi:BPMNLabel>' % (
                n['cx'] - EV_LABEL_W / 2, ly, EV_LABEL_W, hh)
        elif n['kind'] == 'xgw' and n['name']:
            lines = wrap_lines(n['name'], int((GW_LABEL_W - 6) // 6.5))
            if len(lines) > 3:
                sys.exit('%s: gateway label "%s" needs %d lines' % (did, n['name'], len(lines)))
            hh = 14 * len(lines)
            lab = '<bpmndi:BPMNLabel><dc:Bounds x="%d" y="%d" width="%d" height="%d"/></bpmndi:BPMNLabel>' % (
                n['cx'] - GW_LABEL_W - 6, n['y'] - 8 - hh, GW_LABEL_W, hh)
        a('      <bpmndi:BPMNShape id="%s_di" bpmnElement="%s"%s><dc:Bounds x="%d" y="%d" width="%d" height="%d"/>%s'
          '</bpmndi:BPMNShape>' % (n['xid'], n['xid'], extra, n['x'], n['y'], n['w'], n['h'], lab))
    for f in seq + assoc:
        wp = ''.join('<di:waypoint x="%d" y="%d"/>' % p for p in f['pts'])
        lab = ''
        if f['lab']:
            lab = '<bpmndi:BPMNLabel><dc:Bounds x="%d" y="%d" width="%d" height="%d"/></bpmndi:BPMNLabel>' % f['lab']
        a('      <bpmndi:BPMNEdge id="%s_di" bpmnElement="%s">%s%s</bpmndi:BPMNEdge>' % (f['xid'], f['xid'], wp, lab))
    a('    </bpmndi:BPMNPlane>')
    a('  </bpmndi:BPMNDiagram>')
    a('</bpmn:definitions>')
    with open(os.path.join(out_dir, fname), 'w', encoding='utf-8', newline='\n') as fh:
        fh.write('\n'.join(X) + '\n')
    return fname, d['pool_w']


def build_all(diagrams, rows, out_dir, ns):
    os.makedirs(out_dir, exist_ok=True)
    written = []
    for d in diagrams:
        fname, w = build(d, rows, out_dir, ns)
        written.append(fname)
        print('built   %-58s pool %4d px' % (fname, w))
    return written


# ---------------------------------------------------------------- doc sync and coverage

TAG_RE = re.compile(r'(<bpmn:(?:task|serviceTask|subProcess) id="[^"]+" name=")([^"]+)(">\s*<bpmn:documentation>)(.*?)(</bpmn:documentation>)', re.S)
PROC_RE = re.compile(r'(<bpmn:process id="Process_L[23]_[^"]+"[^>]*>\s*<bpmn:documentation>)(.*?)(</bpmn:documentation>)', re.S)


def sync_docs(folder, rows, skip=()):
    """Refresh names and documentation of numbered steps (and L2 / L3 pool documentation)
    from the model, without touching layout. Narrative-only tasks are left alone."""
    for fn in sorted(os.listdir(folder)):
        if not fn.endswith('.bpmn') or fn in skip:
            continue
        p = os.path.join(folder, fn)
        src = open(p, encoding='utf-8').read()
        did = fn.split('_', 1)[0]

        def node(m):
            name = m.group(2).replace('&amp;', '&')
            k = name.split(' ', 1)[0]
            if k not in rows:
                return m.group(0)
            r = rows[k]
            return '%s%s%s%s%s' % (m.group(1), escape('%s %s' % (k, r['name']), {'"': '&quot;'}), m.group(3),
                                   escape(row_doc(r)), m.group(5))
        new = TAG_RE.sub(node, src)
        if did in rows and did.count('.') >= 1:
            new = PROC_RE.sub(lambda m: m.group(1) + escape(rows[did]['desc']) + m.group(3), new, count=1)
        if new != src:
            open(p, 'w', encoding='utf-8', newline='\n').write(new)
            print('synced  %s' % fn)


def coverage(folder, rows, top):
    """Every row below the top level is drawn exactly once, and every L2 and L3 row has its
    own diagram. top: the pillar ID, e.g. '3'."""
    seen = {}
    files = [f for f in os.listdir(folder) if f.endswith('.bpmn')]
    for fn in files:
        for m in re.finditer(r'<bpmn:(?:task|serviceTask|subProcess) id="[^"]+" name="([0-9.]+) ', open(
                os.path.join(folder, fn), encoding='utf-8').read()):
            seen.setdefault(m.group(1), []).append(fn)
    bad = 0
    for rid in sorted(rows, key=lambda s: [int(p) for p in s.split('.')]):
        if not rid.startswith(top + '.'):
            continue
        if len(seen.get(rid, [])) != 1:
            print('COVERAGE: row %s drawn %d times %s' % (rid, len(seen.get(rid, [])), seen.get(rid, [])))
            bad += 1
        if rid.count('.') in (1, 2) and not any(f.startswith(rid + '_') for f in files):
            print('COVERAGE: no diagram for %s' % rid)
            bad += 1
    extra = sorted(set(seen) - set(rows))
    for k in extra:
        print('COVERAGE: diagram step %s is not a row in the model %s' % (k, seen[k]))
        bad += 1
    print('%d files; %d rows; %s' % (len(files), len(rows), 'coverage OK' if not bad else '%d problems' % bad))
    return bad
