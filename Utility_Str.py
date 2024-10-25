import re
import os

class Utility_Str:
    @staticmethod
    def add_quotes_to_string(input_string):
        """
        在字符串的左边和右边添加引号。

        :param input_string: 输入的字符串
        :return: 带引号的字符串
        """
        return "'" + input_string + "'"
    def Remove_quotes_to_string(input_string):
        """
        在字符串的左边和右边去除引号。

        :param input_string: 输入的字符串
        :return: 去除首尾引号的字符串
        """
        # 去除首尾引号
        return input_string.strip("'")  # 去除首尾引号
    
    
    @staticmethod
    def extract_parameters_to_str(messages, extract_messsage_position = -1):
        """
        从接收到的消息中提取参数，确保文件名中包含空格的部分被正确处理。

        :param messages: 包含参数的字符串   
        :param extract_messsage_position: 提取参数的位置，-1表示提取所有参数
        :return: 参数的字符串   
        """
        # 使用正则表达式提取 ' ' 之间的字符串
        params = re.findall(r"'(.*?)'", messages)

        # 确保参数数量正确
        str_params = ""
        iPos = 0
        for param in params:
            str_params += "'" + param + "'" + " "

            # 如果 extract_messsage_position不为-1，并且找到了参数的位置，返回该加上 ' ' 的参数
            if (iPos == (extract_messsage_position - 1)) and (extract_messsage_position != -1):
                return ("'" + param + "'")
            
            # 找到参数的位置，返回
            iPos += 1

        # 返回所有参数
        return str_params
    
    @staticmethod    # 在文件开头添加以下函数定义
    def generate_unique_filename(filename):
        print(f"filename: {filename}")
        base, extension = os.path.splitext(filename)  # 分离文件名和扩展名
        counter = 1
        new_filename = f"{base}_{counter}{extension}"  # 创建新的文件名
        print(f"new_filename: {new_filename}")
        while os.path.exists(new_filename):  # 检查文件是否存在
            counter += 1
            new_filename = f"{base}_{counter}{extension}"  # 生成新的文件名
            print(f"new_filename2: {new_filename}")
            return new_filename  # 返回不重复的文件名
        
        return new_filename


    
