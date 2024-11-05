import os
import shutil
import exifread
from datetime import datetime
import ffmpeg
# import queue
# import concurrent.futures
# import time

src_folder = r'Z:\视频&照片\2017'
# dest_folder = r'Z:\视频&照片\2014及以前'
dest_folder = src_folder
unsort_folder = r'Z:\视频&照片未整理'

def get_photo_date(photo_path):
    """读取照片的拍摄日期（如果有EXIF信息）"""
    with open(photo_path, 'rb') as f:
        tags = exifread.process_file(f)
        date_taken = tags.get('EXIF DateTimeOriginal')
        if date_taken:
            try:
                date_taken = datetime.strptime(str(date_taken), '%Y:%m:%d %H:%M:%S')
            except ValueError:
                date_taken = None
        return date_taken
    
def get_video_creation_date(video_path):
    """使用ffmpeg获取视频的创建日期"""
    try:
        # 使用 ffmpeg 获取视频的元数据
        metadata = ffmpeg.probe(video_path, v='error', select_streams='v:0', show_entries='format_tags=creation_time')
        creation_time_str = metadata['format']['tags']['creation_time']
        
        # 转换为日期时间格式
        creation_time = datetime.strptime(creation_time_str, "%Y-%m-%dT%H:%M:%S.%fZ")
        return creation_time
    except Exception as e:
        print(f"获取视频创建时间失败 {video_path}, \n使用文件系统时间: {e}")
        return get_file_creation_date(video_path)


def get_file_creation_date(file_path):
    """读取文件的创建时间"""
    timestamp = os.path.getmtime(file_path)
    return datetime.fromtimestamp(timestamp)

def organize_media_by_date(src_folder, dest_folder):
    """根据文件的日期（拍摄或创建日期）整理文件到目标文件夹"""
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
    # futures = []
    # max_workers = 2
    # with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
    for root, _, files in os.walk(src_folder):
        for file in files:
            file_path = os.path.join(root, file)
            
            if not os.path.exists(file_path):
                continue

            #从文件路径获取日期
            file_date = os.path.basename(root)

            if file_date < '2017-02-06':
                continue

            move_photo(file, file_path)
                # 提交任务
        #         future = executor.submit(move_photo, file, file_path)
        #         futures.append(future)

        #         # 控制并发数量
        #         if len(futures) >= max_workers:
        #             # 等待第一个完成的任务
        #             done, _ = concurrent.futures.wait(futures, return_when=concurrent.futures.FIRST_COMPLETED)
        #             # 移除已完成的任务
        #             futures = [f for f in futures if f not in done]

        # # 等待所有任务完成
        # concurrent.futures.wait(futures)
            
            


def move_photo(file, file_path):
    date_taken = None
    is_target = False

    # 判断文件是否为照片
    if file.lower().endswith(('.jpg', '.jpeg', '.cr2', '.nef', '.raw', '.arw', '.tif', '.rw2')):
        date_taken = get_photo_date(file_path)
        is_target = True
    
    # 如果不是照片，判断是否为视频
    elif file.lower().endswith(('.mp4', '.mov', '.avi', '.mkv', '.flv', '.wmv')):
        date_taken = get_video_creation_date(file_path)
        is_target = True

    # 若存在日期信息，将文件移动到相应的日期文件夹
    if date_taken:
        date_folder = date_taken.strftime('%Y-%m-%d')
        target_folder = os.path.join(dest_folder, date_folder)
        

        #判断是否在同一个文件夹
        if os.path.dirname(file_path) == target_folder or target_folder in file_path:
            content = f"文件已在目标文件夹中: {file_path}"
            print(f"\r{content:<150}", end="\r")
            return 
        try:
            if not os.path.exists(target_folder):
                os.makedirs(target_folder)
            shutil.move(file_path, target_folder)
        except:
            #如果文件已存在，重命名
            if os.path.exists(os.path.join(target_folder, file)):
                new_file_path = os.path.join(target_folder, file + '_1')
                shutil.move(file_path, new_file_path)
                print(f"文件已存在，重命名并移动: {new_file_path}")
            else:
                print(f"文件已存在，移动失败: {file_path}")
                return
            

        file_path_no_ext = os.path.splitext(file_path)[0]

        filename = os.path.basename(file_path)
        filename_no_ext = os.path.splitext(filename)[0]
        for ext in ['.xmp', '.tif', '.psd', '-编辑.tif', '-编辑.psd']:
            targetfilename = filename_no_ext + ext
            dest_file_path = os.path.join(unsort_folder, targetfilename)
            if os.path.exists(dest_file_path):
                print(f'move {dest_file_path} to {target_folder}')
                shutil.move(dest_file_path, target_folder)
            if os.path.exists(file_path_no_ext + ext):
                shutil.move(file_path_no_ext + ext, target_folder)

        print(f"移动文件: {file_path} 到 {target_folder}")
    elif is_target:
        print(f"未找到日期信息 {file_path}")


def main():
    print('开始')
    organize_media_by_date(src_folder, dest_folder)
    print("完成")

if __name__ == "__main__":
    main()
    