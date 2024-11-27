import os

def remove_empty_folders(path):
    # 遍历目录，topdown=False 确保从子目录开始遍历
    for root, dirs, files in os.walk(path, topdown=False):
        for name in dirs:
            dir_path = os.path.join(root, name)
            # 判断目录是否为空
            if not os.listdir(dir_path):  # 如果目录为空
                try:
                    os.rmdir(dir_path)  # 删除空文件夹
                    print(f"Removed empty folder: {dir_path}")
                except OSError as e:
                    print(f"Error removing {dir_path}: {e}")

# 调用函数删除空文件夹

# input_folader = input("请输入文件夹路径：")
input_folader = r"H:\转码"

remove_empty_folders(input_folader)
