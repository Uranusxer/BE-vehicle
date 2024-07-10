import re

def check_string_format(input_string, max_len):
    """
    检测输入字符串是否符合格式要求：
    1. 不存在空格
    2. 仅包含字母、数字、汉字和下划线
    3. 长度不超过限定字数max_len
    """
    # 正则表达式说明：
    # ^        : 字符串开始
    # [a-zA-Z0-9_\u4e00-\u9fa5]+ : 匹配一个或多个字母、数字、下划线或汉字
    # $        : 字符串结束
    pattern = r'^[a-zA-Z0-9_\u4e00-\u9fa5]+$'
    
    # 检查字符串是否匹配正则表达式，并检查长度
    if re.match(pattern, input_string) and len(input_string) <= max_len:
        return True
    else:
        return False
