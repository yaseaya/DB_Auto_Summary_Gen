创建虚拟环境
1. 打开 VSCode：
启动 Visual Studio Code。
2. 打开终端：
您可以通过菜单栏选择 Terminal -> New Terminal，或者使用快捷键 Ctrl + 打开终端。
3. **创建虚拟环境**： 在终端中，使用以下命令创建虚拟环境（假设您使用的是 Python 3）： bash
python -m venv venv
   这将创建一个名为 `venv` 的虚拟环境文件夹。

4. **激活虚拟环境**：
   - **在 Windows 上**：
     ```bash
     venv\Scripts\activate
     ```
   - **在 macOS 或 Linux 上**：
     ```bash
     source venv/bin/activate
     ```

   激活后，您会看到终端提示符前面出现 `(venv)`，表示虚拟环境已激活。

### 安装依赖项

在虚拟环境激活后，您可以安装所需的依赖项，例如 WhisperJax 和 PyTorch：



### 配置 VSCode 使用虚拟环境

1. **选择 Python 解释器**：
   按下 `Ctrl + Shift + P` 打开命令面板，输入并选择 `Python: Select Interpreter`。然后选择您刚刚创建的虚拟环境的 Python 解释器。

2. **运行代码**：
   现在，您可以在 VSCode 中运行您的 Python 代码，确保它使用的是虚拟环境中的依赖项。

### 退出虚拟环境

完成工作后，您可以通过以下命令退出虚拟环境：



这样，您就成功在 VSCode 中创建并使用了虚拟环境。


###

我们可以修改代码以使用 GPU 来加速 Whisper 模型的处理。Whisper 库会自动使用可用的 GPU,但我们可以通过指定设备来确保它使用 GPU。以下是修改后的代码:

```python:WhisperJax2Txt.py
import whisper
import torch

def convert_audio_to_text(input_file, output_file):
    # 检查 GPU 是否可用
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"使用设备: {device}")

    # 加载 Whisper 模型
    model = whisper.load_model("base").to(device)
    
    print("正在转录音频...")
    
    # 转换音频文件
    result = model.transcribe(input_file)
    
    # 将转录文本写入文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(result["text"])
    
    print(f"转录完成。结果已保存到 {output_file}")

if __name__ == "__main__":
    input_file = "path/to/your/audio_or_video_file.mp4"  # 输入文件路径
    output_file = "output.txt"  # 输出文本文件路径
    convert_audio_to_text(input_file, output_file)
```

这个版本的代码做了以下修改:

1. 我们导入了 `torch` 库,以便检查 GPU 是否可用。
2. 我们使用 `torch.cuda.is_available()` 来检查 GPU 是否可用,并相应地设置 `device` 变量。
3. 我们使用 `.to(device)` 将模型移动到适当的设备（GPU 或 CPU）。
4. 我们添加了一个打印语句来显示正在使用的设备。

要使用这个新版本的代码,您需要确保已经安装了 PyTorch。如果还没有安装,您可以使用以下命令安装（包括 CUDA 支持）:

```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

请注意,上面的命令安装的是支持 CUDA 11.8 的 PyTorch 版本。如果您的 CUDA 版本不同,请相应地调整 URL。

此外,请确保您的系统上已经安装了适当的 CUDA 驱动程序和工具包。

这个版本的代码应该能够自动检测并使用可用的 GPU,从而加速音频转录过程。如果您在运行这个新版本时遇到任何问题,或者需要进一步的优化,请告诉我,我会继续帮您解决。