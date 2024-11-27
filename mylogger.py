#日志
import logging

# 创建一个logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


# 创建一个handler，用于写入日志文件
file_handler = logging.FileHandler('move-xmp-log.txt', encoding='utf-8')
file_handler.setLevel(logging.INFO)

# 创建一个handler，用于输出到控制台
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# 设置日志格式
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
# 添加处理器
logger.addHandler(file_handler)
logger.addHandler(console_handler)
