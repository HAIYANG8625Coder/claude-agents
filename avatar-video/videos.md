# Avatar videos

Every video made with `/avatar-video`. The scripter reads this to avoid repeats; the last line of each entry says what to improve next time.

## 2026-11-11 — 新加坡小一｜外国人报名5步 (approved by Michael, not posted yet)
Platform: xhs · Length: 52.8 s · Folder: videos/2026-11-11-sg-p1 · Source: Michael's own note of the same name
Voice: macOS Tingting (no avatar yet, HeyGen not signed in) · Script: reviewer's fixed Script 2 (mistake-first hook, +86 → +65)
What to improve next time: listen for how Tingting reads "M O E / I O I / P D F"; add soft music once signed in to HeyGen.

### 2026-11-12 — re-voiced in Michael's cloned voice (v2, waiting for his review)
Voice: HeyGen instant clone `michael-voice-clone-2min` (made by Michael in the HeyGen web app from voice-samples/michael-voice-clone-2min.mp3), model heygen-voice-1-turbo-free (free). Generated per sentence via the HeyGen MCP in the Claude Code CLI (the desktop app's HeyGen sign-in fails with "Invalid redirect URI"). Joined with tools/heygen-voice.py; scene/caption times remapped from the Tingting timing. Length 48.4 s. Render: renders/2026-11-11-sg-p1_2026-11-12_09-49-09.mp4. Tingting v1 kept in tingting-v1/.

### 2026-11-12 — v3: one-take voice (waiting for Michael's review)
Michael's v2 feedback: "lagging during this video and end of this video, sounds incoherent". Cause: voicing one sentence per call resets the intonation each time and leaves uneven holes (extra 0.4–0.6 s pauses inside 第三步 and 完整清单 plus the added gaps, so the ending stumbled).
Fix: the whole script in ONE HeyGen create_speech call (same clone, free model), sentence times from HeyGen's per-word timestamps (tools/heygen-whole.py), scenes moved with tools/retime.py, captions timed from the word timestamps, scene fades end exactly when the next scene starts. Length 45.6 s. Render: renders/2026-11-11-sg-p1_2026-11-12_21-14-18.mp4. v2 kept in heygen-v2/.
Lesson: always voice the whole script in one take; never stitch sentence-by-sentence TTS.

### 2026-11-12 — v4: same take, 8% slower (APPROVED by Michael: "not bad")
Michael asked to slow down a little. HeyGen ignores `speed` for instant clones (it returned the same 45.2 s take), so the v3 take was stretched to 92% tempo with ffmpeg atempo, pitch kept (tools/slow-take.py), then heygen-whole.py --dir .voice-heygen-full-0.92, retime.py, captions from the scaled word times. Length 49.5 s. Render: renders/2026-11-11-sg-p1_2026-11-12_21-26-14.mp4. v3 kept in heygen-v3/.

### 2026-11-12 — v4.1: captions on the sound (approved v4 + timing fix)
Same voice as v4 (0.92). Captions and scene changes now snap to where the voice actually restarts after a pause (HeyGen's word starts run ~0.15–0.2 s early), via the new voice-video skill (build_vo.py + sync.py). Length 49.5 s. Render: renders/2026-11-11-sg-p1_2026-11-12_21-48-09.mp4. v4 kept in heygen-v4/. Michael asked for this update; waiting for his listen.

## 2026-11-12 — 我怎么做这条视频（克隆声音，免费版）
Platform: xhs · Length: 45.4 s · Folder: videos/2026-11-12-how-i-make · Made with the voice-video skill (one take, 0.92)
Script: Script 1 (reviewer-fixed) with Michael's change: step 1 = "在安静的房间，录两分钟自己的声音" (not the old-video route, since most viewers don't have one).
Render: renders/2026-11-12-how-i-make_2026-11-12_22-12-27.mp4 — waiting for Michael's review.
What to improve next time: the take script used to strip all spaces, so HeyGen read "ClaudeCode"; fixed (only spaced single letters are joined). Matching is now letter by letter.

### 2026-11-12 — 我怎么做这条视频 v2: made more attractive after studying 数字人小米 on Xiaohongshu
Their top tutorial (不会剪辑也能出片, 675 likes / 1571 saves / 169 comments) uses a HUD "studio" frame, a LIVE face picture-in-picture, flow diagrams, real proof visuals, keyword-highlighted captions and a save / comment-keyword call to action. Applied (same voice, same script): HUD frame + timecode + progress bar, a LIVE voice meter that moves with the speech (our face stand-in), karaoke captions, slow zoom per scene, a flow diagram (整篇稿子 → 一次录完 → 慢 8%), the real stitched-vs-one-take waveforms on the 坑 / fix scenes, a "先收藏 · 下次照着做" chip, a quiet music bed and 7 sound effects. v1 kept in v1/. Render: renders/2026-11-12-how-i-make_2026-11-12_22-22-57.mp4 — APPROVED by Michael.

### 2026-11-12 — 我怎么做这条视频 v3: humanized script (APPROVED by Michael, replaces v2)
Ran the humanizer skill over the voice-over: cut the slogan closer "剩下的交给 Claude Code" (now "剩下的步骤，Claude Code 帮我跑完"), merged the fragment row "一句一张卡片，字幕对准每个字" into one sentence, and replaced the repeated "所以只能手动" with a true first-person detail ("我试过走接口克隆，免费版直接拒绝" / "桌面版我一直登不上"). Same facts and 13 scenes; new take, 0.92 pace, re-synced and remixed. Length 46.5 s. Render: renders/2026-11-12-how-i-make_2026-11-12_22-50-38.mp4. v2 kept in v2/.

### 2026-11-12 — 我怎么做这条视频 v4: on-screen links (waiting for Michael's review)
Same voice and script as v3. Added app.heygen.com/avatar/voices under the step 2 card, "skill: voice-video · 已开源" on the Claude Code card, and github.com/HAIYANG8625Coder/claude-agents on the end card. Length 46.5 s. Render: renders/2026-11-12-how-i-make_2026-11-12_22-58-27.mp4. v3 kept in v3/. Note: Xiaohongshu may limit reach for notes that show outside links; there is a v3 without them.

### 2026-11-12 — 我怎么做这条视频 v5: "just give a topic" (waiting for Michael's review)
Michael's change: the viewer doesn't record or write anything per video; they give Claude Code a topic, it writes 2 scripts, they pick one, and it voices it in one take and makes the cards and captions. Lines 7, 8, 11, 12 rewritten (humanizer rules), scenes 6, 7, 10, 11 redrawn (题目 → Claude Code; 写 2 版稿子 → 我挑 1 版 → 一次录完; 卡片 + 字幕; 不用录 · 不用剪 · 10 分钟一条). Links kept. Length 47.3 s. Render: renders/2026-11-12-how-i-make_2026-11-12_23-03-41.mp4. v4 kept in v4/.

### 2026-11-12 — 我怎么做这条视频 v6: no recording per video, coherent story (FINAL, approved by Michael; published on Xiaohongshu 2026-11-12)
Michael's change: drop the stitched-voice mistake; make clear nothing is recorded or edited per video (Claude Code does script, voice-over and visuals); whole video logically coherent; review before changing. video-reviewer verdict FIX: added "what this is" (open-source skill on GitHub), removed the line 2 / line 7 repetition, dropped jargon (接口) and the invented quiet-room advice, "一条我只花十分钟" (his time). Story: hook → only a topic → open-source skill → one-time setup (3 steps, only recording is the 2-min sample) → every video: topic → 2 scripts, pick 1 → cloned-voice voice-over + cards + captions → 不用录 不用剪 10 分钟 → question. 12 scenes, 44.3 s. Render: renders/2026-11-12-how-i-make_2026-11-12_23-13-11.mp4. v5 kept in v5/.

### 2026-11-12 how-i-make-en v1 (English version for X; APPROVED, posted on X 2026-11-12)
- English translation of how-i-make v6: same 12 scenes, music and sound cues; new one-take English voice (HeyGen, language en), pace 0.92, karaoke + push.
- heygen_take.sh now takes VOICE_LANG (default zh); acronym joining only touches capital letters, so "there's a" is no longer merged.
- Length 46.6 s. Render: `avatar-video/videos/2026-11-12-how-i-make-en/renders/2026-11-12-how-i-make-en_2026-11-12_23-45-54.mp4`

## 2026-11-13 — Jensen Huang is out: what NVDA's price really says
Platform: x · Length: 43.3 s · Folder: videos/2026-11-13-nvda-huang (no-avatar mode: cloned voice, one take, pace 0.92, karaoke + push, music bed)
Script: Nvidia is down 31 percent from its high. Most of that happened before the scandal. On November sixth, the New York Times reported on a U.S. intelligence memo. It linked CEO Jensen Huang to an alleged Chinese intelligence asset. Six days later, Huang resigned. That's a governance and national-security risk, not gossip. From November sixth to the twelfth, Nvidia fell 11 percent. AMD rose 31 percent. Money moved inside AI chips. It didn't leave AI. General thinking only. Separate three shocks: the sector crash, the scandal, and the fundamentals. Then watch what's next: earnings on November seventeenth, and a permanent CEO. Not financial advice. How do you handle headline risk?
Render: renders/2026-11-13-nvda-huang_2026-11-13_00-30-45.mp4 (v2: removed the "Michael's cloned voice" box at Michael's request; v1 kept in v1/). APPROVED, posted on X 2026-11-13 with video.
What to improve next time: check the market is closed before calling a price a "close" (Nov 12 was still trading, so the figures are labeled midday); the reviewer caught "nearly half" vs the real ~71% before the scandal.

### 2026-11-13 — NVDA re-styled: preset A "Market news" (waiting for Michael's review)
Michael's feedback on his two X videos: they look the same; make them better and give them different styles, keeping his cloned voice. Same take, script, timing and music mix as the approved v2 (no new HeyGen call); only the visuals changed. New look: light paper background, ink type, red/green numbers, serif "Market Notes" masthead, black ticker tape, full-width −31% hook + price line, a paraphrased news clipping with an "ALLEGED" stamp, a "HUANG RESIGNS" slab, big bars growing on the spoken words, calendar tiles, hard cuts (new `sync.py --cut`). Folder: videos/2026-11-13-nvda-huang-market · Length 43.3 s · Render: renders/2026-11-13-nvda-huang-market_2026-11-13_09-10-43.mp4. The original dark version is untouched in videos/2026-11-13-nvda-huang/.
Also added: style presets A–D in brand/DESIGN.md; avatar-video and voice-video now pick a preset per video instead of copying the last one.
What to improve next time: try preset C (bold type) or B (real screen recordings) for the next X video, so three videos in a row don't share a look.

## 2026-11-13 — 视频风格教程（4种风格）· preset C bold type (published on Xiaohongshu 2026-11-13)
Platform: xhs · Length: 47.9 s · Folder: videos/2026-11-13-video-styles · Style: C · bold type (full-screen color per scene, huge words, hard cuts via `sync.py --cut`, karaoke captions in a black pill)
Follow-up to 我怎么做这条视频. Michael picked Script 2 only (the tutorial) and asked for a humanizer pass: cut the slogan closer, added true details (the 2 X posts looked alike; the skill literally said "keep its styles and layout"; this video is style C). One HeyGen take, zh, pace 0.92.
Demo inside: the English NVDA market-news render (muted, scene 5) and the dark vs market versions side by side (scene 7, both from media 21.0 s so the bars grow together); stills of the two X videos in the hook; the real SKILL.md line in a code card.
Render: renders/2026-11-13-video-styles_2026-11-13_09-30-45.mp4. Note: x-assistant/xhs-video-styles-post.md.
What to improve next time: a full-frame scene that shows at frame 0 needs `opacity:0` in CSS (sync's set at 0 shows it) or lint errors with gsap_fullscreen_overlay_starts_visible.

## 2026-11-13 — 微软宕机20多小时，到底怎么回事儿？ (published on Xiaohongshu 2026-11-13)
Platform: xhs · Length: 59.8 s · Folder: videos/2026-11-13-msft-outage · Style: A · news desk ("科技快讯" masthead, status ticker) with 小Lin说-style evidence cards (paraphrased headline collage, highlighter marks, 说法更新 before/after cards, 未证实 stamp)
Michael first approved a 38 s practical script (Script 2, kept in v1-script2/), then asked to learn from 小Lin说 on Xiaohongshu; her patterns are now in brand/NEWS-PLAYBOOK.md and video-scripter reads it for news topics. He picked the 60 s Version B. One HeyGen take, zh, pace 0.92.
Script: 微软宕机二十多个小时，到底怎么回事儿？美东周四下午开始，Outlook、Teams、Copilot 都受了影响。但原因，微软的说法更新了。微软一开始说负载太高。后来补充，不是流量变多，而是一批服务器突然不可用。说白了，就像超市收银台突然关了几个，人全挤到剩下的。只是个比方。至于为什么，有报道称可能和配置更改有关，微软没证实。有公司推迟了财报，英国 NHS 部分服务也受影响。现在正在恢复，部分用户可能还有问题。我觉得，邮件、聊天、文件、AI 绑在一家，出事就全停。所以宕机期间发的邮件，先别急着重发。微软说重试延长到四十八小时，邮件可能还会到。先问收件人。再备个渠道，电话、微信群，或者另一个邮箱。你们公司有备用方案吗？
Render: renders/2026-11-13-msft-outage_2026-11-13_23-42-00.mp4 (xhs upload copy: renders/msft-outage-xhs.mp4).
What to improve next time: don't force 小Lin's "原因变了" reversal when a source only clarified (the reviewer caught "改口"); declare Chinese fonts with @font-face local() or check fails; give overlapping collage cards ~135 px vertical spacing; chips need white-space:nowrap.

## 2026-11-14 — 为什么说，Agent 的产品是 Harness，不是模型？ (waiting for Michael's review)
Platform: xhs · Length: 48.4 s · Folder: videos/2026-11-14-harness · Style: B · screen tutorial (dark editor window "harness-notes.md") with 小Lin说-style teaching cards (credited article card + highlighter, term = plain words, horse/harness analogy, opinion labeled 我觉得)
Teaches the WeChat article "Harness才是产品：生产级AI Agent设计的12个要点" (忽南忽北Wq, 2026-10-21), credited on screen. Michael first asked for his avatar; HeyGen had no twin (free plan, none created), so he chose no-avatar mode. Script 2 of 2 (reviewer's pick). One HeyGen take, zh, pace 0.92, karaoke + push, music bed reused from how-i-make plus 6 sound cues.
Script: 做 Agent，真正的产品其实不是模型。最近读到一篇讲 Agent 架构的长文，说的就是 Harness。Agent 是能自己调工具办事的 AI，Harness 是模型周围的一切。好比模型是马，Harness 是马具。马具不会让马更聪明，但能让它真正干活。比如工具别全塞给模型，让它按任务去找。知识按需加载，先看名字，用到再读全文。高风险操作由系统拦住，不靠模型在聊天里问一句。我用的 Claude Code 也是这样，技能按需加载，危险操作先确认。但是只有五个工具、任务又短的小应用，直接给就行。我觉得，模型会换，Harness 才留得下。你做 Agent 最头疼哪一块？
Render: renders/2026-11-14-harness_2026-11-14_00-14-05.mp4
What to improve next time: in zsh write `${F}[v]` in ffmpeg filter strings (`$F[v]` is read as an array index and the mix fails silently behind `&&`); mp.weixin.qq.com blocks plain fetches but opens in the built-in browser; the article's company examples (funding, product launches) were left out because we couldn't verify them.

### 2026-11-14 — Harness re-styled: preset E "Sticky-note whiteboard" (published on Xiaohongshu 2026-11-14)
Render: renders/2026-11-14-harness-sticky_2026-11-14_00-19-16.mp4 (xhs upload copy: renders/harness-sticky-xhs.mp4). Note: x-assistant/xhs-harness-post.md.
Michael's feedback on the dark version: change the style, that one has been used many times. Same take, script, timing and audio mix (no new HeyGen call); only the visuals changed. New preset E added to brand/DESIGN.md: white dotted board, colored sticky notes, taped paper, red marker badges, drawn rings. Folder: videos/2026-11-14-harness-sticky · Length 48.4 s. The dark version is untouched in videos/2026-11-14-harness/.
What to improve next time: before building, list which looks the platform has already had (dark HUD ×3 on xhs by now) and pick an unused one first; this Mac has no Chinese handwriting font, so "hand-written" looks must rely on notes, tape and drawn strokes, not type.

## 2026-11-14 — 你敢让 Agent 在你电脑上自己跑命令吗？（开源 Harness 四大流派）(published on Xiaohongshu 2026-11-14)
Platform: xhs · Length: 53.4 s · Folder: videos/2026-11-14-harness-anime · Style: F · anime story (new preset: full-frame AI anime pictures, four characters for the four schools, dojo-sign banners, speed lines, karaoke captions)
Teaches the WeChat article "开源 Agent Harness 四大流派：OpenHands / DSH / Pi / Hermes" (公众号 AI汇览, 2026-10-18), credited on a card in scene 2 and in the footer. Facts come from the article only; the four projects were not checked first-hand, so DSH stays "官方说" and the script says "这四个我没用过，只是转述". Script 2 of 2 (reviewer's pick, Michael chose it). One HeyGen take, zh, pace 0.92. 7 Buzzy images (Nano Banana 2), no retries; the group shot was the reference image for the four single-character pictures. Music bed reused from how-i-make plus 6 sound cues.
Script: 你敢让 Agent，在你电脑上自己跑命令吗？最近读到 AI 汇览的一篇文章，讲开源 Harness 的四大流派。Harness，就是模型外面那层软件。工位派 OpenHands，管活在哪儿跑。注意，不开沙箱，它就直接跑在你机器上。插件派 DSH，官方说一切皆插件。但卸载插件，撤不回它做过的事。极简派 Pi，核心很薄，故意不做子 Agent。它没有内置权限系统，沿用启动者的权限。成长派 Hermes，会从经验里攒技能。可这是记忆，不是训练模型，也会记错。文章说，这只是一种看法，特点会重叠。这四个我没用过，只是转述。我每天用 Claude Code，危险操作会先问我。选哪派，先看你卡在哪。你最近一次没敢让 Agent 继续执行，卡在哪一步？
Render: renders/2026-11-14-harness-anime_2026-11-14_12-06-07.mp4 (xhs upload copy: renders/harness-anime-xhs.mp4). Note: x-assistant/xhs-harness-anime-post.md.
What to improve next time: ask the image model for the subject larger in frame (the characters came out small, so every scene needs a 1.2–1.9× camera zoom); cards must not repeat the caption (changed four of them to add a detail from the article instead); a card needs about 0.5 s + 0.3 s per word on screen, so place it on an earlier spoken word when the scene is short; keep the footer under about 40 characters or it runs off the right edge.

## 2026-11-14 — 新加坡收入最高的 10 个行业 (published on Xiaohongshu 2026-11-14)
Platform: xhs · Length: 43.1 s · Folder: videos/2026-11-14-sg-top-income · Style: A · market news, chart-led (one ranked bar chart that stays on screen and grows bar by bar on each spoken name, a red median line, a "只有 5 个" stamp)
Facts: MOM Labour Force in Singapore 2025, Table C5 (median gross monthly income of full-time residents, incl. employer CPF), read from the two official Excel files with code; see RESEARCH.md. The catch-all "Others" group (6,362) is left out of the ranking and named in the chart footer. Script 2 of 2 (reviewer's pick, Michael chose it). One HeyGen take, zh, pace 0.92, karaoke + push + cut. Music bed reused from how-i-make plus 5 sound cues.
Script: 你猜，新加坡哪个行业，收入最高？第一名，金融与保险，中位数九千二百五十八新币。第二，信息与通讯。第三，公共行政与教育。第四到第七，专业服务，制造业，医疗与社会服务，批发与零售。第八到第十，艺术娱乐与休闲，房地产服务，建筑业。全行业的中位数，是五千七百七十五新币。这十个里，只有前五名高过它。数据来自新加坡人力部，二零二五年。只算全职的公民和永久居民，含雇主公积金。这是整个行业的数字，不是职位工资。你觉得，自己的行业排第几？
Render: renders/2026-11-14-sg-top-income_2026-11-14_23-04-09.mp4
What to improve next time: a layer that must stay across several sentences (the chart) lives outside the .scene divs and is shown and hidden by hand with word anchors; AT keys are single Chinese characters, so index.html has an at("短语") helper that finds a spoken phrase instead of counting "业.3"; keep bar value labels clear of any line drawn across the chart.

## 2026-11-15 — 微软宕机，是被黑了吗？（根本原因后续）(APPROVED, published on Xiaohongshu 2026-11-15)
Platform: xhs · Length: 58.4 s · Folder: videos/2026-11-14-msft-root-cause · Style: E · sticky-note whiteboard as an incident board (cause timeline, pipe analogy, 12-server grid, duration bar that stretches left to Microsoft's earlier start, 5 workday tiles)
Follow-up to 2026-11-13 微软宕机20多小时. Facts in RESEARCH.md: Microsoft's preliminary cause (earlier network capacity upgrade, surfaced after a recent network change; "not related to cyber or AI / agents"), read via an admin-center mirror and press quotes, so everything is labeled 初步 / 意译. Script 2 of 2 (reviewer's pick; Michael chose it over Telegram). One HeyGen take, zh, pace 0.92, karaoke + push. Music bed reused from how-i-make (looped) plus 8 sound cues.
Script: 微软宕机，是被黑了吗？微软的初步原因说，不是，也和 AI 无关。上次视频时，原因还没公布，这是更新。官方说，是之前网络扩容留下的问题。扩容，就是给网络加容量。它一直没事，直到最近一次网络改动，才暴露。比方，水管接头装歪了，平时不漏，后来换了个阀门，就漏了。具体是哪个问题，微软没说，所以现在只是初步原因。过程是这样：服务器没过健康检查，掉线了。剩下的更吃力，重启回来的，一来流量又倒。上次我说二十多个小时，是从公告发出算起。微软记录的起点更早，一共三十小时零五分。现在已恢复。微软承诺五个工作日内出最终报告，大约下周。我觉得，大故障常出在自己的改动，不一定是攻击。你觉得，公司该不该公开改动细节？
Render: renders/2026-11-14-msft-root-cause_2026-11-15_00-22-30.mp4 (xhs upload copy: renders/msft-root-cause-xhs.mp4). Note: x-assistant/xhs-msft-root-cause-post.md.
What to improve next time: an English acronym is one AT key ("ai"), so the at("短语") helper can't find it; use AT["ai"] directly. Stamps that sit on top of text need `data-layout-ignore` or check reports content_overlap. Run `check --json` with all output sent to /dev/null and read the saved report, or the progress lines flood the terminal.

## 2026-11-15 — 英伟达 vs AMD，谁更能涨？ (APPROVED, published on Xiaohongshu 2026-11-15)
Platform: xhs · Length: 56.9 s · Folder: videos/2026-11-15-nvda-vs-amd · Style: A · market news, chart-led (log-scale "$1 since 1999" line chart, 2016 bars, drawdown cards, 2026 columns, "since the 6 Oct high" chart, two paraphrased news cards, earnings calendar tile, two "我觉得" outlook cards)
Asked over Telegram. Data: Yahoo Finance daily adjusted closes to 2026-11-13, see RESEARCH.md and data/analyze.py. `index.html` is generated: edit `template.html.txt`, run `build.py`, then `sync.py --karaoke --push --cut`. Script written and checked by Claude in the main session (no scripter/reviewer agents, no script pick by Michael). One HeyGen take, zh, pace 0.92. Music bed reused from how-i-make (looped) plus 7 sound cues.
Script: 英伟达和 AMD，谁更能涨？我拉了上市以来的数据。一九九九年英伟达上市那天，各投一块钱。到今天，英伟达是四千三百块，AMD 只有五十块。但从二零一六年算，两家几乎打平，都是两百倍左右。代价是，英伟达最深跌过九成，AMD 跌过百分之九十七。今年反过来了，AMD 涨了一倍半，英伟达跌了百分之十二。十月六号两家同创新高，之后英伟达连跌六周，跌了三成。先是芯片股回调，十二号 CEO 黄仁勋又辞职。接下来，先看十七号英伟达的财报。我觉得，英伟达跌得急，短线可能反弹。但新 CEO 没定，难回高点。AMD 势头强，可估值更贵，两周里四次单日涨跌超一成。这只是我的看法，不是投资建议。你更看好谁？
Render: renders/2026-11-15-nvda-vs-amd_2026-11-15_00-41-26.mp4 (xhs upload copy: renders/nvda-vs-amd-xhs.mp4). Note draft: x-assistant/xhs-nvda-vs-amd-post.md.
What to improve next time: stooq.com now sits behind a bot check, so use Yahoo's chart endpoint for prices; a second root-level .html with data-composition-id fails check, so keep templates as .html.txt; captions that show digits for a longer spoken number ("97%" for 百分之九十七) leave karaoke targets missing, so show the spoken form.
