# 《英雄主义》和参考谱面索引

## 1. 注意事项

用户提到的《英雄主义》不是唯一对象。检索结果至少包含现代商业单曲、同名吉他谱、节奏游戏曲、以及英文/意大利文标题含 Heroism/Eroismo 的公版古典作品。

现代作品的谱面、MIDI、扒谱视频通常不等于自由授权。本文只记录链接、元数据和适合研究的结构特征，不复制谱面内容，不下载或再分发受版权保护的文件。

## 2. 现代作品：在虚无中永存《英雄主义》

| 项目 | 信息 |
|---|---|
| 可能对象 | 《英雄主义》- 在虚无中永存 |
| 曲目信息 | Spotify 显示 2025 单曲，时长约 2:07，网易云音乐相关版权/发行信息 |
| 常见谱面/MIDI 元数据 | 多个 MIDI 版本标记为 4/4、120 BPM、钢琴独奏、约 2:06-2:07 |
| 织体观察 | 流行钢琴改编、宽音域伴奏、旋律叠置、延音踏板、左右手可能冲突 |
| 用途 | 做链接索引、曲风分析、内部人工验证 |
| 不建议 | 公开收录谱面截图、公开再分发 MIDI、作为未经授权训练集 |

来源入口：

- Spotify track: https://open.spotify.com/track/1yzIHBuLR4DdKqf9scjyip
- B 站扒谱视频: https://www.bilibili.com/video/BV1atZ1YeEUQ/
- MidiShow 单曲页: https://www.midishow.com/en/midi/223846.html
- MidiShow 标签页: https://www.midishow.com/en/tag/%E8%8B%B1%E9%9B%84%E4%B8%BB%E4%B9%89?sort=marks
- 弹琴吧: https://www.tan8.com/yuepu-107392.html
- PiaStudy: https://piastudy.com/Intermediate/xOUaSK7Z
- 虫虫钢琴: https://www.gangqinpu.com/cchtml/1145982.htm
- 曲谱屋: https://www.qupu5.com/piano/66640.html

## 3. 近名对象

| 对象 | 资料 | 结构特征 | 建议 |
|---|---|---|---|
| 《英雄主义 Pt.2》- Youzee Music / 在虚无中永存 | Amazon Music、B 站公开视频、滴滴音乐资料 | 2025 现代商业曲目，时长约 2:23 | 只记录元数据和链接，不作为公开 OCR 样本 |
| Chord4 同名吉他谱 | Chord4 有 2019 上传吉他谱 | 吉他弹唱谱/和弦谱 | 可用于“同名作品消歧”，不要复制歌词/谱面 |
| Vicious [ANTi] Heroism - Kobaryo / Arcaea | MidiShow、Arcaea Wiki、Bandcamp | 节奏游戏曲，高 BPM，高音符密度 | 适合复杂节奏/游戏谱面参考，不作公开谱面训练样本 |

来源入口：

- Amazon Music《英雄主义 Pt.2》: https://music.amazon.com/tracks/B0FMZN9Q3L
- B 站《英雄主义 Pt.2》相关视频: https://www.bilibili.com/video/BV1y4tGzhEPp/
- Chord4 同名吉他谱: https://chord4.com/tabs/30399
- Vicious [ANTi] Heroism MIDI: https://www.midishow.com/en/midi/vicious-anti-heroism-midi-download-186525
- Arcaea Wiki: https://arcaea.fandom.com/wiki/Vicious_Heroism
- Bandcamp: https://hitnex.bandcamp.com/track/vicious-anti-heroism

## 4. 推荐用于 OCR 的公版参考谱

这些更适合作为项目内自动化测试样本，因为版权风险低、页面结构丰富。

| 作品 | 来源 | 特征 | 用途 |
|---|---|---|---|
| Louis Campbell-Tipton: Sonata heroic | IMSLP | 钢琴独奏，浪漫派，约 24 页，C# minor | 清晰钢琴谱 OCR、密集和弦、跨页结构 |
| William Otto Miessner: Sonata Excelsior, Op.10, I. Heroism | IMSLP | 钢琴独奏，第一乐章标题 Heroism，多速度段，约 55 页 | OCR 长谱、速度/表情标记、多页一致性 |
| Ferdinando Paer: L'eroismo in amore | IMSLP | 歌剧总谱，声乐+管弦乐，大型多声部扫描 | 高难度版面识别、总谱系统识别 |
| Gaspare Spontini: L'eroismo ridicolo | IMSLP | 舞台作品，声乐/管弦乐 | Eroismo 语义相关、公版复杂谱面 |

来源入口：

- Sonata heroic: https://imslp.org/wiki/Sonata_heroic_%28Campbell-Tipton%2C_Louis%29
- Sonata Excelsior, Op.10: https://imslp.org/wiki/Sonata_Excelsior%2C_Op.10_%28Miessner%2C_William_Otto%29
- L'eroismo in amore: https://imslp.org/wiki/L%27eroismo_in_amore_%28Pa%C3%ABr%2C_Ferdinando%29
- L'eroismo ridicolo: https://imslp.org/wiki/L%27eroismo_ridicolo_%28Spontini%2C_Gaspare%29

## 5. 《英雄主义》方向的可提取特征

若目标是让 LLM 生成“类似《英雄主义》的原创乐谱”，不要复制旋律。可以提取这些抽象特征：

| 维度 | 可记录内容 |
|---|---|
| 宏观结构 | intro / A / B / climax / outro 的小节长度 |
| 节奏密度 | 每小节音符数、左手伴奏密度、高潮段密度 |
| 音区 | 旋律常用音区、伴奏最低音、高潮最高音 |
| 织体 | 分解和弦、八度加厚、旋律叠置、踏板持续 |
| 和声节奏 | 每小节换和弦还是半小节换和弦 |
| 情绪曲线 | 从稀疏到密集、从中音区到宽音域 |
| 可演奏性 | 左右手冲突、跨距、是否需要简化 |

可以让多模态模型对截图做“非复制性分析”，输出：

```json
{
  "piece": "英雄主义",
  "measure_range": "1-8",
  "features": {
    "texture": "right-hand melody with broken-chord accompaniment",
    "density": "medium",
    "register": "wide piano range",
    "possible_playability_issue": "left-hand jumps may need simplification"
  },
  "copyright_safe": "feature summary only; no note-by-note transcription"
}
```

## 6. 样本优先级

1. **公版 OCR 样本**：优先 IMSLP 曲谱，建立识图准确率基线。
2. **现代作品内部验证**：只用链接和个人/内部测试，不提交截图或 MIDI 到仓库。
3. **结构化特征库**：保存抽象特征，不保存受版权保护的逐音符内容。
4. **原创生成**：让 LLM 依据抽象特征生成新旋律、新和声、新节奏。
