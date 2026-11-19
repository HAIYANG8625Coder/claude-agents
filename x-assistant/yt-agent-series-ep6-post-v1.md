# Title
从零到1做Agent第6集：计划模式和任务清单｜真实测试
# Description
长任务怎么不跑偏？
这一集给 Agent 加两个工具：计划模式和任务清单，并用一个真实的“提交前检查仓库”任务测试。

真实测试（DeepSeek 模型，每种设置 5 次）
仓库有 4 个插件、9 个技能、4 个子 Agent，我们故意放进 12 处错误，任务只有一句：提交之前，按 CLAUDE.md 的规则检查，全部修好。
· 什么都不加：60 处里改对 59 处，平均 15 轮
· 任务清单：60 处全对，平均 30 轮
· 计划模式加清单：60 处全对，平均 27 轮
唯一漏掉的一次在“什么都不加”里：漏了一个链接，最后却写“所有规则都符合了”。5 次太少，不能说清单更准；清单只是让轮数翻倍。另外两个更小的任务（8 件事、16 件事）三种设置也全部做对。

Claude Code 的做法（官方文档）
· 计划模式：Shift+Tab 或 /plan，读文件、探索、写计划，批准之前不改源码
· 任务清单：待做、进行中、完成，Ctrl+T 显示，压缩后不丢

我们的做法
· 计划模式只给读文件和搜索，加一个 submit_plan，批准后编辑工具才出现
· todo_write：每次传整份清单，同一时间只有一项进行中

两个真实的坑
1. 第一版计划模式把读文件也拦了，模型只能盲写计划
2. 计划太长被截断：修好之前 5 次里有 2 次一个文件都没改

章节
00:00 开场：59 对 60
00:31 为什么长任务会出事
00:56 Claude Code 的计划模式
01:28 我们的计划模式
01:53 Claude Code 的任务清单
02:27 我们的 todo_write
02:55 真实测试
03:56 两个真实的坑
04:39 这一集记住的事

说明：官方没有写任务的字段和状态名，清单的设计是我们自己的。官方说新一点的模型不写清单也能追踪多步骤的工作，所以短任务不一定需要。演示用 DeepSeek 的模型，讲 Claude Code 的部分只引用官方文档。视频里的声音是我用 AI 克隆的声音。

Build a Claude Code style agent from scratch, episode 6: plan mode and a task list, tested on a pre-commit repo check with 12 planted faults.

#Agent #ClaudeCode #AI编程
# Tags
Agent, AI Agent, Claude Code, 从零做Agent, AI编程, 计划模式, plan mode, 任务清单, todo list, Python, 大模型, Anthropic, DeepSeek, LLM agent
