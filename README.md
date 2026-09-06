# obsidian-graphs-skill

> 自用存档。Obsidian Graphs 插件（`obsidian://show-plugin?id=graphs`）用的 skill，按自己机器上的用法整理，不保证通用。

这个 skill 给 Obsidian 笔记里的数学图生成 `graph` 代码块。Graphs 插件会把 ```graph 代码块渲染成交互坐标图，可以画函数曲线、间断点和切线这类常见的，黎曼和、不等式也行。笔记里需要图的地方直接插块进去，不用再贴静态图片。

## 结构

- `SKILL.md`：主文件，说明使用流程、语法要点和踩过的坑
- `references/syntax.md`：元素类型、属性和可用示例
- `references/verification.md`：无头 Chromium 渲染真实插件包做截图校验
- `scripts/validate_graphs.py`：提取并校验笔记里的 `graph` 块
- `agents/openai.yaml`：agent 元数据

## 用法

把目录放进 skills 目录，例如 `~/.agents/skills/obsidian-graphs`。需要出图时，写作 agent 按 `SKILL.md` 生成 `graph` 块，跑 `scripts/validate_graphs.py` 校验后插进笔记。

## 说明

仓库是我自用的存档，公开放着是为了自己换机器方便同步，不打算对外维护。别人要用也行，按 `SKILL.md` 里的步骤试，不保证每个例子都能跑。
