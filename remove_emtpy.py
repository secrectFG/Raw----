#删除所有空文件夹
import os

def remove_empty_folders(path):
    for root, dirs, files in os.walk(path, topdown=False):
        for name in dirs:
            dir_path = os.path.join(root, name)
            if not os.listdir(dir_path):
                os.rmdir(dir_path)
                print(f"Removed empty folder: {dir_path}")

# 调用函数删除空文件夹
remove_empty_folders(r'Z:\视频&照片\2014及以前')