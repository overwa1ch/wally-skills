---
name: wally-storyboard-designer
description: Use only when explicitly requested by name. 按需设计或修订分镜脚本、制作或修订白模视频、绘制场景布局及检查提示词污染；直接使用当前材料，只交付用户指定的产物。
---

# Wally Storyboard Designer

Provide on-demand storyboard-domain functions for the user's supplied story, scene, or shot material.
分镜脚本、白模视频、场景布局与提示词检查可分别取用；只交付本次指定产物，不自动接续其他功能。

Current version: `wally-storyboard-designer@2026-10-24-v4.1-on-demand-tools`

## 共用规则

- Accept scene-divided scripts, tables, images, videos, partial artifacts, conflicting drafts, existing director scripts or performance designs, or any mixture. 输入和交付形式不固定；只处理当前要求，不为执行工具重写材料。
- 按源稿已有场景组织工作，保留原场景名称、顺序及镜号。
- Preserve the latest explicit or approved `作品定义` as source authority. 保留适用的全局风格、灯光、音效、台词、参考绑定和前后衔接；无依据的内容不补写。
- 已有导演脚本或表演设计可直接作为镜头依据，无需转换格式或重写。
- 用户审查白模画面与分镜意图，Agent 核对文件、镜号和交付完整性，按用户反馈定向修订。
- 原创剧本、图片资产制作、具体表演与声音设计、最终视频生成提示词分别由对应专业 skill 处理；本 skill 保留并传递已有内容。

## 按任务读取

只读取当前任务对应的入口。历史版本、脚本实现和测试无需默认加载。

| 当前任务 | 读取入口与交付范围 |
| --- | --- |
| 分镜脚本或定向修订 | [导演脚本合同](references/director-script-output-contract.md)。 |
| 制作白模视频 | 按下方[白模视频](#白模视频)制作或修订。 |
| 新建场景布局 SVG | 用户明确发起时读 [场景布局规则](references/scene-layout-svg-rules.md)。 |
| 提示词污染检查 | 用户明确要求时读 [污染检查](references/pollution-check.md)。 |

## 白模视频

- 按用户指定的分镜或已有镜头材料制作白模视频，表达大致的人物位移、空间关系、构图和运镜，交付用户观看。
- 白模定义与造型约定沿用 `wally-asset-designer`；具体表演由视频模型在该框架内补全。
- 已有白模可直接使用；用户观看后，按反馈修订对应分镜或白模。
