# 当前项目落地笔记

## 1. 建议 MVP

先做“可控生成”，再做“识图导入”。

```text
Phase 1: LLM -> JSON IR -> MIDI/ABC
Phase 2: JSON IR -> MusicXML -> MuseScore/OSMD 预览
Phase 3: 图片/PDF -> Audiveris -> MusicXML -> 校验/纠错
Phase 4: 谱面特征抽取 -> LLM 原创生成
```

## 2. 生成模块

### 2.1 输入

```json
{
  "style": "8-bit heroic",
  "length_measures": 8,
  "key": "C major",
  "time": "4/4",
  "tempo": 140,
  "channels": ["P1", "P2", "TR", "NO"],
  "loop": true
}
```

### 2.2 输出

LLM 输出 `score_ir.json`，程序导出：

| 输出 | 用途 |
|---|---|
| `.abc` | 快速可读、快速预览 |
| `.mid` | 项目当前 8-bit 合成链路 |
| `.musicxml` / `.mxl` | MuseScore/OSMD 可编辑乐谱 |
| `.json` | 后续编辑、修复、回放的主数据 |

### 2.3 必做校验

```text
validate_ir()
  - measure durations
  - channel monophony
  - pitch ranges
  - note/rest event ordering
  - loop length equality across channels
  - export parser roundtrip
```

## 3. 识图模块

### 3.1 输入目录建议

```text
data/score_vision/
  raw/          # 原始图片/PDF，不提交受版权保护内容
  public/       # 公版样本，可记录来源
  work/         # Audiveris .omr/.mxl 临时输出
  reviewed/     # 人工确认后的 MusicXML
  reports/      # 校验报告和 patch 记录
```

### 3.2 流程

```text
import_score_image(input.pdf)
  -> preprocess pages
  -> run_audiveris()
  -> load_musicxml_with_music21()
  -> validate_measures()
  -> render_for_review()
  -> optional_llm_patch()
  -> save reviewed MusicXML
```

### 3.3 多模态 LLM 只做小节级任务

Prompt 方向：

```text
你是乐谱 OCR 校对助手。左图是原始乐谱小节，下面是 OMR 生成的 MusicXML 片段。
只返回 JSON。不要重写整页，只指出该小节里疑似错音、漏休止符、错时值、错连线。
如果无法确定，needs_human_review=true。
```

## 4. 和现有 8-bit 代码的连接点

现有 `src/audio` 更像合成/播放层。建议新增 `src/score`，不要把乐谱逻辑塞进 audio：

```text
src/score/
  ir.py             # dataclass / pydantic schema
  validate.py       # 时值、音域、单声道校验
  export_midi.py    # IR -> MIDI
  export_abc.py     # IR -> ABC
  export_musicxml.py# IR -> MusicXML
  import_musicxml.py# MusicXML -> IR
  omr.py            # Audiveris wrapper
```

如果项目暂时不想引入复杂依赖，最低可先做：

1. `IR -> MIDI`
2. `IR -> ABC`
3. `music21` 验证 ABC/MIDI/MusicXML

## 5. 样本策略

| 样本类型 | 存放 | 是否提交 |
|---|---|---|
| 自己生成的测试谱 | `data/score_vision/public` | 可以 |
| IMSLP 公版谱 | 记录来源和脚本下载方式 | 可以提交链接，谨慎提交文件 |
| 《英雄主义》截图/MIDI | 本地 raw 或外部私有目录 | 不提交 |
| 现代网站谱面链接 | Markdown 索引 | 可以 |

## 6. 下一步任务清单

1. 定义 `ScoreIR` schema。
2. 实现 `ScoreIR -> MIDI`，直接连接当前 8-bit 合成。
3. 实现 `ScoreIR -> ABC`，用于快速人工读谱。
4. 接入 `music21` 做小节时值和音域校验。
5. 选 2-3 份 IMSLP 公版谱做 OMR baseline。
6. 用 Audiveris 跑一次 PDF -> MusicXML，记录失败点。
7. 做一个页面级或小节级并排预览原型。
