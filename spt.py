import os
import argparse
from pydub import AudioSegment
import math

def split_audio_with_overlap(input_file, output_dir, num_chunks=3, overlap_sec=2):
    """
    将一个音频文件拆分成多个重叠的块。

    :param input_file: 输入的音频或视频文件路径。
    :param output_dir: 保存输出块的目录。
    :param num_chunks: 要拆分的块数。
    :param overlap_sec: 每块之间的重叠秒数。
    """
    print(input_file, output_dir, num_chunks, overlap_sec)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"创建目录: {output_dir}")

    print(f"正在加载音频文件: {input_file}")
    # pydub可以自动处理多种格式，背后使用ffmpeg
    audio = AudioSegment.from_file(input_file)
    total_duration_ms = len(audio)
    overlap_ms = overlap_sec * 1000

    # 计算每个块的理论长度（不考虑重叠）
    chunk_len_ms = math.ceil(total_duration_ms / num_chunks)

    print(f"总时长: {total_duration_ms / 1000:.2f} 秒")
    print(f"计划拆分为 {num_chunks} 块，每块之间重叠 {overlap_sec} 秒")

    for i in range(num_chunks):
        # 计算每个块的起始和结束时间点
        start_ms = i * chunk_len_ms
        end_ms = start_ms + chunk_len_ms + overlap_ms

        # 确保结束时间点不会超出音频总长
        end_ms = min(end_ms, total_duration_ms)

        # 如果起始时间点已经等于或超过总时长，说明已经处理完，可以提前退出
        if start_ms >= total_duration_ms:
            break

        print(f"正在处理块 {i+1}/{num_chunks}: 从 {start_ms/1000:.2f}s 到 {end_ms/1000:.2f}s")

        # 从原始音频中切片
        chunk = audio[start_ms:end_ms]

        # 定义输出文件名
        input_filename = os.path.splitext(os.path.basename(input_file))[0]
        output_filename = f"{input_filename}_chunk_{i+1:02d}.wav"
        output_path = os.path.join(output_dir, output_filename)

        # 以WAV格式导出，这是ASR最常用的格式
        chunk.export(output_path, format="wav")
        print(f"已保存到: {output_path}")

    print("\n所有块处理完毕！")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="将音频文件拆分为重叠的块。")
    parser.add_argument("--input-file", required=True, help="输入的音频或视频文件。")
    parser.add_argument("--output-dir", required=True, help="保存输出块的目录。")
    parser.add_argument("--num-chunks", type=int, default=3, help="要拆分的块数。")
    parser.add_argument("--overlap-sec", type=int, default=2, help="块之间的重叠秒数（为了防止句子在切点被断开）。")

    args = parser.parse_args()

    split_audio_with_overlap(args.input_file, args.output_dir, args.num_chunks, args.overlap_sec)


#python ./spt.py --input-file 2025-08-04_15-14-37.mkv --output-dir audio_chunks --num-chunks 4 --overlap-sec 16