import pika
import argparse

# 设计思路
# 本程序用于发送消息到RabbitMQ的两个队列：txt_file_queue和av_file_queue。
# 通过调用send_message_Txt_File_Ready和send_message_AV_File_Ready函数，发送相应的文件名消息。

# 使用说明
# 1. 运行本程序将发送示例文件名到txt_file_queue和av_file_queue。
# 2. 确保RabbitMQ服务正在运行，并且相应的消费者程序正在监听这些队列。

def send_message_Txt_File_Ready(txt_file_name):
    # 创建与RabbitMQ的连接
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()  # 创建频道
    channel.queue_declare(queue='txt_file_queue')  # 声明txt_file_queue
    channel.basic_publish(exchange='', routing_key='txt_file_queue', body=txt_file_name)  # 发送消息
    print(f"Sent {txt_file_name} to txt_file_queue")  # 打印发送的消息
    connection.close()  # 关闭连接

def send_message_AV_File_Ready(av_file_name):
    # 创建与RabbitMQ的连接
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()  # 创建频道
    channel.queue_declare(queue='av_file_queue')  # 声明av_file_queue    
    channel.basic_publish(exchange='', routing_key='av_file_queue', body=av_file_name)  # 发送消息
    print(f"Sent {av_file_name} to av_file_queue")  # 打印发送的消息
    connection.close()  # 关闭连接

def main(file_type, file_name):
    """
    发送文件名到RabbitMQ的txt_file_queue或av_file_queue。

    参数:
    - file_type (str): 文件类型，必须是'txt'或'av'。
    - file_name (str): 要发送的文件名。
    """
    if file_type == "txt":
        send_message_Txt_File_Ready(file_name)
    elif file_type == "av":
        send_message_AV_File_Ready(file_name)
    else:
        print("Invalid type. Please use 'txt' or 'av'.")

if __name__ == "__main__":
    # 使用argparse解析命令行参数
    parser = argparse.ArgumentParser(description='Send messages to RabbitMQ queues.')
    parser.add_argument('file_type', type=str, help="File type: 'txt' or 'av'")
    parser.add_argument('file_name', type=str, help="The name of the file to send")

    args = parser.parse_args()  # 解析参数

    # 调用主函数
    main(args.file_type, args.file_name)
