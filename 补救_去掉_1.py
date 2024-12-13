

import os


target_folder = r'Z:\照片\2020\2020-01-29'

for file in os.listdir(target_folder):
    target_ext = '.jpg'
    if file.lower().endswith(target_ext):
        
        file_path = os.path.join(target_folder, file)
        file_name, file_ext = os.path.splitext(file)
        if (".tif"+target_ext) in file:
            file_path = os.path.join(target_folder, file)
            try:
                os.rename(file_path, file_path.replace(".tif", ""))
            except Exception as e:
                print(f"重命名文件失败: {file_path} -> {file_path.replace('.tif', '')}")
                print(f"错误信息: {e}")

        if file_name.endswith('_1'):
            new_file_name = file_name[:-2] + file_ext
            new_file_path = os.path.join(target_folder, new_file_name)
            try:
                os.rename(file_path, new_file_path)
            except Exception as e:
                print(f"重命名文件失败: {file_path} -> {new_file_path}")
                print(f"错误信息: {e}")

            print(f"重命名文件: {file_path} -> {new_file_path}")
            for file2 in os.listdir(target_folder):
                file_path2 = os.path.join(target_folder, file2)
                file_name2, file_ext2 = os.path.splitext(file2)
                if file_name2 == file_name and file_path != file_path2:
                    new_file_path = os.path.join(target_folder, new_file_name) + file_ext2
                    try:
                    
                        os.rename(file_path2, new_file_path)
                    except Exception as e:
                        print(f"重命名文件失败: {file_path2} -> {new_file_path}")
                        print(f"错误信息: {e}")
                    print(f"重命名文件: {file_path2} -> {new_file_path}")