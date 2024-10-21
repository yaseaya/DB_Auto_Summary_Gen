import pika

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

if __name__ == "__main__":
    send_message_Txt_File_Ready("example_file_02.txt")  # 发送示例文件名到txt_file_queue
    send_message_AV_File_Ready("example_av_file.txt")  # 发送示例文件名到av_file_queue     
