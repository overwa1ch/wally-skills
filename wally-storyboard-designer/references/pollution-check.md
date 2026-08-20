# Prompt Pollution Check

提示词污染：画面内容写得过度详细时，绘图模型会试图把每个词都塞进画面，取平均值去容纳所有提示词，画面平庸、怪异。例：特写却写了裤子、鞋子等全身细节，模型会试图把全身画出来。

Run this check only when the user asks for it. A 分镜脚本 delivery or revision never triggers it by itself.

The checker must stand where the image model stands: it sees only the shot text, with no story and no intent. The agent that wrote the 分镜脚本 must never check or grade its own text — it knows why each word is there and will judge the intent, not the words.

## Dispatch

- Send the checker only the check instructions and the shot blocks, verbatim (heading + 拍摄手法 + 画面内容 + 任务 per shot).
- Never send the source screenplay, 作品定义, scene summaries, assets, or any prior conversation.
- Use an isolated subagent when the environment provides one; otherwise hand the user the copy-ready prompt below to run in a fresh chat, and wait for the report.

## Check, per shot independently

1. 越框: can every visible noun in 画面内容 be drawn inside the crop that 拍摄手法 declares? List every word that cannot.
2. 过密: which named elements inside the crop do not serve the 任务 sentence and would split the frame's attention? List them.

## Report

Per shot: `干净`, or the words to delete plus one short reason. Deletion suggestions only; never rewrite, add, or judge story, coverage, or shot choice.

## Apply

The writer applies the report through targeted revision (only the named shots); re-check revised shots on request.

## Copy-ready checker prompt

```text
你是提示词污染检查员，只看下面的分镜文字，不知道剧情和意图（这正是绘图模型的处境）。
逐镜独立检查两件事：
1. 越框：按"拍摄手法"里的景别，判断"画面内容"里每个可见名词能否画进这个取景框；列出画不进的词。
2. 过密：按"任务"那一句，列出取景框内与该任务无关、会分走画面注意力的词。
每镜输出：镜号 + 干净 / 应删的词 + 一句原因。只建议删词，不改写、不新增、不评价故事和镜头选择。

[粘贴分镜脚本的镜头块]
```
