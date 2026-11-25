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

## 2026-11-15 — AI Agent一直在线？5个部件看懂 (APPROVED, published on Xiaohongshu 2026-11-15)
Platform: xhs · Length: 58.2 s · Folder: videos/2026-11-15-always-on-agents · Style: G · app-UI tutorial (new preset: chapter bar with five pills, a mock app screen per idea, a real screenshot of the article in a browser window, 一图看懂 cheat-sheet ending with 收藏这张图)
Teaches Anthropic's article "Building always-on agents" (William Hu, 2026-11-13); facts in RESEARCH.md. Script 1 of 2 (reviewer's pick, Michael chose it). One HeyGen take, zh, pace 0.92, karaoke + push. Music bed reused from how-i-make plus 7 sound cues. The storyboard was planned in E; Michael asked for a tutorial-only style after hearing the voice, so G was designed and built instead.
Script: 你的 Agent 看着一直在线，其实大部分时间在睡觉。这是 Anthropic 官方文章讲的，我用大白话讲一遍。一次运行就四步：事件来了，醒来干活，写回记录，接着睡。睡着的时候，一个 token 都不花。它靠五个部件。第一，收件箱。所有触发先排队，像前台收信。第二，闹钟。到点只往收件箱丢一条，不直接开跑。第三，记忆。就是一堆文件，只记它自己查不到的。第四，权限。每次调工具，放行、拦下，或者等你点头。第五，发件箱。发消息，这次不打扰你，或者先问你一句。文章说，风险最大的是权限。它拿着你的权限，没人盯着就在跑。所以密钥不交给它，由外面的代理来填。我每天用 Claude Code，所以想把这篇学明白。你最想让 Agent 在后台替你守着什么？
Render: renders/2026-11-15-always-on-agents_2026-11-15_09-49-54.mp4 (xhs upload copy: renders/always-on-agents-xhs.mp4). Note: x-assistant/xhs-always-on-agents-post.md.
What to improve next time: the nested `claude -p` in heygen_take.sh hit the default model's usage limit, so it now runs on Sonnet (TAKE_MODEL to override); an app-screen card must have its rows in at the start of its scene, not on a later word, or it sits empty for a second; a chapter bar and a cheat sheet that span several scenes live outside the .scene divs and are faded by hand.

