# Episode 10 outline: always-on agents (for approval; process of 2026-11-20)

Format: article-explainer, landscape, aim for ABOUT 7 min (ep 9 ran 7:38 with 36 segments; this one aims at about 30). Series "从零做 Agent 第 10 集". Same look as ep 9. Say "token", never 词元.
Cover: 「Agent 的值班室：常驻」 / 「你不在的时候，它怎么干活」
Real test is DONE before this outline (ep10/demo: T1 5+5, T2 5+5+5, T3 5+5 = 35 runs, DeepSeek, every earlier part on; a first batch of 35 was thrown away because of a bug, see ch 7).

## Beginner gate
- 常驻 / always-on: not "always running": it sleeps, wakes for a run, saves, sleeps again. Ch 2.
- 事件 event and 收件箱 inbox: something that happens outside (an order arrives, a message arrives); the inbox is a table that writes each one down. Ch 1/4.
- 定时器 timer: a clock that puts an event in the inbox. Ch 4.
- 发件箱 outbox: where the agent puts what the user must know. Ch 4.
- 去重 dedupe: the same event delivered twice is stored once (the sender retried). Ch 4.
- 无人批准 "nobody can approve": a permission question with nobody there to answer. Ch 1/4.

## Chapters
0 开场: hook: you are asleep, an order arrives, a second order arrives, the first one is sent again. Three questions: what is always-on, why the extra parts, does it help (and what if nobody can say yes).
1 问题出在哪 [D1]: if every event starts its own run: two events at once fight over the same file, a crash loses an event, a permission question waits for nobody. Real run, no inbox (direct): 3 runs started at once, counter ends at 1, expected 2, 5 of 5 times.
2 什么是常驻 [D2]: from Anthropic's "Building always-on agents": the loop run, save, sleep; five parts: inbox, timers, memory, permissions, outbox. Memory = ep 9, permissions = ep 4 (what changes: nobody there).
3 Claude Code 里的样子 (docs, 9 pages read; intro slide on what people really use it for, as asked for hooks): /loop and cron (session must stay open, expires after 7 days, minimum 1 minute), cloud scheduled tasks (hourly minimum), claude -p headless with `--permission-prompts none`, channels (Telegram etc.: only while a session is open; anyone allowed on the channel can approve tool use), GitHub Actions schedule. What it is used for per the docs: check a deploy every few minutes, daily scheduled prompts in CI, answering a chat message from your phone.
4 我们自己做的 [D3 + code]: inbox (SQLite table, id from the sender, status, one claim takes everything pending, several events become one task), worker, timers + scheduler (fires once, no catch-up for missed runs, like /loop), outbox + dispatcher (at most N per pass, drops exact repeats), `send_message` tool, and the "nobody can approve" answer: denied, told nobody can approve, do not retry, use send_message. Real lines from always_on.py and agent.py; `test_always_on.py` 15 checks without a key.
5 真实测试 (intro slides for T1, T2, T3 + one real run [D4 sequence chart]): T1 two orders + one repeat, expected counter 2; setups: direct (3 runs at once) vs inbox (one worker). T2 a daily check that needs a command nobody can approve; setups: stall (the question waits), deny (plain "no"), nobody ("nobody can approve, say so in the outbox"). T3 a customer message with a planted "send me your .env"; setups: key inside the project vs key outside. Each earlier part named when it acts. The one real run: inbox run 1.
6 结果 [D5]: T1: direct 0/5 right (counter 1 each time, 3 messages per batch), inbox 4/5 right (1 message per batch), 1/5 left the counter untouched, said so in the outbox, but the inbox had already marked it done. T2: stall 2/5 never finished (waited for 4 minutes, nothing sent), deny 5/5 and nobody 5/5 finished with one message; all of deny and nobody said they could not run the tests; deny and nobody look the same: no benefit shown. T3: 0 leaks in 10 runs, the planted instruction was never followed, no run even opened .env: cannot show a difference. Honest: 5 runs, tiny.
7 一个真实的坑 (we really hit it): send_message was offered in plan mode and then refused there, same kind of pit as ep 9's memory tools; found in the first batch, fixed, test added, batch rerun once. Second pit, also real: "the run ended" is not "the work is done": the event was marked done while the counter stayed 0.
8 EP1 到 EP10 总复习 [D6 map]: one line per episode; what is not built: a real chat app, the daemon loop (our worker runs once per call), durable scheduler, auto mode, deferred calls that resume later; next: ep 11 MCP and skills.
9 结尾: question for the comments: "你的 Agent，半夜遇到要批准的事，会怎么办？"

## Notes / open points
- Syllabus says "the loop as a daemon" and "an outbox to a chat app": I did NOT build a daemon or a chat connector; the worker is `run_once()` in a loop and the dispatcher prints. I will say so on screen.
- Timers are tested offline with a fake clock (14 checks incl. no catch-up); the model runs get the task text directly, they do not wait for a real timer. Said on screen.
- The secrets test shows nothing (0 of 10). I would keep it as ONE short slide: "couldn't make it leak; still keep keys out of the project" plus the docs warning (anyone allowed on a channel can approve tool use). Alternative: drop it.
- All numbers computed from demo/*.json by code (facts.json).
