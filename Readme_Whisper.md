# WhisperJax2Txt 使用说明

## 简介
`WhisperJax2Txt.py` 是一个用于将音频和视频文件转录为文本的 Python 脚本。它支持从本地音频/视频文件和 YouTube 视频 URL 提取音频并进行转录。

## 环境要求
确保您已安装以下库：
- `whisper`
- `torch`
- `yt-dlp`
- `ffmpeg`

您可以使用以下命令安装所需的库：

## 使用方法

### 1. 准备输入文件
您可以使用以下三种类型的输入：
- **音频文件**：如 `.mp3`、`.wav` 等格式。
- **视频文件**：如 `.mp4`、`.mkv` 等格式。
- **YouTube URL**：以 `http` 开头的有效 YouTube 视频链接。

### 2. 修改脚本中的输入
在 `WhisperJax2Txt.py` 的 `__main__` 部分，设置 `input_file` 和 `output_file` 变量：

### 3. 运行脚本
在终端中运行以下命令：

### 4. 输出结果
转录完成后，结果将保存到指定的 `output_file` 中（如 `output.txt`）。

## 示例
- **输入音频文件**：
  ```python
  input_file = r"D:\My.Dev\WhisperJax2Txt\AV\huawei.mp3"
  ```

- **输入视频文件**：
  ```python
  input_file = r"D:\My.Dev\WhisperJax2Txt\AV\Fly.mp4"
  ```

- **输入 YouTube URL**：
  ```python
  input_file = r"https://www.youtube.com/watch?v=fx6yIosOGpE"
  ```

## 注意事项
- 确保输入文件路径正确，且文件存在。
- 对于 YouTube URL，确保网络连接正常，以便下载音频。
- 如果使用视频文件，确保系统上已安装 `ffmpeg`，以便提取音频。

通过以上步骤，您可以轻松使用 `WhisperJax2Txt.py` 进行音频和视频文件的转录。
