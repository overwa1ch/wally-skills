# Wally Skills

Wally 是一套面向 AI 视频生产的模块化 Codex skills。用户说“wally”后，`wally-helper` 会加载 Wally 助手身份，记录和应用跨模块制作经验，整理材料、判断下一步并组装最终视频提示词。它知道每个专业 skill 的用途，但不能替用户调用；专业工作必须由用户明确调用对应 skill。

## 当前模块

| Skill | 当前版本 | 职责 |
| --- | --- | --- |
| `wally-helper` | V4.1 | Wally 用法与经验层；管理视觉测试状态，把专业修改交回对应 specialist，并以单一当前生成范围的 bindings v2 验证 Route A/B 合同和组装最终视频提示词；需要时原样返回固定的 BGM 制作请求。 |
| `wally-screenplay-writer` | V2.0 | 定义并保存作品定义，按概念超短片、叙事短片、长片、剧集四种格式创作，并负责故事、人物、结构、场景拆解、原创 / 改写对白和剧本诊断。 |
| `wally-storyboard-designer` | V3.17 | 测试层：继承上游作品定义与剧本已有场景结构，以源场景标题或编号为分镜脚本权威，按需交付场景布局 SVG、分镜脚本和固定故事板 / 分镜表提示词；内置 ChatGPT Web 视觉测试流程与可复用脚本，负责机械分页、原生图片证据、规则网格切割、顺序重组和审查 PDF。故事板使用 3×3，分镜表使用 2×2 与场景资产底座；每次生图只生成一个独立版本。 |
| `wally-static-asset-designer` | V2.9 | 内置 Browser 建立命名的 ChatGPT 项目，每项资产独立聊天；Preview 至少 8 套不同风格提示词与图像，各项资产至少 4 套不同提示词与图像，逐版生成供用户选择，并继承已选全局效果。 |
| `wally-action-designer` | V3.21 | 按任务自适应设计动作、摄影、光影、声音和已批准台词的表演执行，并审查生成视频；入口只保留路由，具体合同与制作方法按需读取。 |
| `wally-visual-style-extractor` | V1.6 | 检索既有风格并提取有证据的 style layer，不代做资产、镜头、动作或最终提示词。 |

## 安装

```bash
git clone https://github.com/overwa1ch/wally-skills.git
mkdir -p /path/to/repository/.agents/skills
cp -R wally-skills/wally-* /path/to/repository/.agents/skills/
```

在该 repository 内新建 Codex 任务，让 Codex 只在这个项目作用域发现这些 skills。Wally 不再推荐安装到全局 user skill 目录。

只有 `wally-helper` 采用显式 Wally 触发边界：用户明确说 `wally`、提到 Wally 系列 / 管线或点名某个 `wally-*` skill 时，Helper 才会加载助手身份。它会说明五个专业 skill 的用途；需要专业工作时，它只推荐 skill 并给出可复制的调用请求，由用户明确调用。其余五个专业 skill 按对应专业意图正常触发，不要求用户先说 `wally`。

## 输出结构

