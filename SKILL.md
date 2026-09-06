---
name: obsidian-graphs
description: Create figures in Obsidian notes as interactive Graphs plugin charts. Use when an Obsidian note needs a plotted math/science figure (curves, discontinuities, tangent lines, Riemann sums, inequalities, etc.), or when existing static image embeds should become interactive graphs. Produces `graph` code blocks that the Obsidian Graphs plugin (obsidian://show-plugin?id=graphs) renders. Do not use for generating raster/photo-style images.
---

# Obsidian Graphs (Graphs plugin charts)

The **Graphs plugin** turns fenced code blocks with language `graph` into interactive coordinate plots. `graph` blocks are YAML:

````markdown
```graph
bounds: [Xmin, Ymax, Xmax, Ymin]
width: 640
height: 300
elements: [
    {type: functiongraph, def: [f:sin(x)/x, -8.4, 8.4], att: {strokeColor: blue, strokeWidth: 2.2}},
    {type: text, def: [0, 1.22, '$\\lim_{x\\to 0}\\frac{\\sin x}{x}=1$'], att: {anchorX: middle, fontSize: 13}}
]
```
````

## When to use this skill

- A note needs a plotted math/science figure (function curves, discontinuities, tangents, Riemann sums, inequalities, etc.).
- Existing static image embeds (`![[...png]]`) about math should become interactive plots.

The result is one or more `graph` code blocks placed where the figure belongs in the note. Prefer this over raster images whenever the figure is a graph.

## Workflow

1. **Understand what the figure must show** from the user request and the surrounding note text (curves, markers, annotations, axes ranges).
2. **Design the plot** as a `graph` block:
   - Pick `bounds: [x_min, y_max, x_max, y_min]` so the figure fits (this is LEFT, TOP, RIGHT, BOTTOM order).
   - Optionally set `width` / `height` per block.
   - List `elements` in draw order (later elements render on top).
3. **Validate** every block's YAML before writing into the note (run the bundled validator or `python3 -c "import yaml,sys; yaml.safe_load(open(sys.argv[1]))"`).
4. **Insert** the block into the note where the figure belongs (`\n\n```graph ...\n```\n`, blank line before/after). If one figure deserves multiple views (e.g. 3 discontinuity cases), split it into multiple `graph` blocks.
5. **Verify rendering** if practical: load the actual plugin bundle (`<vault>/.obsidian/plugins/graphs/main.js`) in a headless Chromium harness (see references/verification.md) and screenshot each board. At minimum, confirm YAML parses.

## Syntax essentials

- **Function expression**: `f:sin(x)/x` or `f:(1+1/x)**x`. Use JS math: `**` for power, `exp(x)`, `log(x)`, `abs(x)`, `E` for e, `PI`, trig functions.
- **References**: elements can be referenced by index in `def`, where `e0` is the first element, `e1` the second, etc. For a slider value: `def: [f:x**2, f:e2, right, 0, 2]`; for a text computed from it: `def: [1.0, 3.95, "'n = ' + f:e3"]`.
- **Text / LaTeX**: text elements take `[x, y, 'label']`; wrap LaTeX in `$...$` and escape backslashes once (in the actual code block, `$\lim_{x\to 0}$`).
- **Points**: `face: 'o'` = hollow (missing point), `face: circle` = filled; `fillColor` + `strokeColor` + `size` control appearance.
- **Lines/dashes**: `strokeColor`, `strokeWidth`, `dash: 1|2|3` (dash pattern); `segment` is bounded, `line` is a full line.
- **Special elements**: `integral` fills area under curve; `slider` adds an interactive slider; `riemannsum` draws rectangles; `arrow` draws arrows (usable for dx/dy/Δy labels).

Full element/attribute catalog and many working examples: see `references/syntax.md`.

## Hard-won gotchas

- **Bounds order is [x_min, y_max, x_max, y_min]** — write `[-0.6, 3.6, 9.6, -0.2]`, not `[xmin, xmax, ymin, ymax]`.
- **No apostrophes in unquoted YAML strings**: `f'(x)` breaks the flow mapping. Use `f^\prime`/`f^{\prime}` (i.e. `$f^\prime(x)$`) instead of `$f'(x)$`.
- **`$` inside text**: it's fine, but double-check the YAML quoting — the examples in this skill use single-quoted strings.
- **Don't rely on default axes** for the classic "axes through origin" textbook look: `axis: false` and draw your own `arrow`/`segment` axes, or set `defaultAxes` positions. Default axes are the standard position (left/bottom).
- **Oscillating functions** need many sample points: `att: {numberPoints: 4000}` for e.g. `sin(1/x)`.
- **Validate numbers**: compute helper points (tangent endpoints, MVT secant coordinates) in Python and hard-code decimals so curves/lines intersect exactly.

## References

- `references/syntax.md` — element types, attributes, and annotated working examples.
- `references/verification.md` — headless Chromium harness that renders blocks with the real plugin bundle.
- `scripts/validate_graphs.py` — extract and YAML-validate all `graph` blocks in a note.
