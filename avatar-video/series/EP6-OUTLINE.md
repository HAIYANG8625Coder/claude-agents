# Episode 6 outline: plans and task lists (draft, waiting for approval)

Format: article-explainer, landscape, about 5.5 min (about 2,000 Chinese characters), same look as ep5. Series tag "从零做 Agent 第 6 集".

Cover: 标题「Agent 做长任务：先计划，再打勾」 / 副标题：只读的计划模式，加一张会打勾的任务清单

0 开场: One real number from our runs (filled after the runs): e.g. "不给清单，Agent 三次里有 N 次说做完了，其实漏了一步。" Then the two tools in the episode: plan mode and the task list.
1 为什么长任务会出事: the model forgets steps and declares victory early (EH quote: "declares victory on the entire project too early"); the plan lives only in its head.
2 计划模式（Claude Code）: Shift+Tab, /plan; reads and explores but does not edit until you approve; ExitPlanMode shows the plan; the three choices; Ctrl+G to edit the plan.
3 我们怎么做计划模式: only read-only tools plus submit_plan; write tools are not offered, and refused if called; approval switches mode. Diagram: two tool sets.
4 任务清单（Claude Code）: TaskCreate/Get/List/Update, Ctrl+T, pending / in progress / complete, survives compaction.
5 我们的 todo_write: one tool, three statuses, one in_progress at a time, the list shown every turn. Diagram.
6 真实测试: same multi-step edit task in a sandbox, with tests that pass or fail; without vs task list vs plan + list; 3 runs each, DeepSeek. Table of turns, steps missed, false "done".
7 两个坑: plans never checked off (the model plans, then forgets to update); tasks too big to verify ("fix everything" cannot be checked). Rule: each task has a check you can run.
8 合起来: four takeaways. Next: ep 7 subagents.
9 结尾: question for comments.

Honesty rules (from ep5): only claim what the runs show; say so when a setup never triggered; docs facts marked as docs, our own design marked as ours; the task fields in Claude Code are not documented, so ours are our own.

Open choice for you: the test task. My suggestion: a sandbox project where one request needs 6 separate edits across 4 files (rename a function everywhere, update the docs, add a test, bump a version, and so on), and a test script checks every edit. Pass = all 6 done.
