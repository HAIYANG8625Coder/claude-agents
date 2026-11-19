# Episode 9 outline: memory between sessions (for approval; process of 2026-11-20)

Format: article-explainer, landscape, about 7 min, series "从零做 Agent 第 9 集". Same look as ep 8. Say "token", never 词元.
Cover: 「Agent 的记事本：记忆」 / 「新开一个对话，它还记得你说过什么吗」
Real test is DONE before this outline (ep09/demo, session 1 x 5, session 2 x 20, DeepSeek, every earlier part on).

## Beginner gate
- 会话 session: one conversation from start to end. A new session starts with an empty head. Chapter 1.
- 记忆 memory: a folder of short notes that survives between sessions. Picture: sticky notes in a drawer, plus an index card on top. Chapter 2.
- 索引 index: MEMORY.md, one line per note, the only part loaded at the start. Chapter 2/4.
- 笔记文件 (ep 3) vs 记忆: the notes file is what YOU write; memory is what the agent writes itself. Chapter 3.
- 过期 stale: a note that was true once and is not any more. Chapter 5/6.

## Chapters
0 开场: the real test in one line: two sessions, the user states four facts in session 1 and asks again in a brand-new session 2. Three questions: what is memory, why, does it help (and what if a note is wrong).
1 问题出在哪 [D1]: a new session forgets everything said in chat. What ep 3's notes file does not cover: things you only say once. Shown with real run A (no memory): edits the file it must not edit, answers in English, cannot say how to deploy.
2 什么是记忆 [D2]: a folder of short notes + one index line each; only the index is loaded at the start, a note is opened when needed; save only what cannot be looked up again.
3 Claude Code 里的样子 (docs, read in full): CLAUDE.md (you write) vs auto memory (Claude writes), where they live, what loads at the start (CLAUDE.md whole, MEMORY.md first 200 lines or 25 KB, topic files on demand), the four note types, what it skips (anything derivable from the code), "context, not enforced configuration", /memory, plain markdown you can edit. A slide of real things it stores: e.g. "always use pnpm, not npm", user role, testing feedback.
4 我们自己做的 [D3 + code]: memory_write, memory_forget, the index in the first message (so it survives compaction), the 200 line / 25 KB cut, the two prompt rules (save only what you cannot look up; check a note before relying on it). Real lines from ep09/agent.py and a real note file.
5 真实测试 (3 intro slides: session 1, session 2 task, setups A/B/C/C0) + one real run [D4 sequence chart]: session 1 = user states config.py is ops-owned and changes go through SHOP_ env vars, staging deploy key name and address, always answer in Chinese; session 2 = new conversation: add shipping_fee, adjustable threshold, then "how do I deploy to staging". Setups: A no memory; B memory from session 1; C memory out of date (the docs say the key was renamed); C0 = C without the "check before you rely" rule. Each earlier part named when it acts.
6 结果 [D5]: session 1: all 5 runs saved all 4 facts, 0 junk notes (3 to 4 notes each). Session 2: A edited config.py 5/5, never answered in Chinese, could not give the deploy key; B left config.py alone 5/5, used the SHOP_ variable 5/5, answered in Chinese 5/5, right key 5/5; turns A mean 23.0 vs B 16.2, tokens read A 124,585 vs B 79,434. Stale memory: C new key reported 3/5 (believed the old note 2/5), C0 4/5 (believed old 1/5): the "check first" rule did not show a benefit. Honest: 5 runs, tiny; B shows what memory is for; C/C0 show a wrong note can be believed.
7 一个真实的坑 (we really hit it): first pilot: the agent said "I have no memory tool" and saved nothing, because plan mode hid the memory tools. Fix: plan mode offers them (a note is not an edit of the project), still no edit tools; test added. Also: I started the batch twice by mistake and threw the numbers away (one line, optional).
8 EP1 到 EP9 总复习 [D6 map]: one line per episode, EP9 = memory; what is missing: always-on (ep 10).
9 结尾: question for the comments: "你的 Agent 有没有记错过什么？"

## Notes / open points
- Syllabus mentions an optional offline cleanup pass: NOT built; I will say so on screen in one line rather than claim it.
- Intro slide on what Claude Code really stores (as you asked for hooks): included in chapter 3, from the docs only.
- Length about 7 min. Facts file: all numbers computed from demo/*.json by code.
