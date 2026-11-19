# Title
从零到1做Agent第7集：子Agent｜是什么、为什么、有没有用
# Description
Agent 读一个文件，对话就长一截；读了好多个，后面的活都得背着它们。这一集从零讲清楚子 Agent：它是什么，为什么需要，再用我们自己的真实任务测一测，最后复习第1到7集。

子 Agent 是什么
主 Agent 派出去的小助手：有自己全新的对话，干完一件小事，只把一句结论带回来。像派助手去图书馆，他翻很多本书，你只收一页纸。

好处和代价
好处：主对话保持干净；我们只给它读和搜，改不了东西，更安全。代价：多花 token。Anthropic 说 Agent 约是聊天的 4 倍，他们的多 Agent 研究系统约 15 倍；带回的一页纸还可能漏细节。

真实测试（DeepSeek 模型，只是我们自己的小测试）
任务：从发帖记录里找出 11 月 13 日到 19 日的小红书笔记，共 21 条，打开帖子文件抄下话题标签，做成表存成文件。两种设置各跑 3 次。
· 什么都靠自己：表格对 21/21/20 行，模型调用 34/40/75 次
· 任务里明说让子 Agent 去读文件：表格对 21/20/21 行，模型调用 26/28/33 次
只有 3 次，子 Agent 第一次没出场，所以不能说它更好。主对话最多涨到 1.6 万 token 左右，子 Agent 的好处这次没看出来。

一个真实的坑
第5集的上下文管理压缩得太频繁：旧版每次运行平均压缩 35 次，修复后不到 4 次。同时把轮数上限从 60 提到 100，两处一起改，没分开测。

章节
00:00 开场
00:17 问题出在哪
00:33 什么是子 Agent
00:46 好处和代价
01:11 Claude Code 里的样子
01:39 我们自己做的
02:01 真实测试：测什么、怎么评分
02:39 一次真实运行，逐步看
03:31 结果
04:24 一个真实的坑
05:05 第1到7集复习
05:41 结尾

说明：Claude Code 的部分只引用官方文档（sub-agents 页面）和 Anthropic 的多 Agent 研究系统文章。视频里的声音是我用 AI 克隆的声音。

Build a Claude Code style agent from scratch, episode 7: subagents, why an agent needs them, a small real test on a weekly posting summary, and a review of episodes 1 to 7.

#Agent #ClaudeCode #AI编程
# Tags
Agent, AI Agent, Claude Code, 从零做Agent, AI编程, 子Agent, subagent, 上下文, 大模型, Python, Anthropic, DeepSeek, LLM agent
