import time

# 设计思路
# 本程序用于处理接收到的txt文件名，模拟处理过程并打印当前时间。
# 通过循环模拟处理任务的执行。

# 使用说明
# 1. 该程序应由MQ_Summary_main.py调用，并传递txt文件名作为参数。
# 2. 运行时将打印处理状态和当前时间。

def main(txt_file_name):
    for _ in range(20):  # 模拟处理20次
        print("Doubao_Art_summary is running " + txt_file_name + " 当前时间: ", time.time())  # 打印处理状态和时间
        time.sleep(1)  # 每次处理间隔1秒
