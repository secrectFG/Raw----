import sys
import time

def print_progress_bar(iteration, total, prefix='', length=40, fill='█'):
    """
    打印进度条
    
    :param iteration: 当前迭代次数
    :param total: 总迭代次数
    :param prefix: 进度条前的提示信息
    :param length: 进度条的长度
    :param fill: 填充字符
    """
    percent = ("{0:.1f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    # sys.stdout.write(f'\r{prefix} |{bar}| {percent}% 完成')
    # sys.stdout.flush()
    print(f'\r{prefix} |{bar}| {percent}% 完成', end='\r')

print('开始任务')
print(f'\r1', end='\r')
print(f'\r2', end='\r')
print('test')
print(f'\r2', end='\r')
print(f'\r3', end='\r')
# 示例: 打印进度条
total = 100
for i in range(total):
    print_progress_bar(i + 1, total, prefix='进度')
    time.sleep(0.1)

print()  # 输出换行
print("任务完成!")
