# 标题
Claude Code遥控不掉线｜3步

# 正文
用手机 Telegram 遥控 Claude Code，聊着聊着就收不到回复？我查到原因，改了 3 个设置，步骤都在下面👇

🛠 3 步设置
① 全局关掉插件
在 ~/.claude/settings.json 里把
"telegram@claude-plugins-official" 改成 false

② 只给遥控用的会话单独打开
claude --settings '{"enabledPlugins":{"telegram@claude-plugins-official":true}}' --channels plugin:telegram@claude-plugins-official

③ 脚本里的 claude -p 也关掉
同样加 --settings，把它设成 false

➕ 可选：系统设置 → 通用 → 软件更新 → 自动更新，关掉"安装 macOS 更新"。我自己没关，碰上了重开会话就行

🔍 为什么会掉线
一个 Telegram 机器人同一时间只能有一个进程收消息
插件开在全局时，每开一个会话就多一个进程，新的一启动就把旧的结束掉
所以桌面版新开一个对话，或者脚本在后台跑 claude -p，都会把机器人抢走
macOS 半夜自动更新重启，也会把会话全关掉

💡 不止 Telegram：放在全局设置里的插件，每个会话都会加载，后台的 claude -p 也一样。脚本用不到的插件，可以用 --settings 关掉

🔎 自查：ps 看有几个 telegram 进程；~/.claude/channels/telegram/bot.pid 记着现在是哪个进程在收消息

你用手机遥控 Claude Code 吗？用的是 Telegram 还是别的办法？

#ClaudeCode #AI编程 #Telegram #AIAgent #效率工具
