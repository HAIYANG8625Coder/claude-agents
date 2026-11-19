# Title
从零到1做Agent第3集：笔记｜系统提示和 NOTES.md
# Description
Agent 怎么才懂你的项目？靠系统提示和一份笔记文件。
这一集给 Agent 加上这两样，再用固定任务测它有没有变好。

两样东西
1. 系统提示：API 里单独的 system 参数，写角色、几条规则、环境信息
2. 笔记文件：Claude Code 叫 CLAUDE.md，我们的版本叫 NOTES.md，放进第一条用户消息

对照官方文档
· CLAUDE.md 是系统提示之后的一条用户消息，不是系统提示本身；Claude 把它当背景信息，不是强制执行的配置
· 建议：每个文件少于200行；只写从代码里看不出来的；写得具体、能检查

真实测试（DeepSeek 模型，每种情况跑3次）
· 折扣任务最后写 Done 行：没笔记 0/3，有笔记 3/3
· 辅助函数放进 helpers/ 文件夹：没笔记 0/3，有笔记 3/3
· 四舍五入：2/3 对 3/3，只差一次，可能是运气
· 检查是代码做的，不是让模型自己说

章节
00:00 开场：只多一份笔记，做法就变了
00:20 回顾第2集
00:33 系统提示是什么
01:10 笔记文件
01:58 笔记放在哪
02:33 笔记里写什么
03:11 一份笔记
03:39 怎么知道有用
04:32 跑一遍
05:09 一个意外
05:47 和 Claude Code 比一比
06:08 三个坑
06:31 这一集记住的事

说明：样本很小，只用了一个模型，只是演示这个方法。演示用 DeepSeek 的模型，只引用 Anthropic 官方文档，没有引用源码。视频里的声音是我用 AI 克隆的声音。

Build a Claude Code style agent from scratch, episode 3: a system prompt and a notes file (like CLAUDE.md), tested on fixed tasks.

#Agent #ClaudeCode #AI编程
# Tags
Agent, AI Agent, Claude Code, 从零做Agent, AI编程, 系统提示, system prompt, CLAUDE.md, Python, 大模型, Anthropic, DeepSeek, LLM agent
