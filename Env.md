
# 生成 requirements.txt
pip freeze > requirements.txt

# 安装 requirements.txt
pip install -r requirements.txt

# 安装 torch torchvision torchaudio
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

Looking in indexes: https://download.pytorch.org/whl/cu118





要创建 `requirements.txt` 文件，您可以按照以下步骤操作：

1. **在项目目录中创建 requirements.txt 文件**：
   您可以手动创建一个名为 `requirements.txt` 的文件，或者使用命令行。

   ```bash
   touch requirements.txt
   ```

2. **列出已安装的包**：
   如果您希望将当前环境中已安装的所有包及其版本添加到 `requirements.txt` 中，可以使用以下命令：

   ```bash
   pip freeze > requirements.txt
   ```

   这将把所有已安装的包及其版本写入 `requirements.txt` 文件。

3. **手动编辑 requirements.txt**：
   如果您只想列出特定的包，可以手动打开 `requirements.txt` 文件并添加所需的包及其版本。例如：

   ```
   selenium==4.1.0
   pika==1.2.0
   ```

4. **使用 requirements.txt 安装依赖**：
   其他人可以使用以下命令通过 `requirements.txt` 安装所有依赖：

   ```bash
   pip install -r requirements.txt
   ```

这样，您就可以轻松管理和共享项目的依赖项。