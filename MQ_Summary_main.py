import pika
import subprocess
import time
import logging
from Utility_Str import Utility_Str

# 配置日志
logging.basicConfig(level=logging.INFO,  # 设置日志级别
                    format='%(asctime)s - %(levelname)s - %(message)s')  # 设置日志格式

# 设计思路
# 本程序使用RabbitMQ作为消息队列，处理来自txt_file_queue和av_file_queue的消息。
# 当接收到txt_file_queue的消息时，启动Doubao_Art_summary.py进行处理。
# 当接收到av_file_queue的消息时，启动call_Gen_Artical.py进行处理。
# 使用消息确认机制和预取计数确保任务的顺序处理。

# 使用说明
# 1. 确保RabbitMQ服务正在运行。
# 2. 运行本程序后，它将开始监听两个队列：txt_file_queue和av_file_queue。
# 3. 发送消息到这些队列以触发相应的处理程序。

def reconnect_MQ():
    retry_count = 0
    while retry_count < 5:
        try:
            # 在 RabbitMQ 中，心跳时间的缺省值通常为 60 秒。这意味着如果在 60 秒内没有任何活动，RabbitMQ 将关闭连接。
            # 设置心跳时间为600秒
            connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', heartbeat=600))  # 重新连接到RabbitMQ
            channel = connection.channel()
            # 重新声明队列和注册消费者
            channel.queue_declare(queue='txt_file_queue')
            channel.queue_declare(queue='av_file_queue')
            channel.basic_consume(queue='txt_file_queue', on_message_callback=callback_txt_file_queue, auto_ack=False)
            channel.basic_consume(queue='av_file_queue', on_message_callback=callback_av_file_queue, auto_ack=False)
            print("重新连接成功")
            return channel  # 返回连接的channel
        except pika.exceptions.AMQPConnectionError:
            print("连接失败，正在重试...")
            time.sleep(5)  # 等待5秒后重试
            retry_count += 1
def callback_txt_file_queue(ch, method, properties, body):
    
    print("输出全部参数: " + body.decode())
    # 使用 split() 方法分割字符串，并去掉引号
    txt_file_name = Utility_Str.extract_parameters_to_str( body.decode(), 1 )   # 解码并提取第一个参数
    print("输出第一个参数 txt_file_name: " + txt_file_name)  # 输出第一个参数  
    txt_file_name_target = Utility_Str.extract_parameters_to_str( body.decode(), 2 )  # 解码接收到的消息 并获取第二个参数
    print("输出第二个参数 txt_file_name_target: " + txt_file_name_target)  # 输出第二个参数
    print(f"Received from txt_file_queue: {txt_file_name}")
    
    try:
        from DouBao_Article_Summary import main as doubao_art_summary_main
        doubao_art_summary_main(txt_file_name, txt_file_name_target)  # 调用Doubao_Art_summary的主函数
        # subprocess.Popen(['python', 'Doubao_Article_summary.py', txt_file_name, txt_file_name_target])  # 启动另一个Python程序，并传递文件名作为参数
    except FileNotFoundError:
        print("文件或目录不存在")  # 捕获文件未找到异常
    except Exception as e:
        print(f"处理消息时发生错误: {e}")  # 捕获其他异常
        
    # 手动确认消息
    try:
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except pika.exceptions.StreamLostError:
        print("连接丢失，无法确认消息。")  # 捕获连接丢失异常
        reconnect_MQ()
        print("手动确认消息 AGAIN。")
        ch.basic_ack(delivery_tag=method.delivery_tag)

def callback_av_file_queue(ch, method, properties, body):
    av_file_name = body.decode()  # 解码接收到的消息
    print(f"Received from av_file_queue: {av_file_name}")
    
    # 启动另一个Python程序，并传递文件名作为参数
    try:
        subprocess.Popen(['python', 'call_Gen_Artical.py', av_file_name])  # 启动处理程序
    except FileNotFoundError:
        print("文件或目录不存在")  # 捕获文件未找到异常
    except Exception as e:
        print(f"处理消息时发错误: {e}")  # 捕获其他异常
    
    # 手动确认消息
    try:
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except pika.exceptions.StreamLostError:
        print("连接丢失，无法确认消息。")  # 捕获连接丢失异常
        reconnect_MQ()
        print("手动确认消息 AGAIN。")
        ch.basic_ack(delivery_tag=method.delivery_tag)

def main():
    logging.info("程序开始运行")
    # 设置心跳时间为600秒
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', heartbeat=600))  # 连接到RabbitMQ
    channel = connection.channel()

    if(1):  # 清除已存在的txt_file_queue
        channel.queue_delete(queue='txt_file_queue')
        # 清除已存在的av_file_queue
        channel.queue_delete(queue='av_file_queue')

        channel.queue_declare(queue='txt_file_queue')  # 声明txt_file_queue
        channel.queue_declare(queue='av_file_queue')   # 声明av_file_queue

    # 设置预取计数为1，确保一个任务完成后再接收下一个任务
    channel.basic_qos(prefetch_count=1)

    # 消费者注册
    channel.basic_consume(queue='txt_file_queue', on_message_callback=callback_txt_file_queue, auto_ack=False)  # 消费者注册
    channel.basic_consume(queue='av_file_queue', on_message_callback=callback_av_file_queue, auto_ack=False)  # 消费者注册

    print('Waiting for messages. To exit press CTRL+C')
    try:
        channel.start_consuming()  # 开始消费消息
    except pika.exceptions.ConnectionClosed:
        print("连接丢失，试重新连接...")
        # 重新连接的逻辑
        time.sleep(5)
        reconnect_MQ()

    except pika.exceptions.ConnectionWrongStateError:
        print("连接状态错误，请检查连接设置。")
        # 处理连接状态错误的逻辑
        time.sleep(5)
        reconnect_MQ()        

    logging.info("程序运行结束")

def send_message_Txt_File_Ready(txt_file_name):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))  # 连接到RabbitMQ
    channel = connection.channel()
    channel.queue_declare(queue='txt_file_queue')  # 声明txt_file_queue
    channel.basic_publish(exchange='', routing_key='txt_file_queue', body=txt_file_name,
        properties=pika.BasicProperties(
            delivery_mode=2,  # 使消息持久化
        ))  # 发送消息
    print(f"Sent {txt_file_name} to txt_file_queue")            
    connection.close()  # 关闭连接

def send_av_message(av_file_name):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))  # 连接到RabbitMQ
    channel = connection.channel()
    channel.queue_declare(queue='av_file_queue')  # 声明av_file_queue
    channel.basic_publish(exchange='', routing_key='av_file_queue', body=av_file_name,
        properties=pika.BasicProperties(
            delivery_mode=2,  # 使消息持久化
        ))  # 发送消
    print(f"Sent {av_file_name} to av_file_queue")
    connection.close()  # 关闭连接

if __name__ == "__main__":
    main()  # 运行主函数
