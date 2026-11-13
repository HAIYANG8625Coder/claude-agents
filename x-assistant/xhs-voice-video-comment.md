# 置顶评论（视频笔记：Claude Code做视频｜只给题目）

📌 链接和命令都放这了，建议先收藏⭐

🧰 需要：Node.js 22+（nodejs.org）、HeyGen 免费账号

① 装 Claude Code 终端版：
curl -fsSL https://claude.ai/install.sh | bash

② 下载技能，装依赖（HyperFrames + ffmpeg）：
git clone https://github.com/HAIYANG8625Coder/claude-agents.git
cd claude-agents/avatar-video && npm install

③ 克隆声音：录 1–2 分钟安静环境下的人声，到 app.heygen.com/avatar/voices 选即时克隆，免费版就行

④ 在 claude-agents 文件夹里运行 claude，输入 /mcp，选 heygen 登录（桌面版登不上，要用终端）

⑤ 在 claude-agents 根目录新建 AVATAR-你的名字.md，写三行：
voice_id: 你的声音ID
voice_model: heygen-voice-1-turbo-free
pace: 0.92

⑥ 对 Claude Code 说：用我的声音做一条关于 XX 的视频

技能说明在这：github.com/HAIYANG8625Coder/claude-agents/tree/main/.claude/skills/voice-video

卡在哪一步，留言告诉我👇

---
## 实际发布（2026-11-12）
评论限 300 字、换行会被吞，所以拆成 1 条评论 + 2 条回复，命令用 && 连成一行：
1. 主评论：📌 … ① curl -fsSL https://claude.ai/install.sh | bash （②–⑥ 在回复里👇）
2. 回复：② git clone https://github.com/HAIYANG8625Coder/claude-agents.git && cd claude-agents/avatar-video && npm install ③ … ④ …
3. 回复：⑤ voice_id: 你的声音ID ｜ voice_model: heygen-voice-1-turbo-free ｜ pace: 0.92 ⑥ … 技能说明链接
置顶：网页版没有置顶选项，需在手机 App 里长按主评论 → 置顶。