- 专业产物保留所属 skill 的模板或输出合同结构。
- `wally-screenplay-writer` 在专业产物前保存六字段作品定义；按 1–3 分钟概念超短片、5–10 分钟叙事短片、约 90 分钟长片、多集剧集四种方法路由，实际体量可在所选方法内明确缩放，不建立第五条路线。已有材料从当前可用阶段和用户指定范围继续，定向改写不被无关的格式追问阻塞。1–3 分钟完整人物 / 事件叙事或 3–5 分钟叙事需要先确认是改造成概念超短片，还是扩展为 5–10 分钟叙事短片。
- `wally-storyboard-designer` 是测试层：继承上游作品定义与剧本已有场景结构，保留源场景标题或编号，不再创建另一层故事分段；它设计分镜脚本并给出固定故事板 / 分镜表提示词供用户快速看图测试，只交付用户点名的功能，不做视觉优化改写和回图审查，跨模块流程判断和最终批准状态由 `wally-helper` 管理。
- `wally-static-asset-designer` 以用户提供的参考图承载已清楚可见的规格；正式提示词保留字段名和相对顺序，不显示数字或字母序号，只补目标变化、布局、身份锚点与真实漂移风险。
- `wally-static-asset-designer` 为一个已批准基础 Pxx 的单一关键改变态提供 `Pxx-state`；场景覆盖默认九宫格，九格一致性不足或用户明确要求时可改用 `2×2` 四宫格。
- `wally-action-designer` 只写当前任务中承担独立控制作用的字段；连续动作使用 `Action`，精确单镜使用 `Action + Timing/beats`，多镜头或已有镜头权威使用 Shot。Shot 保留全片时间标题，内部直接使用从 `0.0s` 起算的 `0.2-0.6s: 动作描述` 时间码行，不添加 `Action:` 或 `beat N` 包装；正向不变量与独立失败风险统一进入一个 `Constraints` 字段。
- Camera 和 Shot 只按任务需要选择 capture physics、光学、稳定性、运动动机、剪辑语法、视点、前景、焦点、空间层次与时长预算；这些控制不得覆盖已批准的镜头权威。
- 原创或改写对白属于 `wally-screenplay-writer`；`wally-action-designer` 只保留已批准措辞并设计其表演、口型、停顿、声音与镜头内执行。
- `wally-visual-style-extractor` 按请求选择 Style Lookup、Analysis Card、Three-Stage Brief、Reusable JSON Prompt 或 Transfer Validation；`subject`、`scene`、`camera` 只接受用户已有值或复用占位符。
- `wally-helper` 同时消费旧版固定导演正文和新版弹性导演正文；每次组装只处理一个当前生成范围，bindings v2 只记录该范围实际使用的资产，不再保存额外的范围字段。Route A 保留外层 `Reference List`，Route B 保留外层 `Asset List / Prompt / Constraints`，两条路线均可用确定性脚本验证。
- 未明确提供音乐时，每段导演正文默认使用无BGM的完整环境声与 SFX；明确提供音乐或要求绝对静音时按该声音状态执行。导演正文不写 `Reference:` 或平台绑定。

## 新手使用方式

直接说“wally”，然后描述想做的视频，或上传任意已有材料。Helper 会整理信息、判断下一步，并给出对应 skill 名称和可以直接复制的调用请求；用户复制请求并明确调用该 skill，再把产物带回 Wally。

## 当前推荐经验

1. `wally-screenplay-writer` 完成可用的剧本初稿。
2. `wally-storyboard-designer` 按剧本原有场景逐场制作简单故事板草稿，低成本测试景别、运镜、动作和镜头顺序；故事问题交回 Screenplay，镜头问题交回 Storyboard，Helper 记录测试与批准状态。
3. `wally-static-asset-designer` 先生成符合剧本整体调性的 Preview 候选，由用户选择全局效果；再生成各项资产候选，由用户逐项选定。场景九宫格一致性不足时，建议用户选择 `2×2` 四宫格。
4. `wally-storyboard-designer` 用导演脚本和已批准静态资产生成分镜表：导演脚本是分镜的唯一依据，静态资产是视觉效果的唯一依据；用户通过多版分镜表复核镜头序列。
5. `wally-action-designer` 设计动作、表演、摄影、光影和声音执行。
6. `wally-helper` 检查产物兼容性并完成最终组装。

`wally-helper` 从开始到结束持续陪同；上面的顺序是当前经验建议，不是专业 skill 的调用前提。`wally-visual-style-extractor` 可在任何需要锁定或复核视觉风格的阶段按需使用。实际顺序以当前材料和交付目标为准。

## 健康检查

仓库的 `validate-wally-skills` GitHub Actions job 会检查六项 frontmatter、引用完整性、跨模块合同、匿名 Route fixtures、公开安全和冻结提示词 hash。也可在本地运行：

```bash
python -m pip install Pillow reportlab
python scripts/validate_wally_skills.py --skills-root .
python -m unittest discover -s wally-helper/tests -p 'test_*.py' -v
python -m unittest discover -s tests -p 'test_*.py' -v
python -m unittest discover -s wally-storyboard-designer/tests -p 'test_*.py' -v
```

## 仓库迁移

原独立仓库已分别更名为 `overwa1ch/deco-helper-deprecated` 和 `overwa1ch/deco-helper-storyboard-deprecated`，并转为 Private，从公开列表隐藏。它们只保留历史内容，不再作为当前版本来源。本仓库是 Wally 系列唯一公开的主发布仓库。

这里的 `wally-helper/` 仍是 Wally 系列中的有效协调模块；废弃并隐藏的是原先单独发布它的旧 GitHub 仓库。

## License

[MIT](LICENSE)
