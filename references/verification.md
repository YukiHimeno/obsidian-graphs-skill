# Verifying graph blocks (headless Chromium)

The plugin's real rendering path can be executed in a headless Chromium page so each `graph` block can be screenshot and inspected without opening Obsidian.

## Ingredients

- The installed plugin bundle: `<vault>/.obsidian/plugins/graphs/main.js`
- A mock for the `obsidian` module and minimal DOM shims (`createEl`, `addClass`, ...)
- `js-yaml` and `MathJax` from a CDN (or bundled locally)
- Chromium in headless mode

## Approach

1. Build one HTML page that:
   - local/shim `window.require = (name) => name === "obsidian" ? mock : throw`.
   - loads `main.js` and captures `window.module.exports.default` (the plugin class).
   - for each source YAML: `plugin.utils.parseCodeBlock(yaml, false)` then `plugin.handleCodeBlock(yaml, boxEl, false)` into a fresh div.
2. Render with headless Chromium, then either:
   - screenshot the whole page at high DPI and crop per board, or
   - evaluate `document.title` containing counts of boards/errors after load.
3. Inspect the screenshots (or DOM) for: curves present, dashed lines, hollow/solid points, LaTeX rendered, slider visible, no error boxes.

## Reference implementation

A working harness was built previously in `/tmp/graphgen/` (`build_harness.py` -> `board.html`, `all.png`, `crops/`). Reuse that pattern; adjust the `main.js` path and the list of sources.

Key shims needed:

```js
window.MathJax = { tex: {inlineMath: [["$", "$"]], processEscapes: true}, start: {typeset: false, prompt: "none"} };
window.CodeMirror = {defineMode: function(){return {}}, getMode: function(){return {}}};
HTMLElement.prototype.createEl ||= function(tag, opts){ ... };
```

## When verification is optional

If a headless browser is unavailable, at least ensure every block parses as YAML and the element `def`s reference existing element indices (`e0`, `e1`, ...). Run `scripts/validate_graphs.py`.
