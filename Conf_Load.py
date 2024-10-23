import json

class MonitorFolder:
    def __init__(self, name, path, description, extensions, execution_cmd, File_Handling_After_Execution, MoveCopyTo, BackupTo):
        self.name = name
        self.path = path
        self.description = description
        self.extensions = extensions
        self.execution_cmd = execution_cmd
        self.File_Handling_After_Execution = File_Handling_After_Execution
        self.MoveCopyTo = MoveCopyTo
        self.BackupTo = BackupTo

    def Find_FolderConf(self, folder_name):
        """
        通过查找folder's name 返回 monitor_folder_instances。

        参数:
        - folder_name: 文件夹的名称

        返回:
        - list: 包含指定文件夹名称的 monitor_folder_instances
        """
        return [folder for folder in self.monitor_folder_instances if folder.name == folder_name]

def load_settings(file_path):
    """
    使用UTF-8编码读取配置文件并返回内容。

    参数:
    - file_path: 配置文件的路径

    返回:
    - list: 配置文件的内容
    """
    try:
        with open(file_path, 'r', encoding='UTF-8', errors='ignore') as f:
            settings = json.load(f)
            monitor_folders = settings['Monitor_Folders']
            monitor_folder_instances = []
            for folder in monitor_folders:
                monitor_folder_instance = MonitorFolder(
                    folder['name'],
                    folder['path'],
                    folder['description'],
                    folder['extensions'],
                    folder['execution_cmd'],
                    folder['File_Handling_After_Execution'],
                    folder['MoveCopyTo'],
                    folder['BackupTo']
                )
                monitor_folder_instances.append(monitor_folder_instance)

                # print("文件夹名称:", monitor_folder_instance.name)
                # print("文件夹路径:", monitor_folder_instance.path)
                # print("文件夹描述:", monitor_folder_instance.description)
                # print("文件后缀名:", monitor_folder_instance.extensions)
                # print("执行命令:", monitor_folder_instance.execution_cmd)
                # print("文件操作动作:", monitor_folder_instance.File_Handling_After_Execution)
                # print("移动/复制到:", monitor_folder_instance.MoveCopyTo)
                # print("备份到:", monitor_folder_instance.BackupTo)
                # print("--------------------")

            return monitor_folders
    except FileNotFoundError:
        print(f"文件未找到: {file_path}")
    except json.JSONDecodeError:
        print(f"文件内容解析错误: {file_path}")
    except Exception as e:
        print(f"发生错误: {e}")

if __name__ == "__main__":
    settings = load_settings('Setting.Conf')
    if settings:
        print("配置文件内容:", settings)