## 2026-11-15 — 我的 Always-on Agent 实操（续集）(APPROVED v2, published on Xiaohongshu 2026-11-15 12:13)
Platform: xhs · Length: 59.9 s · Folder: videos/2026-11-15-stats-agent · Style: G · app-UI tutorial (same preset as the previous video on purpose: it's the follow-up, 理解 → 实操)
Shows the stats agent in agents/stats-agent built for real: the inbox table rows, the launchd timer, the 4 memory files, the allow-list, the outbox, the Full Disk Access pitfall, Michael's real Telegram message (cropped, no header), and the cost of the two runs. Facts in RESEARCH.md. Script 2 (the reviewer's pick, which Michael chose and asked to frame as a follow-up). One HeyGen take, zh, pace 0.92, karaoke + push. Music bed reused from how-i-make plus 7 sound cues.
Script: 给后台 Agent 开最省事的权限，我试过，没用。上个视频讲我的理解，这次是真实操：照 Anthropic 的文章，做了个盯小红书数据的 Agent。它看笔记发出后的二十四小时，值得说才发 Telegram。收件箱是个 SQLite 表。闹钟是 launchd，每十分钟看一次，没事就不叫醒模型。记忆是四个文件。权限是白名单，只读 Chrome，命令行和上传都拒绝。模型只给结果，数据特别好或特别差，才发提醒。问题来了：Mac 不让后台任务读文档文件夹。我开过完全磁盘访问权限，没解决。而且每个 Python 脚本，都能看所有文件。于是我把它搬进自己的文件夹，这个权限就用不着了。这是它发我的真实消息，最新五条笔记的数据。今天两次真跑，分别约两毛和三毛五美元。代码开源在 GitHub。如果是你，会开完全磁盘访问吗？
Render: renders/2026-11-15-stats-agent_2026-11-15_11-52-00.mp4
What to improve next time: the repo restructure broke the voice-video scripts' ffmpeg path (they used abspath through the .claude/skills symlink); fixed with realpath and one more `..`. The at() helper now splits English words, so at("telegram") works.
v2: Michael found the opening "最省事的权限" confusing (it named a permission the viewer hadn't met yet). Reordered so the story runs in order: result first (an Agent that watches my Xiaohongshu data), then 上集理解 → 这集实操, the five parts, the pitfall (now introduced as 做的时候踩了个坑), the real Telegram message, cost, and the question 你会让一直在线的 Agent，替你盯什么？ New HeyGen take, pace 0.92, 58.1 s. Render: renders/2026-11-15-stats-agent_2026-11-15_12-09-10.mp4. v1 kept in v1/.
What to improve next time: don't open on a detail the viewer can only understand later; open on what the thing does for them.

## 2026-11-15 — Anthropic 怎么做 Always-on Agent（工程解读 01，长视频精读）(draft, waiting for Michael)
Platform: xhs · Length: 209.4 s (3:29) · 16:9 · Folder: videos/2026-11-15-always-on-deep-dive · Style: H · article deep-dive (first video from the article-explainer skill)
Source: Anthropic "Building always-on agents" (William Hu, 2026-11-13), https://claude.com/resources/articles/building-always-on-agents. Facts in RESEARCH.md; 7 figures captured from the page into assets/. Outline approved; script approved with the "上次我用一分钟…" line removed (Michael wanted a standalone video, not a follow-up). 16 slides in 8 chapters: opening (78% / 40% cost bars), 一次 run, 收件箱, 定时器, 记忆, 权限, 发件箱, 合起来 + 留个问题.
Voice: 8 HeyGen chapter takes (takes.py split/merge, 0.7 s gaps), pace 0.92, no karaoke, no push. No music. index.html is generated: edit build.py, then run it and sync.py.
Render (v1, kept in v1/): 2026-11-15-always-on-deep-dive_2026-11-15_17-47-29.mp4. v2 render: renders/2026-11-15-always-on-deep-dive_2026-11-15_17-57-42.mp4 (216.9 s) (xhs upload copy: renders/always-on-deep-dive-xhs.mp4; cover: renders/cover.png). Note draft: x-assistant/xhs-always-on-deep-dive-post.md.
What to improve next time: a big number label on a tall bar can hit the heading above it (78% did); check every slide's busiest frame, not only its middle. Many captions are flagged line_unread because they follow the voice at speaking pace; that is expected here.
v2: Michael asked to drop the closing disclaimer ("没有测这套架构本身的效果" sounded like he hadn't tested anything) and instead briefly introduce the stats agent he posted today. New last line: 我照着这篇文章，自己做了一个一直在线的 Agent，替我盯小红书笔记的数据。收件箱是一张 SQLite 表，闹钟是 launchd，记忆是四个文件，值得说才发 Telegram。细节在我上一条视频里。+ the question. Only chapter 7 was re-recorded; the ending slide shows a 我照着做了一个 card with four part → tool chips above the question. Note updated to match.
v3: Michael asked to replace 细节在我上一条视频里 with 细节开源在 GitHub 上，地址在评论区, and to show the Telegram screenshot as the demo result. The ending is now two slides: 我照着做了一个 (2x2 part → tool grid, the real Telegram message from videos/2026-11-15-stats-agent/assets/telegram.png with a 真实消息 stamp, a GitHub chip) and the 留个问题 card. Chapter 7 re-recorded again. Render: renders/2026-11-15-always-on-deep-dive_2026-11-15_18-05-29.mp4 (220.8 s); v1/ and v2/ keep the earlier renders.

## 2026-11-15 — How Anthropic builds always-on agents (English, Chinese subtitles) (published on Xiaohongshu and X 2026-11-15)
Platform: xhs + x · Length: 218.4 s (3:38) · 16:9 · Folder: videos/2026-11-15-always-on-deep-dive-en · Style: H · article deep-dive
Same content as the approved Chinese v3 (videos/2026-11-15-always-on-deep-dive), translated: English voice (8 HeyGen chapter takes, en, pace 0.92) and English slides, with Chinese subtitles in the caption band. Each subtitle is a <div class="cap" data-say="<English clause>">中文</div>, so sync.py times the Chinese text on the English words; this worked first time. index.html and script.json are generated by build_en.py (it reuses the CSS from the Chinese build.py).
Render: renders/2026-11-15-always-on-deep-dive-en_2026-11-15_18-40-54.mp4 (upload copy: renders/always-on-deep-dive-en-upload.mp4, 4.7 MB). Notes: x-assistant/xhs-always-on-deep-dive-en-post.md; X post logged in x-assistant/posts.md.
What to improve next time: at("…") anchors must use whole HeyGen words; hyphenated words come back as one word ("long-horizon" → AT["longhorizon"]), so anchor on a plain word next to them. X accepted a 3:38 video on this account, so the 2:20 free-tier limit was not a problem.

## 2026-11-15 — AI 抢走工作了吗？Anthropic 查了数据 (v2 APPROVED, published on Xiaohongshu 2026-11-16)
Platform: xhs · Length: 55.5 s · Folder: videos/2026-11-15-ai-jobs · Style: C · bold type (one huge word or number per beat, new full-screen colour each scene, hard cuts, paper caption plate, source line on every scene)
Asked over Telegram as "the labour market impact of AI article Anthropic just published". No post newer than 16 Oct 2026 exists on Anthropic's Research, News, Institute or Economics pages (checked 2026-11-15), so the video uses "Labor market impacts of AI: A new measure and early evidence" (Massenkoff and McCrory, 2026-03-05) plus the 16 Oct posts "How employment is changing at Anthropic" and "The AI expectations gap". Michael was told this and asked to send a link if he meant another one. Facts were read by web-fetch subagents (paraphrased); numbers used: 94% vs 33% (computer and maths), programmers 75%, no clear unemployment rise since late 2022, ages 22–25 entry into exposed jobs about 14% slower and only barely significant, junior share of Anthropic technical staff 21% to 14%. One HeyGen take, zh, pace 0.92, karaoke + push + cut. Music bed reused from how-i-make plus 7 sound cues.
Script: AI 到底有没有抢走工作？Anthropic 查了数据。他们提出一个新指标：观测暴露度。对比的是，AI 理论上能做的，和人们真用来做的。计算机和数学类工作，理论上能做百分之九十四。实际用到的，只有百分之三十三。暴露最高的是程序员，覆盖率百分之七十五。研究发现，高暴露职业的失业率，没有明显上升。但有个小信号：二十二到二十五岁的人，进入这类岗位的速度，慢了百分之十四。研究说，这个结果刚刚勉强显著，别过度解读。十月的更新里，Anthropic 自己，初级技术员工占比，从百分之二十一降到百分之十四。但它是特殊的公司，不能代表整个经济。我觉得，目前更像招聘放缓，还不是大规模失业。你觉得，哪类岗位会先受影响？
Render: renders/2026-11-15-ai-jobs_2026-11-15_23-27-37.mp4 (xhs upload copy: renders/ai-jobs-xhs.mp4). Note draft: x-assistant/xhs-ai-jobs-post.md.
What to improve next time: check the title length with count.py BEFORE telling Michael the title (it was 23, then 21, then fixed to 19); a full-screen scene must not use `visibility:visible` in CSS (lint error gsap_fullscreen_overlay_starts_visible), let the sync block show it; give a scene colour strip below the source bar enough height (480 px).

Version 2 (2026-11-15): Michael said the per-occupation percentages were missing and important. Added a ranked chart of Figure 3 "Most exposed occupations" (exact values read from the article's table in Chrome: programmers 74.5, customer service 70.1, data entry 67.1, medical records 66.7, market research 64.8, sales reps 62.8, financial analysts 57.2, software QA 51.9, information security 48.6, computer user support 46.8) plus the 30% zero-exposure note. Figure 2 (radar by occupation category) has no printed values, so only the values stated in the text are used. New script and take (12 sentences, 62.3 s). v1 kept in v1/. Render: renders/2026-11-15-ai-jobs_2026-11-15_23-36-36.mp4 (upload copy: renders/ai-jobs-v2-xhs.mp4).
What to improve next time: read the article's own figures first (the Anthropic page shows Figure 3 as a table image that Chrome can zoom; PDFs from WebFetch come back as raw bytes and this Mac has no pdftoppm), instead of relying on a summary of the text; when a viewer asks for "the numbers", put every one on screen and speak only the first and last.
Published note: tags needed care. Typing "#tag" + Return picks the FIRST suggestion, which can be a different topic ("#职场" gave "职场经验howto"; "#AI" offers "新建话题" first). Take a screenshot after each tag and click the suggestion whose name matches exactly, then read the tags back from the editor text.

## 2026-11-16 — Anthropic：Agent 记忆怎么做（工程解读 02，长视频精读）(draft, waiting for Michael)
Platform: xhs · Length: 384.4 s (6:24) · 16:9 · Folder: videos/2026-11-16-agent-memory · Style: H · article deep-dive
Source: Anthropic Engineering "The components of agent memory" (Lance Martin, 2026-11-06), https://www.anthropic.com/research/components-of-agent-memory. Facts in RESEARCH.md; 6 figures (1, 3, 4, 7, 10, 14) screenshotted from the page into assets/. Asked over Telegram ("make a tutorial video based on this article"). Outline approved; script approved as written (14 slides, 8 chapters + opening); voice approved after the first 92 s.
Voice: 9 HeyGen chapter takes (takes.py split/merge, 0.7 s gaps), pace 0.92, no karaoke, no music. 1,860 characters came out at 6:24, not the 5.6 min I estimated (chapter gaps and pace add time). index.html is generated: edit build.py, run it, then sync.py.
Render: renders/2026-11-16-agent-memory_2026-11-17_08-58-43.mp4 (xhs upload copy: renders/agent-memory-xhs.mp4, 6.6 MB; cover: renders/cover.png). Note: x-assistant/xhs-agent-memory-post.md.
What to improve next time: (1) a usage limit hit mid-run and chapters 5-8 failed; takes.py keeps finished chapters, so only rerun the failed ones. (2) heygen_take.sh's nested session retypes words.json by hand, so spot-check it. (3) caption ids are c0..cN: never give a slide element an id like c13 (my chip vanished until I renamed it). (4) the subagent that read the page returned figure numbers that were not in the text; only the ones I read off the images were used.

## 2026-11-17 — 新加坡工作准证全解析2027 (published on Xiaohongshu 2026-11-17)
Platform: xhs · Length: 319.9 s (5:19) · 9:16 · Folder: videos/2026-11-17-sg-work-passes · Style: G · app-UI tutorial (29 scenes, chapter bar of 5 pills, mock cards, cheat-sheet ending)
Source: MOM and EDB pages read 2026-11-17 (facts and page dates in RESEARCH.md). Script SCRIPT.md (reviewed by video-reviewer, 19 fixes); voice: one take, "S Pass" written 艾斯 Pass so the S is a separate letter.
Render: renders/2026-11-17-sg-work-passes_2026-11-17_12-12-07.mp4 (xhs upload copy: renders/sg-work-passes-xhs.mp4, 8.4 MB). Note: x-assistant/xhs-sg-work-passes-post.md.
What to improve next time: the nested HeyGen session could not save words.json (shell approval); I pulled the audio URL and original_words from the saved MCP response. Plan the script to about 4 minutes (it came out 5:19, and 29 scenes took many rounds of layout fixes); add a real MOM screenshot if wanted.

## 2026-11-17 — 从零做一个 Agent · 第 1 集：循环 (published on Xiaohongshu 2026-11-17, landscape)
Platform: xhs · Length: 454.3 s (7:34) · 16:9 · Folder: videos/2026-11-17-agent-ep1-landscape · Style: H · article deep-dive + chart-draw diagrams (6 staged SVGs from diagrams.py). A vertical dark-editor version is in videos/2026-11-17-agent-ep1 (not posted; Michael chose landscape).
Source: Claude Code docs (how it works, agent loop, tools reference), Anthropic "Building effective agents"; code in series/agent-from-scratch/ep01 (agent.py, test_loop.py, demo outputs from a real deepseek-flash run). Script: series/EP1-SCRIPT.md (reviewed, 14 fixes). Voice: one take 7:34 pace 0.92.
Render: renders/2026-11-17-agent-ep1-landscape_2026-11-17_15-10-45.mp4 (upload copy renders/agent-ep1-landscape-upload.mp4). Note: x-assistant/xhs-agent-series-ep1-post.md.
What to improve next time: the nested HeyGen session can't save words.json (needs shell approval), so I extract the audio URL and original_words from the saved MCP response by hand; the sequence diagram's text is small (8 messages in one slide); 7:34 vs the 8 min target.
Update 2026-11-17 (episode 1, landscape): cover restyled from green to the beige/orange look of the chart-draw diagrams (Michael's request); master re-rendered as renders/2026-11-17-agent-ep1-landscape_2026-11-17_17-30-53.mp4 (upload copy renders/agent-ep1-landscape-upload.mp4, 9.5 MB). The live Xiaohongshu note keeps the earlier render on purpose. The old render is in renders/old/. An English script exists (series/EP1-SCRIPT-EN.md) but no English video was made.

## 2026-11-17 — 从零做一个 Agent · 第 2 集：工具 (published on Xiaohongshu 2026-11-17, landscape)
Platform: xhs · Length: 430.5 s (7:11) · 16:9 · Folder: videos/2026-11-17-agent-ep2 · Style: H · article deep-dive + 8 staged chart-draw diagrams (diagrams.py)
Source: Claude Code docs (tools reference, Edit/Bash behaviour), Anthropic tool-writing engineering article; code in series/agent-from-scratch/ep02 (agent.py, test_tools.py, demo runs run-fix and run-recover with deepseek-flash). Script: series/EP2-SCRIPT.md (v2, reviewed). Voice: one take, pace 0.92.
Render: renders/…18-02-15.mp4 (upload copy renders/agent-ep2-upload.mp4, 8.8 MB, volume -1.5 dB). Note: x-assistant/xhs-agent-series-ep2-post.md.
What to improve next time: the ep2 voice was not explicitly confirmed before posting (Michael approved the note text and said post); the note says the repo is not public yet, so edit it once the repo is public.

## 2026-11-17 — 从零做一个 Agent · 第 3 集：笔记 (scheduled on Xiaohongshu for 2026-11-18 09:00)
Platform: xhs · Length: 423.3 s (7:03) · 16:9 · Folder: videos/2026-11-17-agent-ep3 · Style: H · article deep-dive + 5 staged chart-draw diagrams (diagrams.py)
Source: Claude Code docs (Memory, Best practices), Anthropic prompting guide (system prompt role); code in series/agent-from-scratch/ep03 (agent.py, test_prompt.py, evals.py, demo runs with deepseek-flash). Script: series/EP3-SCRIPT.md (v2, reviewed, 15 fixes), research notes series/EP3-RESEARCH.md. Voice: six chapter takes merged, pace 0.92.
Render: renders/2026-11-17-agent-ep3_2026-11-17_22-05-45.mp4 (upload copy renders/agent-ep3-upload.mp4, 9.0 MB, volume -1.5 dB). Note: x-assistant/xhs-agent-series-ep3-post.md. Article and diagrams are in the repo (articles/ep03-system-prompt-and-notes.md).
What to improve next time: the chapter 2 take failed on the first try and worked on the second; the terminal slides for the two demo runs are small (15 lines at 26 px); the repo's articles were edited on GitHub by Michael (byline), so pull before pushing.

## 2026-11-17 — 从零做一个 Agent · 第 4 集：权限 (scheduled on Xiaohongshu and YouTube for 2026-11-18 12:00)
Platform: xhs · Length: 445.5 s (7:25) · 16:9 · Folder: videos/2026-11-17-agent-ep4 · Style: H · article deep-dive + 7 staged chart-draw diagrams (diagrams.py)
Source: Claude Code docs (Permissions, Permission modes, Security, Best practices, Settings); code in series/agent-from-scratch/ep04 (agent.py gate, test_permissions.py, demos.py, demo runs: injection 12 real runs, fooled scripted model, fatigue 6 runs). Script: series/EP4-SCRIPT.md (v2, reviewed, 19 items), research notes series/EP4-RESEARCH.md. Voice: five chapter takes merged, pace 0.92.
Render: renders/2026-11-17-agent-ep4_2026-11-17_23-35-51.mp4 (upload copy renders/agent-ep4-upload.mp4, 9.1 MB). Note: x-assistant/xhs-agent-series-ep4-post.md. Article and diagrams pushed to the repo (articles/ep04-permissions.md).
What to improve next time: the video does not mention that our project rule file is loaded without a trust step (the article does); the Y/A/N cards appear late in the scene; the "fooled model" is scripted, so the slides say so on screen.

## 2026-11-18 — 从零做一个 Agent · 第 5 集：上下文 (scheduled 2026-11-18 19:00 on Xiaohongshu and YouTube)
Platform: xhs (+ YouTube if he wants) · Length: 358.1 s (5:58) · 16:9 · Folder: videos/2026-11-18-agent-ep5 · Style: H · article deep-dive + 5 staged diagrams (diagrams.py, incl. the real tokens-per-turn chart)
Source: Claude Code docs (Context window, How Claude Code works, Costs, Commands), Anthropic engineering post "Effective context engineering for AI agents", Claude API docs (context windows, token counting, context editing); code in series/agent-from-scratch/ep05 (agent.py context manager, test_context.py, demos.py; 12 real DeepSeek runs in demo/repeat). Script: series/EP5-SCRIPT.md (v2, reviewed, 24 items), research notes series/EP5-RESEARCH.md, outline series/EP5-OUTLINE.md. Voice: nine chapter takes merged, pace 0.92.
Render: renders/2026-11-18-agent-ep5_2026-11-18_13-46-12.mp4 (upload copy renders/agent-ep5-upload.mp4, 7.9 MB). Note: x-assistant/xhs-agent-series-ep5-post.md.
Notes: HeyGen no longer accepts voice_model heygen-voice-1-turbo-free; heygen_take.sh now leaves the model out (plugin avatar-video 0.3.1). Only 3 real runs per setup; the "both" setup failed once (60-turn limit), clearing alone failed in the first version until the system prompt told the model to write findings in its replies.
What to improve next time: many slides are cards on a mostly empty stage; the chart shows only the first run of each setup; the humanizer pass was not run on the note.

## 2026-11-19 — 从零做一个 Agent · 第 6 集：计划模式和任务清单 (published 2026-11-19 on Xiaohongshu and YouTube)
Platform: xhs + YouTube · Length: 313.4 s (5:13) · 16:9 · Folder: videos/2026-11-19-agent-ep6 · Style: H · article deep-dive + 3 staged diagrams (diagrams.py)
Source: Claude Code docs (Permission modes, Interactive mode, Tools reference, Best practices), Anthropic engineering post "Effective harnesses for long-running agents"; code in agent-from-scratch/ep06 (agent.py plan mode + todo_write, test_plan.py, demos.py; real DeepSeek runs in demo/: work 5 per setup, hard 5, easy 3). Script: series/EP6-SCRIPT.md, research series/EP6-RESEARCH.md, outline series/EP6-OUTLINE.md. Voice: ten chapter takes merged, pace 0.92.
Render: renders/2026-11-19-agent-ep6_2026-11-19_00-25-15.mp4 (upload copy renders/agent-ep6-upload.mp4, 6.4 MB). Notes: x-assistant/xhs-agent-series-ep6-post.md, x-assistant/yt-agent-series-ep6-post.md.
Result: plain 59/60 (mean 15.2 turns), todo 60/60 (29.6), plan+todo 60/60 (27.2); only 5 runs per setup, so no claim that the list is more accurate; the list roughly doubles the turns.
What to improve next time: ep06 code and article are not on GitHub yet; the humanizer pass was not run on the texts; no real "plan never checked off" case could be shown.

## 2026-11-19 — 从零做一个 Agent · 第 6 集 v2：计划模式和任务清单（重做，本地版，未发布）
Platform: xhs + YouTube (PUBLISHED 2026-11-19; XHS old note and old YouTube video deleted first) · Length: 326.8 s (5:27) · 16:9 · Folder: videos/2026-11-19-agent-ep6-v2 · Style: H · article deep-dive + 7 staged diagrams (4 new concept diagrams D1-D4: no-plan agent, plan mode vs diving in, task list states, before/during/after)
Why: Michael (2026-11-19): v1 never explained what plan mode and the task list are, why an agent needs them, or how they help; viewers don't know them. v1 (ep6) was deleted from YouTube the same morning; the XHS note is still up (Michael: don't delete yet, update locally first).
Script: series/EP6-SCRIPT.md (v2, reviewed by video-reviewer, Michael OK'd 2026-11-19); v1 kept as series/EP6-SCRIPT-v1.md. Numbers re-checked against ep06/demo/*.json. Voice: eleven chapter takes merged, pace 0.92.
Render: renders/2026-11-19-agent-ep6-v2_2026-11-19_09-33-45.mp4 (18.5 MB). Added later at Michael's request: 3 test-intro slides before the results (repo and 12 faults, task and scoring, the three setups); before/after code slides for the two pitfalls (the first-version code was never saved, so the left side was rewritten with both bugs put back and verified: test 1 and test 6 of test_plan.py fail on it, all pass on the real agent.py; file in assets/first-version-agent.py). Status: waiting for Michael's verdict.
What to improve next time: shorter than v1 (4:20 vs 5:13) because the explainer chapters are tight; the humanizer pass was not run; chips under diagrams are small.

## 2026-11-21 — 从零做一个 Agent · 第 12 集：测试和调试
Platform: xhs + YouTube (PUBLISHED 2026-11-21, public now) · Length: 500.3 s (8:20) · 16:9 · Folder: videos/2026-11-21-agent-ep12 · Style: H · article deep-dive + 8 staged diagram sets (+ 8 card scenes)
Source: Anthropic Engineering, "Demystifying evals for AI agents" (2026-01-09) + Claude Code docs (CLI reference read in full) + our own eval harness: 4 tasks x 2 setups x 5 trials = 40 real runs (DeepSeek).
Script: series/EP12-SCRIPT.md (36 slides, reviewed by video-reviewer, 8 fixes applied, Michael OK'd 2026-11-21). Numbers by code: facts.py -> facts.json (check_facts clean for script and both post texts). Voice: nine chapter takes merged, pace 0.92.
Render: renders/2026-11-21-agent-ep12_2026-11-21_11-01-24.mp4 (26.8 MB). YouTube: https://youtu.be/bruLz7bm0P8.
Result of the test shown: the one-sentence change did not help (base 20/20, with the sentence 18/20; tasks too easy, baseline saturated). Real pit: a rigid grader failed a correct answer.
What to improve next time: the humanizer pass was not run on the post texts; the XHS title was 21 characters and needed one comma removed; harder tasks would let a change show a difference; the contact sheets are labelled by time, not slide number.

## 2026-11-21 — 从零做一个 Agent · 第 13 集（终章）：把它们接在一起
Platform: xhs + YouTube (PUBLISHED 2026-11-21, public now) · Length: 687.9 s (11:28) · 16:9 · Folder: videos/2026-11-21-agent-ep13 (+ videos/2026-11-21-agent-ep13-demo for the recorded terminal session) · Style: H · article deep-dive + 10 chapters, 51 slides, one persistent terminal window in chapter 05
Source: Claude Code docs (interactive mode, how it works, sessions, checkpointing, commands, security, sandboxing, sub-agents, headless) + Anthropic streaming docs + our own chat loop (agent-from-scratch/ep13: repl.py, agent.py, 38 checks with a fake model, 30 real runs on DeepSeek, a real recorded terminal session).
Script: series/EP13-SCRIPT.md (51 segments, reviewed by video-reviewer, 8 fixes; Michael OK'd 2026-11-21). Numbers by code: facts.py -> facts.json. Voice: ten chapter takes plus the demo narration take (reused), pace 0.92. YouTube: https://youtu.be/yhImrMlX79o.
Also made: a series 2 plan (series/SERIES2-PLAN.md, a draft: enterprise-class AI agent, 13 episodes) and research notes (SERIES2-RESEARCH.md).
Results shown: kept chat vs fresh: "list the files you changed" 5/5 vs 0/5; streaming first text 5.1 s vs 7.04 s, total 7.44 vs 7.04; Ctrl+C repair 4/5 vs 0/5; resume 5/5.
What to improve next time: the humanizer pass was not run on the post texts; segment 18 ("不用 API key 就能跑") can read as if the whole test needs no key (it means the 38 checks with a fake model); two heygen_take.sh nested sessions could not save big responses (recovered from the saved response); the Ctrl+C was simulated by raising KeyboardInterrupt in the real-run test (the recorded demo used a real Ctrl+C byte); the 720p upload copy is soft (11-minute video under the 10 MB upload limit).

## 2026-11-24 · agent-s2-intro (series 2 intro: 企业级 Agent 导读)
Platform: xhs + YouTube (PUBLISHED 2026-11-24, public) · Length: 471.2 s (7:51) · 16:9 · Folder: videos/2026-11-24-agent-s2-intro · Style: series 2 dark console look (navy + cyan; series 1 stays cream and crimson)
Source: PRD v1.1, TRD v1.1, prototype v1.0 (public repo build-an-enterprise-class-agent) + series/SERIES2-VERIFICATION.md. Design only, nothing built; no run results shown.
Script: series/SERIES2-INTRO-SCRIPT.md (36 segments, reviewed by video-reviewer, all must-fix applied; Michael OK'd 2026-11-24). Voice: nine chapter takes, pace 0.92. YouTube: https://youtu.be/2yRzU4ov3Zs
What to improve next time: slides had an empty stage for 3 to 8 s at the start of some scenes (first element appeared on a late phrase); fixed by showing the first element at the first words. Chapter-bar colours are hard-coded in the template and had to be patched in build.py for the dark look. A "A P I" phrase did not match after the real voice, because HeyGen joins spaced capitals into "API".

## 2026-11-24 · github-top-skills (10 office-work skills on GitHub)
Platform: xhs + X (PUBLISHED 2026-11-24) · Length: 108.4 s (1:48) · 9:16 · Folder: videos/2026-11-24-github-top-skills · Style: G · app-UI cards (no avatar; countdown bar 10 to 1)
Source: GitHub API stars read 2026-11-24 about 12:30 SGT (candidates.json, table.md), READMEs (readmes/), SKILL.md counts by treeless clone. Michael chose list A (everyday knowledge work, 2026-11-24 "1") and asked for less grouping talk and no ending (sentences 31 to 33 cut).
Script: SCRIPT-v2-final-draft.md sentences 1 to 30 (reviewed by video-reviewer twice, all must-fix applied; Michael OK'd). Voice: one take, pace 0.92, 108 s.
What to improve next time: the first voice take failed to save (large response), recovered from the saved HeyGen tool-result file; a spaced "P P T" becomes "PPT" in the word timings so card phrases must use han words; the first sentence also contained "第十名", so the countdown bar appeared too early until I used the second occurrence; the repo list was built from topic searches only (stars change daily); the video is longer than the usual 30 to 35 s on X.

## 2026-11-24 · sg-education (Singapore public education for an international child, parents' guide)
Platform: xhs only (PUBLISHED 2026-11-24 about 19:35 SGT) · Length: 283.0 s (4:43) · 9:16 · Folder: videos/2026-11-24-sg-education · Style: G · app-UI cards (staircase diagram of the school ladder, chapter bar 全貌/怎么进/毕业后/学费, fee bars)
Source: official pages read 2026-11-24: MOE (international students, AEIS, S-AEIS, P1, fees press release 2023, courses, JAE), NUS UGTuition PDF, NTU tuition and important-dates pages, Singapore Polytechnic fees page. RESEARCH.md lists what is NOT confirmed (SMU fees, other four polytechnics, ITE and O-Level for international students, 2027 monthly fees).
Script: script.json, 34 lines (v2 29 lines approved by Michael, then 5 lines on N/O/A Level added at his request, option B). Voice: one take, pace 0.92. Earlier 4:03 version kept in v1-4min/.
What to improve next time: the research relied on subagent fetches, so quotes should be checked on the page; the HeyGen take failed to save again (recovered from the saved response); a topic with no existing tag (#新加坡留学) cannot be linked on Xiaohongshu, check topics before approving the text; the same preset G was used twice on one day; I wrote "English tip: none" twice against the rule; the first estimate of the new section's time was a guess, read times from timing.json.

## 2026-11-24 · psle-explained (PSLE explained for parents)
Platform: xhs only (PUBLISHED 2026-11-24 about 21:30 SGT) · Length: 172.5 s (2:52) · 9:16 · Folder: videos/2026-11-24-psle-explained · Style: G · app-UI cards (AL table, 3+2+1+2=8 sum, citizenship ladder, Posting Group table that builds row by row, chapter bar 是什么/怎么算/选学校/分组)
Source: SEAB (about-psle, important dates, 2026 exam timetable PDF), MOE (PSLE scoring system, S1 posting, how posting works, posting groups, Full SBB). RESEARCH.md: whether international students sit PSLE is NOT FOUND, so the line was cut at Michael's request.
Script: script.json, 32 lines (33 proposed, line on international students removed by Michael). Voice: one take, pace 0.92.
What to improve next time: scene cards with a head chip showed an empty white card before the first row; fixed by popping the card with its first row (rows_scene in build.py). The first contact sheets were sent before two small fixes (card 7 wrap, SEAB wording), so say so; the subagent first mislabelled 18 Dec as the PSLE results date, check dates on the page.

## 2026-11-25 · sg-edu-opinion (Singapore education: official data + Michael's view)
Platform: xhs only (SCHEDULED for 2026-11-25 12:30 SGT as v3) · Length: v3 133.5 s (2:14); v2 was 184.7 s (3:05) · 9:16 · Folder: videos/2026-11-24-sg-edu-opinion · Style: G · app-UI cards (PISA and TIMSS ranking tables, chapter bar 数据/改革/问题/我的看法)
Source: MOE PISA 2022 press release and Annex A1, TIMSS 2023 official exhibits, MOE parliamentary replies and COS 2025 (RESEARCH.md). Opinion lines are labelled on screen.
Script: script.json, 29 lines (v1 26 lines approved 2026-11-24, ranking-table lines 4, 7, 9 and cards approved 2026-11-25). Voice: one take, pace 0.92. Ending tail 1.8 s. Captions show digits.
Render: renders/2026-11-24-sg-edu-opinion_2026-11-25_09-17-14.mp4
Change 2026-11-25 (Michael: 去掉我的看法, keep the others): v3, 20 lines, opinion section (old lines 20-28) removed, line 2 reworded, 3 chapter tabs. Previous 29-line version kept in v2-with-opinion/. Cards sent for approval before the new voice take.
v3 APPROVED (script and cards, Michael 'OK' 2026-11-25) and rendered: renders/2026-11-24-sg-edu-opinion_2026-11-25_09-27-06.mp4, new voice take at pace 0.92; the v2 takes are in v2-with-opinion/.
What to improve next time: Michael dropped the opinion section after seeing the full video, so ask whether he wants an opinion part before writing one; the card text 「2024 年中一起」 reads like mid-2024, write 「从 2024 年的中一开始」 as in the post.

## 2026-11-25 · ai-words-cartoon (11 AI words explained with a cartoon robot)
Platform: xhs (rendered, waiting for Michael's verdict on the video, text and slot) · Length: 84.9 s (1:25) · 9:16 · Folder: videos/2026-11-25-ai-words-cartoon · Style: cartoon doodle (new look, drawn in SVG by build.py: cream dotted paper, ink outlines, a robot mascot, one chain from AI to Agent, cheat sheet at the end)
Request: Michael, Telegram, "cartoon style" for AI, AI Agent and common AI words. References seen on search pages only (RESEARCH.md).
Script: script.json, 14 lines, written without the video-scripter / video-reviewer agents; approved by Michael ("Okay", then "Ok" for the cards). Voice: one take, pace 0.92, the 0.93 s pause after line 1 cut by 0.42 s (.voice-heygen-full-0.92-trim). Ending tail 3 s.
Render: renders/2026-11-25-ai-words-cartoon_2026-11-25_09-51-13.mp4 (xhs upload copy: renders/ai-words-xhs.mp4)
What to improve next time: HeyGen may return "AI" as one word, so build.py matches beats letter by letter.

## 2026-11-25 · ai-words-manga (same script and voice as ai-words-cartoon, black-and-white manga)
Platform: xhs (rendered, waiting for Michael's verdict and slot) · Length: 84.9 s (1:25) · 9:16 · Folder: videos/2026-11-25-ai-words-manga · Style: manga (comic demo B, chosen by Michael over American comic and cute 4-panel; comic-demos/ in the cartoon folder): panels that appear on spoken words, screentone, speed lines, sound words, black caption bars, hard cuts
Render: renders/2026-11-25-ai-words-manga_2026-11-25_10-01-51.mp4 (xhs upload copy: renders/ai-words-manga-xhs.mp4). Post text: x-assistant/xhs-ai-words-cartoon-post.md (卡通 changed to 漫画).
This version replaces ai-words-cartoon, which was not posted.
What to improve next time: offer style demos before drawing all scenes; a speech balloon needs a visible speaker in the same panel.


## 2026-11-25 — AI words, whiteboard hand-drawing demo (one scene: Agent)
Platform: xhs · Length: 9 s · Folder: videos/2026-11-25-ai-words-handdraw-demo · Demo only, not posted.
Michael sent a Xiaohongshu whiteboard-drawing tutorial and asked for the AI words video in that style. Same voice (cut from the manga version), 1 line drawing + 1 green-screen hand (Buzzy, Nano Banana 2); `build.py` uncovers each drawing along a zigzag over its inked area with the hand following; `key.py` removes the green. Render: renders/2026-11-25-ai-words-handdraw-demo_2026-11-25_13-00-09.mp4.
v2 (same day): Michael said the arm was too long at the top left. Now a mirrored hand draws the left column and the right hand the right column, with a much smaller arm stretch (2.5, was 7). Render: renders/2026-11-25-ai-words-handdraw-demo_2026-11-25_13-03-51.mp4.
What to improve next time: bring the hand in from the nearest side so only a short arm shows; waiting for his verdict on v2.

## 2026-11-25 — AI words, whiteboard hand-drawing, full video
Platform: xhs · Length: 85 s · Folder: videos/2026-11-25-ai-words-handdraw · APPROVED (Michael: "Post it on xhs"); scheduled for Thu 2026-11-26 20:30 with a cover made from the 5.05 s frame (renders/cover-3x4.png).
Same script, voice and timing as the manga version. 14 boards: 12 new line drawings (Buzzy, Nano Banana 2, 3:4, 2K, no retries) + the demo's Agent drawing and hand; the last board is a text list drawn by code. `build.py` finds each drawing's box, times it on the spoken words, uses a right hand for the right column and a mirrored hand for the left, and builds captions from `words.json`. Check passed (only short-caption "line_unread" warnings, captions follow the voice); qa: 84.9 s, peak -1.5 dB, no long silences. Render: renders/2026-11-25-ai-words-handdraw_2026-11-25_13-10-38.mp4; upload copy renders/ai-words-handdraw-xhs.mp4.
What to improve next time: ask for exactly the grid wanted; 3 of 12 pictures came back with an extra row (left unused). Short on-picture labels are new text: show them to Michael.
