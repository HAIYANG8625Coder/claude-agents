# 标题
Claude Code手机遥控｜9个坑

# 正文
在新加坡写代码，最近在学 AI Agent。用手机 Telegram 遥控电脑上的 Claude Code，从零配置到双向聊天，9个坑都整理好了，建议先收藏⭐👇

🧰 准备：Mac + Claude Code + Telegram 账号

① 建机器人
Telegram 找 @BotFather → /newbot → 拿到 token

② 装插件 telegram@claude-plugins-official
⚠️坑1：提示没有 git → 终端运行 xcode-select --install，同意许可，等几分钟
⚠️坑2：找不到官方插件市场 → /plugin marketplace add anthropics/claude-plugins-official
⚠️坑3：终端提示 claude: command not found → curl -fsSL https://claude.ai/install.sh | bash，再把 ~/.local/bin 加进 PATH

③ 装 Bun
⚠️坑4：机器人完全没反应，因为插件靠 Bun 运行 → curl -fsSL https://bun.sh/install | bash，把 ~/.bun/bin 加进 PATH，重启 Claude
⚠️坑5：修好还是不行？失败会被缓存，约 15 分钟后开新会话才重试

④ 保存 token
/telegram:configure <token>
⚠️坑6：我把 token 直接贴进了聊天。泄露了就去 BotFather /revoke 换新的

⑤ 配对
给机器人发消息拿配对码 → /telegram:access pair <配对码>
只自己用：/telegram:access policy allowlist

⑥ 双向聊天
⚠️坑7：桌面版会话只能发、收不到你的消息，要在终端启动：
claude --channels plugin:telegram@claude-plugins-official
⚠️坑8：两个会话会抢同一个机器人，只留一个
⚠️坑9：机器人跑在自己电脑上，终端关了或电脑睡了就不回

现在出门也能用手机让 Claude 干活了。你们还踩过什么坑？评论区聊聊～

#ClaudeCode #AI编程 #Telegram #AIAgent
