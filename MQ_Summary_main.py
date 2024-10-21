import pika
import subprocess
import time

# 设计思路
# 本程序使用RabbitMQ作为消息队列，处理来自txt_file_queue和av_file_queue的消息。
# 当接收到txt_file_queue的消息时，启动Doubao_Art_summary.py进行处理。
# 当接收到av_file_queue的消息时，启动call_Gen_Artical.py进行处理。
# 使用消息确认机制和预取计数确保任务的顺序处理。

# 使用说明
# 1. 确保RabbitMQ服务正在运行。
# 2. 运行本程序后，它将开始监听两个队列：txt_file_queue和av_file_queue。
# 3. 发送消息到这些队列以触发相应的处理程序。

def callback_txt_file_queue(ch, method, properties, body):
    txt_file_name = body.decode()  # 解码接收到的消息
    print(f"Received from txt_file_queue: {txt_file_name}")
    
    try:
        from DouBao_Article_Summary import main as doubao_art_summary_main
        doubao_art_summary_main(txt_file_name)  # 调用Doubao_Art_summary的主函数
        subprocess.Popen(['python', 'Doubao_Article_summary.py', txt_file_name])  # 启动另一个Python程序
    except FileNotFoundError:
        print("文件或目录不存在")  # 捕获文件未找到异常
        
    # 手动确认消息
    ch.basic_ack(delivery_tag=method.delivery_tag)

def callback_av_file_queue(ch, method, properties, body):
    av_file_name = body.decode()  # 解码接收到的消息
    print(f"Received from av_file_queue: {av_file_name}")
    
    # 启动另一个Python程序，并传递文件名作为参数
    try:
        subprocess.Popen(['python', 'call_Gen_Artical.py', av_file_name])  # 启动处理程序
    except FileNotFoundError:
        print("文件或目录不存在")  # 捕获文件未找到异常
    
    # 手动确认消息
    ch.basic_ack(delivery_tag=method.delivery_tag)

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))  # 连接到RabbitMQ
    channel = connection.channel()

    # 清除已存在的txt_file_queue
    channel.queue_delete(queue='txt_file_queue')
    # 清除已存在的av_file_queue
    channel.queue_delete(queue='av_file_queue')

    channel.queue_declare(queue='txt_file_queue')  # 声明txt_file_queue
    channel.queue_declare(queue='av_file_queue')   # 声明av_file_queue

    # 设置预取计数为1，确保一个任务完成后再接收下一个任务
    channel.basic_qos(prefetch_count=1)

    # 消费者注册
    channel.basic_consume(queue='txt_file_queue', on_message_callback=callback_txt_file_queue, auto_ack=False)
    channel.basic_consume(queue='av_file_queue', on_message_callback=callback_av_file_queue, auto_ack=False)

    print('Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()  # 开始消费消息

def send_message_Txt_File_Ready(txt_file_name):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))  # 连接到RabbitMQ
    channel = connection.channel()
    channel.queue_declare(queue='txt_file_queue')  # 声明txt_file_queue
    channel.basic_publish(exchange='', routing_key='txt_file_queue', body=txt_file_name)  # 发送消息
    print(f"Sent {txt_file_name} to txt_file_queue")            
    connection.close()  # 关闭连接

def send_av_message(av_file_name):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))  # 连接到RabbitMQ
    channel = connection.channel()
    channel.queue_declare(queue='av_file_queue')  # 声明av_file_queue
    channel.basic_publish(exchange='', routing_key='av_file_queue', body=av_file_name)  # 发送消息
    print(f"Sent {av_file_name} to av_file_queue")
    connection.close()  # 关闭连接

if __name__ == "__main__":
    main()  # 运行主函数
