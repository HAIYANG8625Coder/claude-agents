# Episode 12 outline: testing and debugging an agent (DRAFT for approval; 2026-11-21)

Format: article-explainer, landscape, about 8 min. Series "从零做 Agent 第 12 集". Same look as ep 11. Say "token" and "skill" in English.
Cover: 「改了一行，Agent 变好了吗？」 / 「别靠一次运行下结论」
Status: research done (EP12-RESEARCH.md). The real test (the eval harness and its runs) is NOT done yet; every number on screen must come from it. The chapters below say what it must show.

## Beginner gate
- 任务 task: one test with a fixed input and a rule for success. Ch 2.
- 试验 trial: one attempt at a task. Outputs vary, so run each task several times. Ch 2/5.
- 评分器 grader: code that checks the result. We check the outcome (the file, the state), not the sentence the agent says. Ch 2/4.
- 轨迹 trace: the full saved record of one run, every message and tool call. Ch 3/4.
- pass@k and pass^k: at least one success in k tries vs all k succeed. 75% per trial gives about 42% for pass^3. Ch 5.

## Chapters
0 开场: hook: you change one line of the system prompt, run once, it works, you ship it. Was it the change, or luck? Three questions: how do you know a change helped, what do you save, what do you look at when it fails.
1 问题出在哪 [D1]: judging by one run; reading only the final answer. Show a real case from our harness: the same task, same setup, passes in one trial and fails in the next.
2 什么是评测 [D2]: task, trial, grader, trace (words from Anthropic's "Demystifying evals for AI agents", 2026-01-09). Grade the outcome, not the exact tool order. Code grader first, human reading for the rest. "20-50 simple tasks drawn from real failures is a great start"; we use 4 to stay on screen.
3 Claude Code 里的样子 (docs, read): `claude -p` with `--output-format json` (result, session ID, cost) or `stream-json`; `--max-turns` and `--max-budget-usd` as caps; `/usage` and `/context`; `--debug` with filters and `--debug-file`; `--safe-mode` (turn all customizations off: if the problem goes away, one of them caused it); `--restricted` "intended for evaluation harnesses". Transcripts are saved as JSONL, but the docs say the entry format is internal and changes. Say what the docs do NOT give: a test harness for your own tasks.
4 我们自己做的 [D3 + code]: eval.py: 4 fixed tasks, a clean temp copy of the workspace per trial, the full messages saved as JSON, a code grader on the outcome, a table of pass rate, turns and tokens per task, a flag to run one change at a time. Checks that run without a key (grader on a recorded trace, clean-copy isolation, table maths).
5 真实测试 [D4 sequence]: baseline vs ONE change, N trials per task, same model as ep 11. The change is chosen BEFORE the run and written down; candidates: the plan-mode reminder, or a shorter tool description. Show one run end to end, then the table.
6 结果 [D5]: pass rate, mean turns, mean tokens with the spread (runs vary, as in ep 11). Say whether the change helped, did nothing, or cannot be told apart at this sample size. Do not claim more than N trials show.
7 一个真实的坑 (must be one we really hit while building the harness; write it only after it happens). Candidates: a grader that passes a wrong answer, a 0% task that was a broken task, leftover files between trials.
8 EP1 到 EP12 回顾 [D6 map]: one line per episode; what is not built: LLM graders, a big task set, automatic regression runs in CI; next: ep 13, putting it together.
9 结尾: question for comments: "你改完 Agent 之后，是怎么知道它变好了的？"

## Notes / open points
- Anthropic's article does not say "do not grade only the final answer"; we say it as our own advice, not as a quote.
- Unread sources: hooks debugging, agent-sdk cost tracking, agent view. Read hooks debugging before ch 3 if hooks appear on screen.
- Pitfall slide: a 0% pass rate over many trials usually means a broken task or grader, not a weak agent.
