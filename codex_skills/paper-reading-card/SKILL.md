---
name: paper-reading-card
description: Use when reading a paper, blog, essay, or technical note and turning it into a compact card focused on problem, method, result, interpretation, claim, relation to the active project, and whether it changes the mainline.
metadata:
  short-description: Write paper and blog reading cards
---

# Paper Reading Card

Create a compact first-pass reading card. Do not summarize the whole paper section by section unless asked.

## Repo Templates

Use these templates when working inside the research workspace:

- `paper_reading/_templates/summary_card.md`: shortest first-pass card
- `paper_reading/_templates/paper_reading_record.md`: full paper reading process record
- `paper_reading/_templates/blog_reading_record.md`: blog / essay reading process record

## Required Output

```markdown
# Reading Card

论文标题：

我为什么读它：

核心问题：

作者方法：

关键结果：

作者解释：

我的判断：

和我研究的关系：

以后是否需要精读：是/否

## Mainline Update Check
```

## Rules

- Separate what the authors claim from your own judgment.
- State whether the reading changes the mainline, creates a risk, or is only background.
- If it should be filed, recommend one `paper_reading/` category.
- Keep the card concise.
- When writing Markdown research documents, inline formulas must use `$...$` and display formulas must use `$$...$$`.
