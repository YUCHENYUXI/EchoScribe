# 目标文件名
filename=/mnt/f/k.mp4

# 检查文件存在？如果不存在，则退出

if [ ! -f "$filename" ]; then
    echo "文件不存在: $filename"
    exit 1
fi

# MKV2WAV分割参数
num_chunks=2
overlap_sec=4

# MKV2WAV
python ./spt.py --input-file $filename  --output-dir audio_chunks --num-chunks $num_chunks --overlap-sec $overlap_sec
# ASR
python ./fun.py
# 清理WAV
rm -rf audio_chunks/*.wav

