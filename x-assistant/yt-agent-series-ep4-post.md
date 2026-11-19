# Title
从零到1做Agent第4集：权限｜放行、询问、拒绝
# Description
你敢让 AI 在你的电脑上直接执行命令吗？
这一集给 Agent 加一道权限关卡：放行、询问、拒绝，让它做事，又不会乱来。

关卡怎么设计
1. 每个工具调用先过关：先看拒绝，再看询问，最后看放行，第一条匹配的决定结果（官方文档同样的顺序）
2. 规则写成 工具名(内容)，星号匹配任何文字，包括空格；用户目录和项目目录的规则合并
3. 一条命令拆成几段，每一段都要放行；看不懂的写法直接询问
4. 被拒绝时把原因当错误还给模型，不让程序崩溃

四种模式：default、accept-edits、read-only、dont-ask。官方还有 plan、auto、bypassPermissions，这集没做。

真实测试（DeepSeek 模型）
· README 里放了一条命令（提示注入），12 次运行，模型一次都没照做。但 12 次太少，不能说明它安全
· 脚本模拟的会照做的假模型：没有关卡，文件被创建；有关卡，用户说不，没有创建
· 修 bug 任务：默认模式每次问 4 次；accept-edits 加一条放行规则，每次只问 1 次

章节
00:00 开场：敢让 AI 直接执行命令吗
00:19 谁来决定
00:37 规则的写法
01:04 先拒绝，再询问，再放行
01:20 我们的规则
01:44 关卡的代码
02:01 复合命令
02:34 没有规则的时候
03:04 四种模式
03:34 询问和拒绝
04:05 真实测试：藏在文件里的指令
04:38 但是不能指望模型
05:11 问得太多
05:49 和 Claude Code 比一比
06:33 三个坑
06:55 这一集记住的事

说明：假模型是脚本模拟的，不是真实模型。拒绝规则不是围绕程序的安全边界，真正的隔离要用沙箱，这集没做。演示用 DeepSeek 的模型，讲 Claude Code 的部分只引用官方文档。视频里的声音是我用 AI 克隆的声音。

Build a Claude Code style agent from scratch, episode 4: a permission gate with allow, ask and deny rules, tested against a prompt injection.

#Agent #ClaudeCode #AI编程
# Tags
Agent, AI Agent, Claude Code, 从零做Agent, AI编程, 权限, permissions, 提示注入, prompt injection, Python, 大模型, Anthropic, DeepSeek, LLM agent
