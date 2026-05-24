# LLM 乐谱生成研究区

> 建立日期：2026-05-24  
> 目标：为本项目后续“用 LLM 生成、识别、校验、渲染乐谱”提供独立资料区。  
> 重点：识图能力、OMR 到 MusicXML、LLM 生成乐谱的中间表示，以及《英雄主义》相关参考资料。

## 文件地图

| 文件 | 用途 |
|---|---|
| [music-knowledge-and-formats.md](music-knowledge-and-formats.md) | LLM 生成乐谱需要的最小乐理、格式选择、推荐 JSON IR |
| [vision-omr-pipeline.md](vision-omr-pipeline.md) | 图片/PDF 乐谱识别流程：OMR、MusicXML、music21 校验、多模态 LLM 纠错 |
| [heroism-and-reference-scores.md](heroism-and-reference-scores.md) | 《英雄主义》同名/近名对象、现代作品版权风险、可合法用于 OCR 的公版参考谱 |
| [implementation-notes.md](implementation-notes.md) | 面向当前项目的落地方案、MVP 模块拆分、测试样本建议 |

## 核心结论

1. **不要让 LLM 直接生成完整 MusicXML 作为第一步。**  
   MusicXML 信息完整，但 XML 冗长，LLM 容易漏标签、漏小节时值、混淆声部。更稳的路线是：

   ```text
   自然语言/参考图像
     -> 逐小节 JSON IR
     -> 规则校验
     -> MusicXML / ABC / MIDI / LilyPond
     -> 渲染、试听、人工校对
   ```

2. **识图主干应采用 OMR + MusicXML。**  
   推荐 MVP：

   ```text
   图片/PDF
     -> Audiveris
     -> MusicXML/MXL
     -> music21 结构校验
     -> OpenSheetMusicDisplay/Verovio 并排预览
     -> MuseScore 人工修正
     -> MusicXML 为主文件，MIDI 只作试听
   ```

3. **多模态 LLM 更适合做“局部审稿员”，不适合单独替代 OMR。**  
   把原图按页、系统、小节切片，给模型看“原图小节 + OMR 输出片段”，让它只返回结构化 JSON patch，再由 music21/自写校验器检查。

4. **《英雄主义》大概率是现代商业作品，不能直接收录谱面内容。**  
   可以记录链接、曲目信息、速度/拍号/音域等元数据；OCR 测试样本优先选择 IMSLP 公版曲谱。

## 推荐工程主线

当前项目是 8-bit 音乐方向，建议先做两个互相独立但可组合的能力：

| 能力 | 输入 | 中间结果 | 输出 |
|---|---|---|---|
| LLM 生成乐谱 | 用户提示词、风格、长度、调性 | JSON IR | ABC/MIDI/8-bit 音频 |
| 谱面识图 | 图片/PDF 乐谱 | MusicXML + 小节级校验报告 | 可编辑 MusicXML/MIDI/参考 JSON IR |

后续如果要让 LLM “模仿某个谱面”，不要直接训练现代曲谱截图；先用识图链路抽取经授权或公版样本的结构特征，例如拍号、调性、织体、节奏密度、声部数量、和声节奏，再让 LLM 生成新的原创乐句。

## 主要来源入口

- Audiveris OMR: https://github.com/Audiveris/audiveris
- OpenSheetMusicDisplay: https://github.com/opensheetmusicdisplay/opensheetmusicdisplay
- Verovio toolkit: https://www.verovio.org/
- music21 documentation: https://www.music21.org/music21docs/
- MusicXML official site: https://www.musicxml.com/
- W3C MusicXML 4.0 reference: https://www.w3.org/2021/06/musicxml40/
- ABC notation / abcjs docs: https://docs.abcjs.net/overview/abc-notation
- LilyPond notation reference: https://lilypond.org/doc/stable/Documentation/notation/
- Humdrum **kern reference: https://www.humdrum.org/rep/kern.html
- ChatMusician paper: https://arxiv.org/abs/2402.16153
- Text2Score paper: https://arxiv.org/abs/2605.13431
