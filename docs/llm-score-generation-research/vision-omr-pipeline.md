# 乐谱识图 / OMR / 多模态纠错流程

## 1. 结论

图片/PDF 到可编辑乐谱，MVP 不应让多模态 LLM 直接“看图写完整 MusicXML”。更稳的生产路线是：

```text
图片/PDF
  -> 预处理
  -> OMR 识别
  -> MusicXML/MXL
  -> music21 规则校验
  -> OSMD/Verovio/MuseScore 渲染复核
  -> 多模态 LLM 小节级纠错
  -> 人工确认
  -> MusicXML 主文件 + MIDI 试听文件
```

MIDI 不能作为主交换格式，因为它缺少大量谱面语义：拼写、声部、连线、装饰音、排版、反复记号、歌词对齐等。

## 2. 工具选型

| 类别 | 工具 | 作用 | 备注 |
|---|---|---|---|
| 开源 OMR | Audiveris | 图片/PDF 到 `.omr`、MusicXML/MXL | 当前最实用的开源基线；主要面向印刷 CWMN，不适合手写谱 |
| 乐谱渲染 | OpenSheetMusicDisplay | 浏览器加载并渲染 MusicXML | 适合做并排校对 UI，不做识图 |
| 乐谱渲染/转换 | Verovio | MEI/MusicXML 到 SVG/MIDI/time-map | 适合服务端或前端渲染，也不是 OMR |
| 符号处理 | music21 | 读取/改写/分析 MusicXML、MIDI、ABC | 做结构校验和格式转换 |
| 编辑器 | MuseScore Studio | 打开、人工修改、导出 MusicXML/MIDI/PDF | OMR 后的人机校对中心 |
| 深度学习 OMR | SMT、TrOMR、oemer、lmx | image-to-token / image-to-sequence | 可做研究增强线，先不要作为 MVP 依赖 |

来源：

- Audiveris: https://github.com/Audiveris/audiveris
- OpenSheetMusicDisplay: https://github.com/opensheetmusicdisplay/opensheetmusicdisplay
- Verovio: https://www.verovio.org/
- music21 docs: https://www.music21.org/music21docs/
- MuseScore handbook: https://musescore.org/handbook
- Linearized MusicXML research: https://github.com/OMR-Research/lmx

## 3. MVP 流程

### 3.1 输入预处理

目标是让 OMR 看到稳定、清晰、接近扫描件的图。

| 输入问题 | 处理 |
|---|---|
| PDF 多页 | 拆页，保留页码和原始坐标 |
| 拍照倾斜 | 透视校正、裁边、去阴影 |
| 分辨率低 | 统一到 300-600 DPI |
| 背景脏 | 灰度化、增强对比度、去噪 |
| 页面旋转 | 自动检测并旋正 |

### 3.2 OMR 主识别

Audiveris CLI 示例：

```powershell
audiveris -batch -transcribe -export -output out input.pdf
```

输出：

| 文件 | 用途 |
|---|---|
| `.omr` | Audiveris 内部工程文件，可 GUI 校对 |
| `.mxl` / `.musicxml` | 后续主交换格式 |
| 日志 | 记录失败页、小节、符号识别异常 |

### 3.3 结构校验

用 music21 或自写解析器检查：

| 校验项 | 失败表现 |
|---|---|
| 小节时值 | 4/4 小节不足/超过 4 拍 |
| 声部数量 | 同 staff 的 voice 分裂异常 |
| 调号/临时记号 | 大量不合调性的异名音 |
| 谱号变化 | clef 识别错导致整体八度/音区错误 |
| tie/slur | 连线断开、延音被拆成重复击键 |
| lyrics | 歌词错位或丢失 |
| repeats | 反复、跳房子、D.S./D.C. 丢失 |

### 3.4 并排视觉复核

推荐 UI：

```text
左侧：原谱图像页/小节切片
右侧：MusicXML 渲染 SVG
底部：校验错误列表 + LLM patch 建议 + 人工确认按钮
```

可选渲染器：

- OpenSheetMusicDisplay：前端 MusicXML 渲染。
- Verovio：MusicXML/MEI 到 SVG，适合命令行或服务端。
- MuseScore：人工编辑与最终导出。

## 4. 多模态 LLM 的正确位置

多模态模型的优势是“看局部图像并发现明显错漏”。不要让它整页重写谱子，应让它做小范围 patch。

### 4.1 小节级输入

每次给模型：

1. 原谱第 N 页第 M 小节截图。
2. OMR 导出的该小节 MusicXML 片段。
3. 规则校验错误，例如“小节时值为 3.5 拍，应为 4 拍”。
4. 只允许返回 JSON。

### 4.2 建议 JSON schema

```json
{
  "measure_id": "page-1-system-2-measure-7",
  "confidence": 0.72,
  "issues": [
    {
      "type": "duration_mismatch",
      "location": {"staff": 1, "voice": 1, "beat": 3.5},
      "description": "疑似漏识别一个八分休止符",
      "proposed_patch": {
        "operation": "insert_rest",
        "at": 3.5,
        "duration": "1/8"
      },
      "needs_human_review": true
    }
  ]
}
```

### 4.3 Patch 原则

| 原则 | 原因 |
|---|---|
| 只 patch 局部小节 | 降低幻觉和误改范围 |
| patch 必须可回滚 | 保留 OMR 原始结果 |
| patch 后重新渲染 | 防止修复 XML 但视觉更错 |
| patch 后重新校验 | 小节时值、声部、连线必须合法 |
| 低置信度标红 | 给人工处理，不自动覆盖 |

OpenAI 相关官方文档入口：

- Images and vision: https://platform.openai.com/docs/guides/images-vision
- Structured Outputs: https://platform.openai.com/docs/guides/structured-outputs

## 5. 准确率风险

| 谱面类型 | 风险 |
|---|---|
| 清晰印刷钢琴谱 | 最适合 MVP |
| 标准管弦总谱 | 可做，但声部/系统复杂度更高 |
| 手写谱 | 不适合首版自动识别 |
| 吉他谱/鼓谱/现代记谱 | OMR 风险高，需专门模型或规则 |
| 古谱、低清扫描 | 需要人工校对，版面解析容易失败 |
| 密集装饰音/跨谱表/多声部钢琴 | 容易漏连线、错声部、错节奏 |

## 6. 测试分层

| 层级 | 样本 | 目标 |
|---|---|---|
| L1 | 自己生成的简单 MusicXML 再渲染成图片 | 验证 pipeline 通路 |
| L2 | IMSLP 清晰公版钢琴谱 | 验证真实扫描识别 |
| L3 | 多声部/管弦公版总谱 | 验证复杂版面 |
| L4 | 现代曲谱链接，仅内部人工测试 | 不公开分发，验证目标曲风 |

## 7. 项目内建议接口

```text
score_vision/
  preprocess.py       # PDF/page/image 预处理
  omr_audiveris.py    # 调用 Audiveris 并管理输出
  validate_musicxml.py# music21 校验
  render_compare.py   # OSMD/Verovio/MuseScore 渲染接口
  llm_patch.py        # 多模态模型小节级 patch
  review_store.py     # 保存 patch、置信度、人工确认状态
```
