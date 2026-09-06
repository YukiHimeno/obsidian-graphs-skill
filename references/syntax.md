# Graphs plugin syntax reference

Obsidian Graphs plugin: `obsidian://show-plugin?id=graphs`. Source: DylanHojnoski/obsidian-graphs, wiki: dylanhojnoski.github.io/obsidian-graphs-wiki/.

## Top-level fields

```yaml
bounds: [x_min, y_max, x_max, y_min]   # order: left, top, right, bottom
width: 640        # optional pixel width
height: 300       # optional pixel height
axis: true|false  # default axes on/off (default true)
elements: [ ... ] # list of element objects, drawn in order
```

`elements` entries look like:

```yaml
{type: <type>, def: [<definition>], att: {<attributes>}}
```

`att` is optional and maps to JSXGraph attributes (`strokeColor`, `strokeWidth`, `fillColor`, `fillOpacity`, `dash`, `size`, `face`, `fontSize`, `anchorX`, `name`, `numberPoints`, ...).

## Element types (in the figures skill)

### functiongraph — plot y = f(x)

```graph
bounds: [-8.4, 1.4, 8.4, -0.6]
elements: [
    {type: functiongraph, def: [f:sin(x)/x, -8.4, 8.4], att: {strokeColor: blue, strokeWidth: 2.2}},
    {type: functiongraph, def: [f:exp(x), -3.0, 2.2], att: {strokeColor: blue, strokeWidth: 2.2, numberPoints: 400}}
]
```

- `def: [f:<expr>, x_min, x_max]` — domain is explicit.
- Use JS expressions: `x**2`, `(1+1/x)**x`, `sin(x)`, `cos(x)`, `tan(x)`, `log(x)` (natural log), `exp(x)`, `abs(x)`, `E`, `PI`.
- `numberPoints` raises sampling density (e.g. 4000 for oscillation).

### segment — bounded straight segment

```graph
elements: [
    {type: segment, def: [[-8.4, 1], [8.4, 1]], att: {strokeColor: gray, strokeWidth: 1, dash: 3}},
    {type: segment, def: [[0.2, 0.64], [1.8, 0.64]], att: {strokeColor: red, strokeWidth: 1.8, dash: 3}}
]
```

### line — infinite straight line (through two points)

```graph
elements: [
    {type: line, def: [[-0.5, -3.1725], [3.0, 6.2775]], att: {strokeColor: green, strokeWidth: 1.8, dash: 1}}
]
```

### point — marker

```graph
elements: [
    {type: point, def: [0, 1], att: {face: 'o', size: 4, strokeColor: blue}},       # hollow
    {type: point, def: [1, 2], att: {face: circle, size: 3, fillColor: blue, strokeColor: blue}}  # filled
]
```

- `face: 'o'` renders a hollow point (missing/undefined value).
- `face: circle` renders a filled disc; `fillColor` + `strokeColor` + `size` control it.

### text — annotation (supports LaTeX with `$...$`)

```graph
elements: [
    {type: text, def: [0, 1.22, '$\lim_{x\to 0}\frac{\sin x}{x}=1$'], att: {anchorX: middle, fontSize: 13}},
    {type: text, def: [1.1, 0.78, 'x=0 处无定义（空心点）'], att: {fontSize: 9, strokeColor: gray}}
]
```

- Plain text and inline LaTeX can be mixed in one string.
- Avoid apostrophes in the string when the YAML is flow-style (see gotchas in SKILL.md).
- `anchorX: middle` centers at x; otherwise left-anchored.

### arrow — directed arrow (good for dx/dy/Δy etc.)

```graph
elements: [
    {type: arrow, def: [[0.7, 0.7], [1.25, 0.7]], att: {strokeColor: contrast, strokeWidth: 1.2}},
    {type: arrow, def: [[1.24, 0.814333], [1.24, 1.633833]], att: {strokeColor: green, strokeWidth: 1.1}}
]
```

### integral — area under the curve

```graph
elements: [
    {type: functiongraph, def: [f:x**2, 0, 2], att: {strokeColor: contrast, strokeWidth: 2.2}},
    {type: integral, def: [[0, 2], e0], att: {fillColor: blue, fillOpacity: 0.13}}
]
```

- `def: [[a, b], <curve-elem>]` — second entry references the functiongraph element (here `e0`).

### slider — interactive parameter

```graph
elements: [
    {type: slider, def: [[1.2, 4.32], [2.4, 4.32], [2, 8, 24]], att: {name: n}}
]
```

- `def: [[x1,y1],[x2,y2],[min, max, initial]]`.

### riemannsum — Riemann rectangles (left/right/middle)

```graph
elements: [
    {type: functiongraph, def: [f:x**2, 0, 2], att: {strokeColor: contrast, strokeWidth: 2.2}},
    {type: slider, def: [[1.2, 4.32], [2.4, 4.32], [2, 8, 24]], att: {name: n}},
    {type: riemannsum, def: [f:x**2, f:e2, right, 0, 2], att: {fillColor: gray, fillOpacity: 0.06, strokeColor: gray, strokeWidth: 1}},
    {type: text, def: [1.0, 3.95, "'n = ' + f:e3"], att: {anchorX: middle, fontSize: 10.5}}
]
```

- `def: [f:<expr>, f:<slider-elem> or end, left|right|middle, x_min, x_max]`.
- `f:e2` references the slider element; the text `'n = ' + f:e3` reads the slider value.

## Other types available

Derived from plugin source `Types` enum: `circle`, `ellipse`, `parabola`, `polygon`, `polygonalchain`, `regularPolygon`, `circumcircle`, `circumcenter`, `circumcirclearc`, `incenter`, `sector`, `semicircle`, `curve`, `curveparametric`, `curvedifference`, `curveintersection`, `curveunion`, `derivative`, `tangent`, `parallel`, `perpendicular`, `intersection`, `inequality`, `slopefield`, `slopetriangle`, `stepfunction`, `glider`, `tapemeasure`, `boxplot`, `chart`, plus 3D types (`functiongraph3d`, `curve3d`, etc.). For plotting figures the essentials above are enough.
