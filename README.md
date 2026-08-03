# Wally Skills

Wally 是一套面向 AI 视频生产的模块化 Codex skills。用户说“wally”后，`wally-helper` 会加载 Wally 助手身份，记录和应用跨模块制作经验，整理材料、判断下一步并组装最终视频提示词。它知道每个专业 skill 的用途，但不能替用户调用；专业工作必须由用户明确调用对应 skill。

## 当前模块

| Skill | 当前版本 | 职责 |
| --- | --- | --- |
| `wally-helper` | V3.12 | Wally 用法与经验层；管理视觉测试状态，把专业修改交回对应 specialist，验证 Route A/B 合同并组装最终视频提示词。 |
| `wally-screenplay-writer` | V1.7 | 定义作品形态，创作概念或叙事超短片至长片 / 剧集，并负责故事、人物、结构、原创对白和诊断。 |
| `wally-storyboard-designer` | V1.19 | 继承上游作品定义，按需交付 SEG、场景布局、导演脚本、分镜设计、固定提示词和 returned-board 审查。 |
| `wally-static-asset-designer` | V2.6 | 静态资产规划、Preview、Pxx-state、九宫格 / 2×2 场景参考、生产提示词与成图审查。 |
| `wally-action-designer` | V3.8 | 按任务设计动作、摄影、光影、声音和已批准台词的表演执行，并审查生成视频。 |
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
- `wally-screenplay-writer` 在专业产物前保存明确的作品定义；1–3 分钟完整叙事使用压缩的叙事超短片规则，不强制完整 Want / Need / Arc。
- `wally-storyboard-designer` 继承上游作品定义并只交付用户点名的分镜专业功能；跨模块流程判断和最终批准状态由 `wally-helper` 管理。
- `wally-static-asset-designer` 以用户提供的参考图承载已清楚可见的规格；正式提示词保留字段名和相对顺序，不显示数字或字母序号，只补目标变化、布局、身份锚点与真实漂移风险。
- `wally-static-asset-designer` 为一个已批准基础 Pxx 的单一关键改变态提供 `Pxx-state`；场景覆盖默认九宫格，九格一致性不足或用户明确要求时可改用 `2×2` 四宫格。
- `wally-action-designer` 只写当前任务中承担独立控制作用的字段；连续动作使用 `Action`，精确单镜使用 `Action + Timing/beats`，多镜头或已有镜头权威使用 Shot。Shot 保留全片时间标题，内部直接使用从 `0.0s` 起算的 `0.2-0.6s: 动作描述` 时间码行，不添加 `Action:` 或 `beat N` 包装；正向不变量与独立失败风险统一进入一个 `Constraints` 字段。
- 原创或改写对白属于 `wally-screenplay-writer`；`wally-action-designer` 只保留已批准措辞并设计其表演、口型、停顿、声音与镜头内执行。
- `wally-visual-style-extractor` 按请求选择 Style Lookup、Analysis Card、Three-Stage Brief、Reusable JSON Prompt 或 Transfer Validation；`subject`、`scene`、`camera` 只接受用户已有值或复用占位符。
- `wally-helper` 同时消费旧版固定导演正文和新版弹性导演正文；Route A 保留外层 `Reference List`，Route B 保留外层 `Asset List / Prompt / Constraints`，两条路线均可用确定性脚本验证。
- 未明确提供音乐时，每段导演正文默认使用无BGM的完整环境声与 SFX；明确提供音乐或要求绝对静音时按该声音状态执行。导演正文不写 `Reference:` 或平台绑定。

## 新手使用方式

直接说“wally”，然后描述想做的视频，或上传任意已有材料。Helper 会整理信息、判断下一步，并给出对应 skill 名称和可以直接复制的调用请求；用户复制请求并明确调用该 skill，再把产物带回 Wally。

## 当前推荐经验

1. `wally-screenplay-writer` 完成可用的剧本初稿。
2. `wally-storyboard-designer` 用简单故事板草稿低成本测试景别、运镜、动作和镜头顺序；故事问题交回 Screenplay，镜头问题交回 Storyboard，Helper 记录测试与批准状态。
3. `wally-static-asset-designer` 准备并批准可复用静态资产；场景九宫格一致性不足时，优先改用 `2×2` 四宫格。
4. `wally-storyboard-designer` 用修改后的剧本和已批准资产生成分镜表，复核完整序列的剧情覆盖、节奏、连续性和可拍性。
5. `wally-action-designer` 设计动作、表演、摄影、光影和声音执行。
6. `wally-helper` 检查产物兼容性并完成最终组装。

`wally-helper` 从开始到结束持续陪同；上面的顺序是当前经验建议，不是专业 skill 的调用前提。`wally-visual-style-extractor` 可在任何需要锁定或复核视觉风格的阶段按需使用。实际顺序以当前材料和交付目标为准。

## 健康检查

仓库的 `validate-wally-skills` GitHub Actions job 会检查六项 frontmatter、引用完整性、跨模块合同、匿名 Route fixtures、公开安全和冻结提示词 hash。也可在本地运行：

```bash
python scripts/validate_wally_skills.py --skills-root .
python -m unittest discover -s wally-helper/tests -p 'test_*.py' -v
python -m unittest discover -s tests -p 'test_*.py' -v
```

## 仓库迁移

原独立仓库已分别更名为 `overwa1ch/deco-helper-deprecated` 和 `overwa1ch/deco-helper-storyboard-deprecated`，并转为 Private，从公开列表隐藏。它们只保留历史内容，不再作为当前版本来源。本仓库是 Wally 系列唯一公开的主发布仓库。

这里的 `wally-helper/` 仍是 Wally 系列中的有效协调模块；废弃并隐藏的是原先单独发布它的旧 GitHub 仓库。

## License

[MIT](LICENSE)
