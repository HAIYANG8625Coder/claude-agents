# Article and paper deep-dive videos (长视频精读)

Learned on 2026-11-15 from a Xiaohongshu AI-knowledge creator (Silicon Valley algorithm engineer, ~1K followers but 4K likes on one Stanford-course video). Studied two of their videos frame by frame: "Anthropic 最新文章：拆解 Always-on Agent" (7 min 18 s) and "斯坦福论文：8分钟读懂Multi-Agent" (6 min 5 s). Used by the `article-explainer` skill and style preset H in `DESIGN.md`. We copy the method, never their content, cover text or face.

## What their videos are
- **16:9, 1280×720, 6–8 min.** A long read of ONE source (a company engineering article, or 2–3 papers on one question), not a 60 s short.
- **An HTML slide deck, screen-recorded.** A cream page that advances slide by slide while they talk; the mouse cursor sits still on screen the whole time, which gives away a browser recording. We render the same kind of deck with HyperFrames instead (sharper, no cursor, timed to the words).
- **Their own voice, natural pace, Chinese with English terms kept** (Agent, worker, token, run). Their face in a small circle bottom-right at the opening and the ending only.

## The layout (every slide)
1. **Chapter bar on top:** `01 一次 run · 02 收件箱 · … · 合起来`, or `01 定义 · 02 设计 · 03 对齐 · 04 验收 · 05 怎么搭 · 结尾`. The current chapter is bold with a red underline, so viewers always know where they are in a 7-minute video.
2. **Section tag:** a solid crimson block `02 事件收件箱` at the top left when a chapter starts.
3. **The source itself on screen:** the article's own figure, a paragraph of the original English on a white card, or the paper's first page tilted slightly. It proves "this is what the source says".
4. **The rebuilt version next to it, in Chinese:** the same idea redrawn as boxes and arrows, a mock data table, a clock, a code diff with the one changed value boxed in red, or two big bars (blue = before / one agent, crimson = after / many agents) with the numbers in a big serif.
5. **A source line on every slide**, small and grey: `原文：Anthropic《Building always-on agents》· William Hu · 2026-11-13`, `斯坦福 CooperBench（arXiv 2601.13295）附录 C 表 5：GPT-5，315/652 → 183/652`, `同上 图 2（第 11 页）`. When a picture is their own inference, they say so: `示意`, `每日简报的流程是示意，按原文规则推演`, `五条为本片归纳，均出自原文`.
6. **Caption band:** a pale full-width band near the bottom, one short clause at a time, bold serif.

## The structure
- **Cover = frame 0.** A separate, louder design: green gradient, a series tag (`工程解读 | 04`), a date badge (`11.13 最新发布`) for news-fresh sources, the title on two lines, a one-line subtitle in a white strip (`大部分时间在睡觉的 Agent`), one pill per chapter with an icon, and their photo in a circle.
- **Opening:** the most surprising number or line from the source, with the source's first page beside it (`48% → 28%: 两个 Agent 合作写代码，成功率比一个还低`).
- **Chapters:** one per part of the source (the article's five primitives; the papers' three failure types). Each chapter = original figure/quote → rebuilt Chinese picture → the one sentence to remember.
- **合起来:** a recap table, one row per chapter (`02 事件收件箱 | 事件先落表，同一时间只让一个 worker 处理`), the last row highlighted.
- **Ending:** a `留个问题` card with one question (`设计 · 对齐 · 验收，这三件事里，哪件最难做到？`), and the same question in the note's last line.

## The note text (desc)
- Opens with the date and source and one plain sentence of what it's about.
- States the surprising point (`文章最反直觉的一点：…`).
- One bullet per chapter, each with its concrete rule or number.
- **几点说明**: what the source does and doesn't show (`文章里唯一的数字是…，没有测这套架构本身的效果`) and which parts are their own inference.
- A question for the comments, then 6–7 topics (`#Agent #Anthropic #Claude #AI工程 #大模型 #人工智能`).

## Why it works
- Trust: the original is always on screen and every number has a page or table reference.
- Saves: the recap table and the clear chapters make it a reference people come back to (their top video is a Stanford homework walkthrough with 4K likes).
- Honesty lines (`示意`, `几点说明`) cost nothing and stop "you made that up" comments.
