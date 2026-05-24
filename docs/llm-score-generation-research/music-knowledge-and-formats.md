# LLM 生成乐谱：乐理与格式

## 1. 最小乐理模型

LLM 生成乐谱时，不需要一开始覆盖所有专业记谱，但必须显式表达这些对象：

| 模块 | 必须表达 | 常见失败 |
|---|---|---|
| 调式/调号 | tonic、mode、key signature、临时升降号、转调点 | 调号和临时记号混淆；升降号拼写不符合调性 |
| 拍号/小节 | time signature、pickup、小节编号、每小节总时值 | 小节溢出或不满 |
| 节奏 | note/rest duration、附点、连音、三连音、切分 | tie/slur 混用；tuplets 总时值错误 |
| 旋律 | pitch、octave、scale degree、motif、phrase、cadence | 句法弱、音域不合理、结尾无稳定性 |
| 和声 | chord symbol、Roman numeral、inversion、harmonic rhythm | 和弦音拼写错；旋律与和声强拍冲突 |
| 声部 | part、staff、voice、SATB、voice leading | 声部交叉、平行五/八度、声部音域越界 |
| 配器 | instrument、clef、transposition、playable range | 移调乐器写成实音；不可演奏音域 |
| 表情/装饰 | dynamics、articulation、ornaments、grace notes、slur、tie | MIDI 播放信息和谱面符号混在一起 |

乐理参考：

- Open Music Theory Fundamentals: https://open.library.okstate.edu/sandbox/part/fundamentals/
- Voice Leading and Part Writing: https://musictheory.pugetsound.edu/mt21c/VoiceLeading.html
- Open Music Theory Orchestration: https://open.library.okstate.edu/sandbox/part/orchestration/
- MuseScore expressive markings: https://handbook.musescore.org/notation/expressive-markings

## 2. 格式选择

| 格式 | LLM 友好度 | 优点 | 缺点 | 推荐用途 |
|---|---:|---|---|---|
| ABC notation | 高 | 短、纯文本、容易 few-shot、适合旋律和 lead sheet | 复杂排版/现代记谱/大型总谱能力弱 | LLM 初稿、旋律草图、快速 MIDI |
| JSON IR | 高 | 可校验、可转换、适合程序处理 | 不是通用乐谱标准，需要自写转换器 | 项目内部主中间表示 |
| MusicXML | 中 | 交换标准，保留乐谱语义，MuseScore/Finale/Sibelius 可读 | 冗长，LLM 容易生成非法 XML | 最终可编辑乐谱 |
| MIDI | 中低 | 播放友好，DAW 可读，适合模型训练 | 缺排版、声部、拼写、装饰、重复记号等语义 | 试听、音高/节奏事件、8-bit 渲染 |
| LilyPond | 中高 | 文本化、高质量排版、适合版本控制 | 语法专业，编译失败需要修复循环 | 高质量 PDF/SVG |
| Humdrum/**kern | 中 | 分析友好，可表达音高、时值、装饰、连线等 | 面向分析，不是主流交换/排版格式 | 和声/声部/语料库分析 |

格式来源：

- MusicXML for developers: https://www.musicxml.com/for-developers/
- W3C MusicXML attributes: https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/attributes/
- MIDI 1.0 specification entry: https://midi.org/midi-1-0-detailed-specification
- MuseScore import/export notes: https://musescore.org/da/print/book/export/html/278625
- ABC notation docs: https://docs.abcjs.net/overview/abc-notation
- LilyPond notation reference: https://lilypond.org/doc/stable/Documentation/notation/
- Humdrum **kern: https://www.humdrum.org/rep/kern.html

## 3. 推荐中间表示：Measure-wise JSON IR

核心思路：LLM 先生成“逐小节音乐计划”，程序再转成目标格式。Text2Score 也采用类似的两阶段思路：LLM 先把自然语言转为结构化小节计划，再驱动乐谱生成。

Text2Score: https://arxiv.org/abs/2605.13431

### IR 示例

```json
{
  "metadata": {
    "title": "Untitled Chiptune",
    "style": "8-bit heroic stage theme",
    "tempo": {"bpm": 140, "beat_unit": "quarter"}
  },
  "global": {
    "key": {"tonic": "C", "mode": "major"},
    "time": "4/4",
    "swing": false
  },
  "parts": [
    {
      "id": "P1",
      "instrument": "pulse_square_lead",
      "clef": "treble",
      "range": ["C4", "C6"],
      "voices": [
        {
          "id": "lead",
          "measures": [
            {
              "number": 1,
              "harmony": [{"at": 0, "symbol": "C", "roman": "I"}],
              "events": [
                {"at": 0, "type": "note", "pitch": "E5", "dur": "1/8", "velocity": 100},
                {"at": 0.5, "type": "note", "pitch": "G5", "dur": "1/8"},
                {"at": 1, "type": "note", "pitch": "C6", "dur": "1/4"},
                {"at": 2, "type": "rest", "dur": "1/2"}
              ]
            }
          ]
        }
      ]
    }
  ]
}
```

## 4. 8-bit 约束字段

当前项目偏 8-bit，IR 应额外表达这些约束：

| 字段 | 示例 | 用途 |
|---|---|---|
| `chip_profile` | `nes_2a03` | 选择通道限制 |
| `channel_role` | `lead` / `arp` / `bass` / `noise` | 映射 P1/P2/TR/NO |
| `duty_cycle` | `12.5%` / `25%` / `50%` | 方波音色 |
| `monophonic` | `true` | 防止同通道和弦 |
| `arp_pattern` | `[0, 4, 7, 4]` | 用琶音模拟和弦 |
| `loop` | `{"start_measure": 5, "end_measure": 20}` | 游戏音乐循环 |

## 5. 校验规则

生成后必须过规则校验，失败则反馈给 LLM 或自动修复。

| 校验 | 最低要求 |
|---|---|
| 小节时值 | 每个 voice 的每小节时值等于拍号容量，允许 pickup |
| 音高拼写 | pitch class 与 key/accidental 一致 |
| 音域 | 每个 part 不超出可演奏音域 |
| 单声道限制 | 8-bit P1/P2/TR 每个时间点最多一个 note |
| 和声一致性 | 强拍旋律优先落在 chord tone 或明确 passing tone |
| 连线闭合 | tie start/stop 成对，slur 不替代 tie |
| 导出可解析 | MusicXML 可被 music21/MuseScore 打开；ABC 可被 music21/abc2midi 解析 |

## 6. LLM 提示词原则

1. 先让模型输出结构计划，不直接输出最终 MusicXML。
2. 输出 JSON 时使用固定 schema，并要求不能写注释。
3. 每次只生成 4-8 小节，长曲用 section 拼接。
4. 让模型显式写出 key、time、tempo、channel roles、loop 点。
5. 对失败样例进行“错误消息回填”，让模型只修复失败小节。

示例：

```text
你是乐谱生成器。只输出符合 schema 的 JSON，不要解释。
生成 8 小节 NES 风格 heroic 主题：
- 4/4, C major, 140 BPM
- P1 lead: C4-C6, 单声道
- P2 arpeggio: 每小节按和弦 16 分音符琶音
- TR bass: C2-C4, root/fifth
- NO drums: kick/snare/hihat 事件
- loop from measure 1 to 8
要求每个 voice 每小节正好 4 拍。
```
