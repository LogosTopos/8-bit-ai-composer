# Codex 搜索任务：收集 8-bit 游戏音乐谱面

> 把这个 prompt 直接发给 Codex（OpenAI Codex CLI / o3 / o4-mini），他有视觉和浏览器能力，能搜到我们搜不到的谱子、截图、视频教程。

---

## 任务目标

为 "AI 自动编写 8-bit 音乐" 项目收集**视觉化**的乐谱、钢琴卷帘、Tracker 截图、YouTube 教程，作为 AI 的训练/参考素材。

---

## 搜索指令

### 第一轮：乐谱图片（Image Search）

使用浏览器/视觉能力搜索以下内容的**图片**，保存截图：

1. **经典 NES 游戏原声谱子**
   - "Super Mario Bros theme sheet music"
   - "Zelda overworld piano sheet music"
   - "Mega Man 2 Dr Wily stage sheet music"
   - "Castlevania Vampire Killer sheet music"
   - "Kirby Dream Land Green Greens sheet music"
   - "Metroid Brinstar sheet music"
   - "Final Fantasy NES battle theme sheet music"
   - "Contra Jungle stage sheet music"
   - "Ninja Gaiden 4-2 sheet music"
   - "Duck Tales Moon theme sheet music"

2. **FamiTracker / 追踪器截图**
   - "FamiTracker pattern view screenshot"
   - "FamiTracker instrument editor screenshot"
   - "LSDJ Game Boy tracker screenshot"
   - "DefleMask Genesis tracker screenshot"
   - "Furnace tracker chiptune screenshot"

3. **MIDI 钢琴卷帘**
   - "NES music MIDI piano roll"
   - "chiptune MIDI editor screenshot"
   - "8-bit music MIDI arrangement"

### 第二轮：YouTube 教程（视觉分析）

找到并**截图关键帧**（钢琴卷帘、音符序列、设置面板）：

1. **FamiTracker 教程**
   - "FamiTracker tutorial how to make NES music" — 截图其中展示具体音符排列的画面
   - "FamiTracker Mega Man style tutorial"
   - "FamiTracker Castlevania style tutorial"

2. **8-bit 音乐制作**
   - "How to make chiptune music step by step"
   - "8-bit music composition tutorial"
   - "NES music theory explained"

3. **名曲拆解**
   - "How Super Mario Bros music was made"
   - "Zelda music theory analysis"
   - "Koji Kondo composition breakdown"

### 第三轮：GitHub / Web 工具（视觉交互）

打开以下网页，截图关键界面：

1. **在线 Chiptune 工具**
   - https://www.beepbox.co — 截图界面布局、音符编辑区
   - https://jummb.us — 在线 chiptune tracker
   - https://boscaceoil.net — 简易 chiptune DAW

2. **GitHub 项目页面**
   - 搜索 "chiptune AI" 或 "music generator" — 截图项目 README 中的架构图、示例输出
   - 搜索 "NES music dataset" — 截图数据样例

3. **论坛/社区的精华帖**
   - chipmusic.org 的教程板块
   - r/chiptunes 的置顶资源帖
   - NESdev 论坛的音乐编程板块

---

## 输出格式

把所有收集到的内容整理到一个 Markdown 文件中，结构如下：

```markdown
# 8-Bit 视觉参考手册

## 1. 经典名曲谱面
[粘贴截图] [附上来源URL] [简单说明该曲的特点]

## 2. Tracker 工作流截图
[粘贴截图] [说明这是什么软件的什么界面]

## 3. YouTube 教程关键帧
[粘贴截图] [附上视频URL] [说明截图展示了什么技巧]

## 4. 在线工具界面
[粘贴截图] [附上工具URL] [标注界面各部分功能]

## 5. MIDI 钢琴卷帘参考
[粘贴截图] [说明展示了什么编曲结构]
```

保存到 `D:/Auto/Github/8-bit/docs/visual-sheet-music-reference.md`

---

## 特别注意

- **优先找有具体音符的画面** — 能看清 C4 E4 G4 的那种
- **重点找 Tracker 软件里的 pattern 编辑区** — 这些是 AI 最需要学习的格式
- **多截图、多保存** — 宁滥勿缺
- **每张图标注来源 URL** — 方便以后追溯
- 如果遇到付费墙后面的内容，跳过，标注"付费内容需手动获取"
