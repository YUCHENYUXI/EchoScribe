import os
import glob
import datetime # --- NEW ---: 导入datetime库用于生成时间戳
from funasr import AutoModel

# --- Configuration ---
dvc = "cuda:0"  # 使用CUDA还是CPU

# Use a highly accurate Paraformer model from ModelScope.
model = AutoModel(model="iic/speech_paraformer-large_asr_nat-zh-cn-16k-common-vocab8404-pytorch",
                  device=dvc)

# --- NEW ---: 定义日志文件名
# 创建一个带当前时间戳的文件名，例如: asr_log_2025-08-04_21-45-30.txt
timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
log_filename = f"asr_log_{timestamp}.txt"
clean_transcript_filename = "final_transcript.txt" # --- NEW ---: 干净的最终结果文件名

# 指向包含音频块的目录
input_dir = "./audio_chunks/"

# 使用glob找到所有.wav文件
audio_files = glob.glob(os.path.join(input_dir, "*.wav"))
audio_files.sort()  # 确保按顺序处理

print(f"在目录 {input_dir} 中找到 {len(audio_files)} 个音频文件进行处理。")
print(f"详细日志将被保存到: {log_filename}")

# --- NEW ---: 创建一个列表来收集纯文本结果
all_text_results = []

# --- NEW ---: 使用 'with open' 来打开日志文件，'w'表示写入模式，encoding='utf-8'支持中文
with open(log_filename, 'w', encoding='utf-8') as log_file:
    log_file.write(f"--- ASR Log Started at {timestamp} ---\n")
    log_file.write(f"Processing {len(audio_files)} files from directory: {input_dir}\n")
    log_file.write("="*40 + "\n\n")

    for audio_file in audio_files:
        line_to_print = f"\n--- 正在处理: {audio_file} ---"
        print(line_to_print)
        log_file.write(line_to_print + "\n")

        try:
            # 调用funasr进行识别
            res = model.generate(input=audio_file)

            # 检查并保存识别结果
            if res and "text" in res[0]:
                recognized_text = res[0]['text']
                
                line_to_print = f"识别结果: {recognized_text}"
                print(line_to_print)
                log_file.write(line_to_print + "\n")
                
                # --- NEW ---: 将干净的文本添加到列表中
                all_text_results.append(recognized_text)
            else:
                line_to_print = "未能识别出文本。"
                print(line_to_print)
                log_file.write(line_to_print + "\n")

        except Exception as e:
            line_to_print = f"处理文件 {audio_file} 时发生错误: {e}"
            print(line_to_print)
            log_file.write(line_to_print + "\n")

    log_file.write("\n\n" + "="*40 + "\n")
    log_file.write("--- 所有文件处理完毕 ---\n")

print("\n--- 所有文件处理完毕 ---")
print(f"详细日志已保存在 {log_filename}")


# --- NEW: Bonus Step ---
# 将所有识别出的文本片段拼接起来，保存到一个干净的文件中
if all_text_results:
    print(f"\n正在将所有识别出的文本拼接并保存到 {clean_transcript_filename}...")
    with open(clean_transcript_filename, 'w', encoding='utf-8') as f:
        # 你可以选择用句号、空格或者换行符来连接
        # 这里我们使用句号加换行符，便于阅读
        final_text = "。\n".join(all_text_results)
        f.write(final_text)
    print("最终文稿保存成功！")
else:
    print("没有可用于生成最终文稿的识别结果。")