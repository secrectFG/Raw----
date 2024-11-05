
import os
import shutil



src_folder = r'Z:\视频&照片\2021\整理'
dest_folder = r'Z:\视频&照片\2021\2021-03-24'

# 遍历源文件夹中的所有文件
for root, _, files in os.walk(src_folder):
    for file in files:
        file_path = os.path.join(root, file)
        # print(file_path)
        file_dir = os.path.dirname(file_path)
        # print(file_dir)
        file_name = os.path.basename(file_path)
        # print(file_name)
        filename_no_ext = os.path.splitext(file_name)[0]

        #从dest_folderz中找到同名文件.xmp
        targetfilename = filename_no_ext+'.xmp'
        dest_file_path = os.path.join(dest_folder, targetfilename)
        if os.path.exists(dest_file_path):
            print(f'move {dest_file_path} to {file_dir}')
            shutil.move(dest_file_path, file_dir)

        targetfilename = filename_no_ext+'.tif'
        dest_file_path = os.path.join(dest_folder, targetfilename)
        if os.path.exists(dest_file_path):
            print(f'move {dest_file_path} to {file_dir}')
            shutil.move(dest_file_path, file_dir)

        targetfilename = filename_no_ext+'.psd'
        dest_file_path = os.path.join(dest_folder, targetfilename)
        if os.path.exists(dest_file_path):
            print(f'move {dest_file_path} to {file_dir}')
            shutil.move(dest_file_path, file_dir)
            
        