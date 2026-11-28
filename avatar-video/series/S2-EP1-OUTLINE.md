# Series 2 episode 1 outline: many users, one agent service (for approval; 2026-11-25)

Format: article-explainer, landscape, aim for 8 to 9 min. Series 「从零做企业级 Agent」第 1 集. Series 2 look (dark navy + cyan, copied from the intro project). Keep "token" and "skill" in English.
Cover: 「两个人同时用一个 Agent，A 读到了 B 的文件」 / 「多用户服务：身份、会话、一个请求一个进程」
Real test is DONE before this outline (ep01/demos.py: two users at once 5+5, another user's file 5, restart 5+5 = 25 trials on DeepSeek flash, 0 failed requests; leftover variables measured with the real SDK; 17 no-key checks in tests/test_service.py). Not committed yet. Sources: S2-EP1-RESEARCH.md.

## Beginner gate
- 服务 service: a program that keeps running and answers requests from many people. Ch 2.
- 身份 and token: a long random string that says who is asking. The server keeps only its fingerprint (hash). Ch 2/4.
- 进程 process and 线程 thread: two processes each have their own memory; threads in one process share it. Ch 2/6.
- 会话 session: one saved conversation, that belongs to one user. Ch 2/4.
- 环境变量 environment variable: a setting a program inherits from the shell that started it. Ch 7.

## Chapters
0 开场: hook: two people use the same agent. lin asks for their own project's code name. 5 times out of 5 they get sam's. (On screen: our own first version, sam asking 0.5 s after lin.) Three questions: why, how to fix it, what is still open after the fix.
1 问题出在哪 [D1]: series 1 built an agent for ONE person. Put a server in front and three things are missing: who is asking, whose folder, whose conversation.
2 概念 [D2, 3 slides]: token → user → folder → session in one picture; thread vs process (shared memory vs separate); where a session lives (a file on this disk).
3 Claude Code 里的样子 (docs, read): "One agent session maps to one subprocess"; each session its own working folder; check identity in front of the agent, not inside it; transcripts on local disk are lost on restart, SessionStore mirrors them (transcripts only, best-effort); credential order, and /status.
4 我们自己做的 [D3 + code]: agentd.py (token checked before any path; someone else's session answers 404, same as none; project is a name inside your folder, no ".."; admin makes tokens, own tenant only); store.py (token stored as SHA-256); runner.py (a new process per message, environment built from nothing); turn.py (load, run, save; agent.py not edited; read-only mode). About 370 new lines. 17 checks without a key.
5 真实测试 (3 intro slides): T1 two users at once, naive (engine imported, a thread per request) vs one process per session, 5 trials each; T2 lin asks for a file in sam's folder, 5 trials; T3 say a word, restart the service, ask for it, file kept vs removed, 5 trials each.
6 结果 [D4, the main chapter]: T1 naive: lin got sam's code name 5/5 (in 2 of 5 the answer noted the folder looked wrong; sam got their own 5/5); process per session: own answer 10/10, other file seen 0/10. Why: the engine keeps its folder in one variable, agent.ROOT; the later request changes it while the earlier one waits for the model (show the 4-step timeline). T3 kept: 5/5, no tool call. Removed: 0/5, no error at all; the agent searched (5 to 15 tool calls); 3 said they did not know, 2 offered another word from the project as the answer. Honest: five trials, one model, our own small project, the overlap was arranged.
7 一个真实的坑 (we got it wrong first): a leftover variable. We expected an old token to travel with our key; the test failed. Measured: with the key given in code the token is NOT sent, but an old ANTHROPIC_BASE_URL sends our call AND our key to the old address; if the key itself comes from a variable, the old token goes along. Fix: build the engine's environment from nothing. (Real SDK 0.125.0, stub server; about the SDK, not Claude Code.)
8 身份不是隔离 (what is still open) [D5]: T2: in 4 of 5 the model used the file tool, was refused and stopped; in 1 of 5 it went straight to `cat` and got sam's file, because read-only mode allows it. Stopping was the model's choice, not our protection. Also open: no policy (ep 2), no sandbox (ep 4), the engine still holds the key (ep 5). One design change since the intro video: commands will be started by the service, outside the agent's sandbox (macOS cannot put one sandbox inside another; tested).
9 结尾: one line: identity says who is asking; only a boundary decides what they can touch. Next: rules nobody can switch off. Question for the comments: 「你们团队共用的 AI 工具，知道每个请求是谁发的吗？」

## Notes / open points
- The naive version is our own deliberately simple first try, not any product. Say so on screen.
- The 0.5 s offset guarantees the overlap; we did not measure how often it happens with real traffic.
- "Read-only mode" is series 1's mode: file reads and a short list of commands (ls, cat, grep and others).
- Two sessions of the same user share one project folder; not tested, harmless while read-only.
- Grading of the "removed file" answers is by the first line (one answer offered a word and added "I don't know it" at the end).
- All numbers come from ep01/demo/facts.json, computed by code. Tokens read: about 138,000 input tokens (not exact for the naive runs); output not counted.
- Code is uncommitted in the public repo until you say "push".

## Changes after the outline was approved (Michael, 2026-11-25)
- New chapter 03 系统架构 after the basic words: the whole series on one map, how one request flows, how the first version was wired, and whether one agent per laptop has the same problem (our reasoning, not tested). Later chapters move up one number.
- The login-credential order slide is gone (the environment variable is now explained in the code and pitfall slides). The three "why" slides are two.
