# L0 Value Chain Map

Companion to [00-cross-reference-and-summary.md](../../00-cross-reference-and-summary.md). The whole value chain, with each box a pillar. It is a value chain map and not a BPMN: the links from Pillars 5 and 6 are many-to-many and attach to specific steps, which BPMN sequence flows cannot show. BPMN is used from L1 down, where there is a sequence.

| File | Purpose |
|---|---|
| [L0_value-chain-map.svg](L0_value-chain-map.svg) | PowerPoint-safe vector view |
| [L0_value-chain-map.png](L0_value-chain-map.png) | 3840 x 2160 render of the SVG |
| [L0_value-chain-map.drawio](L0_value-chain-map.drawio) | Editable copy for draw.io and Lucid import |
| [l0-register.json](l0-register.json) | The register: pillars, areas, flows, CTPs, shared keys, with the source and step IDs behind each link |
| `build_l0.py` | Generates the three views from the register |
| `validate_l0.py` | Checks the three views against each other and the register |

## Levels

| Level | Scope | Where |
|---|---|---|
| L0 | The whole value chain; each box is a pillar | this folder |
| L1 | One pillar; each box is an L2 area | `../bpmn/[pillar folder]/[pillar number]_[title].bpmn` |
| L2 | One area; each box is an L3 sub-process | `../bpmn/[pillar folder]` |
| L3 | One sub-process; each box is an L4 step | `../bpmn/[pillar folder]` |

The decomposition tables number it this way: the pillar is "2", its areas "2.x" are labelled L2.

## Changing the map

1. Edit `l0-register.json`. Never type a label or link into the SVG or draw.io file.
2. `python build_l0.py` regenerates the SVG and draw.io files and renders the PNG (needs Microsoft Edge).
3. `python validate_l0.py` must print PASS. It checks the register, SVG hygiene, draw.io strictness for import, SVG against draw.io, register coverage in both directions, layout, and the PNG.

Open item: Pillar 6 to Pillar 4 is shown as "To confirm". The Pillar 6 interaction table has no Pillar 4 row, while the standards matrix lists ICMM controls as secondary for Pillar 4.
