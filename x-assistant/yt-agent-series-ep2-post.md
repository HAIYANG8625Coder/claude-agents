# Title
从零到1做Agent第2集：工具｜读文件、搜索、改代码、跑命令
# Description
Agent 为什么能读文件、改代码、跑测试？因为我们给了它工具。
这一集给第1集的循环装上4个工具，再看它自己修好一个 bug。

四个工具
1. read_file：读文件，每行加行号
2. grep：用正则搜索，最多返回50条
3. run_bash：执行命令，超时20秒
4. edit_file：把一段旧文字精确替换成新文字，旧文字必须一模一样且只出现一次

三条设计原则
1. 出错别崩溃：把错误写成清楚的话，用 is_error 还给模型
2. 返回别太长：超过4000字符就截断，并提示它请求少一点
3. 守住边界：读、搜、改会检查路径在不在项目文件夹里；run_bash 不受这个检查管，权限留到后面讲

真实运行（DeepSeek 模型）
· 修 bug：add 函数被写成相减，5轮后测试全部通过
· 错误恢复：让它不读文件直接改，被拒绝后自己先读再改，成功

章节
00:00 开场：模型自己什么都不会执行
00:24 回顾第1集的循环
00:35 一个工具由哪四样东西组成
01:16 四个工具：read_file、grep、run_bash、edit_file
02:16 为什么用精确替换，不重写整个文件
02:54 原则1：出错别崩溃
03:24 原则2：返回别太长
04:04 原则3：守住边界
04:29 演示：自己修好一个 bug
05:18 演示：没读文件就改，被拒绝后怎么恢复
05:40 和 Claude Code 的工具比一比
06:13 设计工具的三个坑
06:39 这一集记住四件事

说明：屏幕放不下，视频里的工具说明写得比较短，官方文档建议至少写三四句。演示用 DeepSeek 的模型，只引用 Anthropic 官方文档和文章，没有引用源码。视频里的声音是我用 AI 克隆的声音。

Build a Claude Code style agent from scratch, episode 2: four tools (read, grep, bash, exact-string edit) and three design rules, with a live bug-fix demo.

#Agent #ClaudeCode #AI编程
# Tags
Agent, AI Agent, Claude Code, 从零做Agent, AI编程, 工具调用, tool use, function calling, Python, 大模型, Anthropic, DeepSeek, LLM agent
