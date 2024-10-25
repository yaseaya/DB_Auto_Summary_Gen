import json
# import Utility_Str


class MonitorFolder:
    def __init__(self, name, path, target_Folder_Name, name_target, extensions, execution_cmd, File_Handling_After_Execution, MoveCopyTo, BackupTo):
        self.name = name
        self.path = path
        self.target_Folder_Name = target_Folder_Name
        self.name_target = name_target
        self.extensions = extensions
        self.execution_cmd = execution_cmd
        self.File_Handling_After_Execution = File_Handling_After_Execution
        self.MoveCopyTo = MoveCopyTo
        self.BackupTo = BackupTo

def Find_FolderConf(folders, folder_name):
    """
    通过查找文件夹名称返回 MonitorFolder 实例。

    参数:
    - folders: MonitorFolder 实例的列表
    - folder_name: 要查找的文件夹名称

    返回:
    - MonitorFolder 实例或 None
    """
    for folder in folders:
        if folder.name == folder_name:
            return folder
    return None  # 如果未找到，返回 None

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
                    folder['target_Folder_Name'],
                    folder['name_target'],
                    folder['extensions'],
                    folder['execution_cmd'],
                    folder['File_Handling_After_Execution'],
                    folder['MoveCopyTo'],
                    folder['BackupTo']
                )
                monitor_folder_instances.append(monitor_folder_instance)

            return monitor_folder_instances  # 返回 MonitorFolder 实例列表
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
