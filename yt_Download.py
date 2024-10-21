import whisper
import torch
import os
import yt_dlp
from pytube import YouTube

def download_youtube_audio(url, output_path):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            audio_file = os.path.splitext(filename)[0] + '.mp3'
            print(f"音频已下载到: {audio_file}")
            return audio_file
    except Exception as e:
        print(f"下载 YouTube 音频时出错: {str(e)}")
        return None

def convert_audio_to_text(input_file, output_file):
    # 检查 GPU 是否可用
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"使用设备: {device}")

    # 加载 Whisper 模型
    model = whisper.load_model("base").to(device)
    
    print("正在处理音频...")
    
    # 如果是 YouTube URL，先下载音频
    if input_file.startswith('http'):
        print("检测到 YouTube URL，正在下载音频...")
        audio_file = download_youtube_audio(input_file, os.path.dirname(output_file))
        if audio_file is None:
            print("下载音频失败，程序终止。")
            return
        input_file = audio_file
    
    # 获取绝对路径并处理可能的编码问题
    input_file_abs = os.path.abspath(input_file)
    input_file_abs = input_file_abs.encode('utf-8').decode('utf-8')
    
    # 转换音频文件
    try:
        result = model.transcribe(input_file_abs)
    except RuntimeError as e:
        print(f"转录时出错: {str(e)}")
        print(f"请检查文件路径是否正确: {input_file_abs}")
        return
    
    # 将转录文本写入文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(result["text"])
    
    print(f"转录完成。结果已保存到 {output_file}")

def download_youtube_video(url, output_path=''):
    try:
        # 创建 YouTube 对象
        yt = YouTube(url)
        
        # 选择音频流或视频流
        stream = yt.streams.filter(only_audio=True).first()  # 仅下载音频
        # stream = yt.streams.get_highest_resolution()  # 下载最高分辨率的视频
        
        # 下载文件
        print(f"正在下载: {yt.title}")
        stream.download(output_path)
        print(f"下载完成: {yt.title}")
    except Exception as e:
        print(f"下载失败: {str(e)}")

if __name__ == "__main__":
    input_file = "https://www.youtube.com/watch?v=fx6yIosOGpE"  # YouTube URL 或本地文件路径
    output_file = "output.txt"  # 输出文本文件路径
    convert_audio_to_text(input_file, output_file)

    youtube_url = input("请输入 YouTube 视频链接: ")  # 输入 YouTube 视频链接
    download_youtube_video(youtube_url)
