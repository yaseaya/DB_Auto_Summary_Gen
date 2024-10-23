import os
import time
import json
import watchdog.events
import watchdog.observers
import Conf_Load
from send_message_AutoSummary import send_message_Txt_File_Ready
# from Conf_Load import load_settings, Find_FolderConf  # 使用 conf_load.py 中的 load_settings 函数

class FileEventHandler(watchdog.events.FileSystemEventHandler):
    def __init__(self, extensions, folder_instance):  # 添加构造函数参数
        self.extensions = extensions
        self.folder_instance = folder_instance  # 保存文件夹实例
        self.execution_cmd = folder_instance.get('execution_cmd', '')  # 使用 get 方法安全获取 execution_cmd

    def on_created(self, event):
        # 检查是否是文件
        if not event.is_directory:
            # 获取文件扩展名
            _, ext = os.path.splitext(event.src_path)
            # 检查文件扩展名是否在监控列表中
            if ext in self.extensions:
                print(f"New file created: {event.src_path}")
                # 添加执行命令
                # self.execution_cmd = self.execution_cmdfolder_instance_ToBe_Summarized.execution_cmd  # 使用正确的文件夹实例
                cmd = self.execution_cmd + " " + event.src_path
                print(cmd)
                # os.system(cmd)
                send_message_Txt_File_Ready(event.src_path)

def main():
    # 加载配置
    folders = Conf_Load.load_settings('Setting.Conf')
    folder_instance_ToBe_Summarized = Conf_Load.load_settings('Setting.Conf')  # 确保正确加载配置
    # folder_instance_ToBe_ASR = Conf_Load.Find_FolderConf(folders, 'File_Monitor_ToBe_ASR')

    # 监控的文件扩展名
    extensions = ['.txt', '.mp4', '.txt', '.pdf', '.csv', '.docx', '.doc', '.xlsx', '.xls', '.pptx', '.ppt', '.mobi', '.epub', '.png', '.jpeg', '.jpg']  # 可以根据需要添加其他扩展名
    # 创建事件处理器
    for folder in folders:
        event_handler = FileEventHandler(extensions, folder)  # 使用正确的文件夹实例
        observer = watchdog.observers.Observer()  # 创建观察者实例
        observer.schedule(event_handler, folder['path'], recursive=False)  # 在创建观察者后进行调度
        # 启动观察者
        observer.start()
        print("Monitoring folders...")
     
    try:
        while True:
            time.sleep(1)  # 让主线程保持运行
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main()
