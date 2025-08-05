# EchoScribe

**EchoScribe** 是一个音频转录 Python 工具。  
开发的原始目的旨在将OBS studio录制的mkv会议纪要转为文本，即信息模态转换。同时基于**有叠分割-ASR-LLM总结**功能解决了GPU显存不足的问题。

基于LLM开发。

## ✨ 主要功能

  * **视频转换**：将视频会议纪要（.mkv）分割为可重叠的音频片段。
  * **音频转换**：将指定目录下音频文件转换为文本。

## 📂 文件结构

```
.
├── fun.py     # 视频转换，分割，重复处理
└── spt.py     # 将给定文件夹中所有音频ASR
```

## ⚙️ 安装与依赖

在运行此项目之前，您需要安装FUNASR，推荐使用conda安装。

## ▶️ 如何使用

**示例:**

```bash
# mkv转音频
# args:
# --input-file: 输入mkv文件
# --output-dir: 输出音频片段目录
# --num-chunks: 分割片段数
# --overlap-sec: 片段重叠秒数
python ./spt.py --input-file [file name].mkv --output-dir audio_chunks --num-chunks 4 --overlap-sec 16

```

```bash
# 音频转文本
python ./fun.py # 使用GPU将"./audio_chunks/"中的所有文件转换为文本

```

```
# 输出1: asr_log_2025-08-04_21-49-45.txt
--- ASR Log Started at 2025-08-04_21-49-45 ---
Processing 32 files from directory: ./audio_chunks/
========================================


--- 正在处理: ./audio_chunks/2025-08-04_15-14-37_chunk_01.wav ---
识别结果: 【res】


--- 正在处理: ./audio_chunks/2025-08-04_15-14-37_chunk_02.wav ---
识别结果: 【res】


========================================
--- 所有文件处理完毕 ---
```

```
# 输出2: final_transcript.txt
【res1】
【res2】
```

```
# 整理结果
关于自动驾驶前沿技术的思考与探索分享会
日期： 2025年8月X日
主讲人： Z博士（根据上下文推断）

1. 背景与VLA（视觉语言智能体）的引入

【res】

2. 3D高斯重建与渲染的统一

【res】
……

QA

Aer:【res】
Ber:【res】

Cer:【res】
Ber:【res】

```

## 🤝 贡献

欢迎对 `EchoScribe` 的做出贡献！  
如果您有任何好的想法或建议，请随时提交 Pull Request 或创建 Issue。

## 📄 许可证

该项目采用 [MIT License](https://opensource.org/licenses/MIT) 授权。