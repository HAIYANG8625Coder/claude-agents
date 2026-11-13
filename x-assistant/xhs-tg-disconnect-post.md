# 标题
Claude Code遥控断联｜2个根因

# 正文
在新加坡写代码，用手机 Telegram 遥控 Claude Code。前两天整理过 9 个坑，这次又遇到断联，查到 2 个根因，修法都在下面👇

😵 现象
① 早上打开电脑，前一晚开着的 Claude 会话没了
② 新开的会话聊到一半，Telegram 不回了。活其实已经干完，只是发不到手机上

🔍 根因1：新会话把机器人抢走了
Telegram 插件开在全局设置里，每开一个会话，就多一个机器人进程
一个机器人同时只能有一个进程收消息。插件启动时会直接结束上一个进程，它默认旧进程是崩溃留下的
我做视频的技能会在后台开一个 claude -p 去调 HeyGen。它一启动，主会话就断了；它跑完退出，机器人就没人接了
桌面版新开一个对话，也会抢

🔍 根因2：macOS 半夜自动更新
凌晨 2:53 自动装了 27.2.1，2:55 重启，所有会话都被关掉

🛠 修复
① 全局关掉插件：在 ~/.claude/settings.json 里把
"telegram@claude-plugins-official" 改成 false
② 只给遥控用的那个会话单独打开：
claude --settings '{"enabledPlugins":{"telegram@claude-plugins-official":true}}' --channels plugin:telegram@claude-plugins-official
③ 脚本里的 claude -p 也加 --settings，把它设成 false
④ 可选：系统设置 → 通用 → 软件更新 → 自动更新，关掉"安装 macOS 更新"
系统更新不常有，我自己留着没关，碰上了重开会话就行

💡 排查：ps 看有几个 telegram 进程；~/.claude/channels/telegram/bot.pid 记着现在是哪个进程在收消息

你遥控 Claude 时遇到过断联吗？最后查出来是什么原因？

#ClaudeCode #AI编程 #Telegram #AIAgent
