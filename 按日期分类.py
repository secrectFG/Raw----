import os
import shutil
import exifread
from datetime import datetime
import ffmpeg
#日志
import mylogger
logger = mylogger.logger

src_folder = r'Z:\照片\2020'
dest_folder = src_folder #只有在年份目录才能这样做，否则会很糟糕

# dest_folder = r'Z:\照片\整理'

unsort_folder = r'Z:\视频\未整理'

def count_files_in_folder(folder_path):
    total_files = 0
    for root, dirs, files in os.walk(folder_path):
        total_files += len(files)  # 每次循环累加文件数

    return total_files

is_debug = False

old_move = shutil.move

def shutil_move(src, dst):
    try:
        if is_debug:
            print(f"移动文件: {src} -> {dst}")
        else:
            old_move(src, dst)
    except Exception as e:
        logger.error(f"移动文件失败: {src} -> {dst}, 错误: {e}")

shutil.move = shutil_move

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

def organize_media_by_date(src_folder, dest_folder, total_file_count):
    """根据文件的日期（拍摄或创建日期）整理文件到目标文件夹"""
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    for root, _, files in os.walk(src_folder):
        for file in files:
            file_path = os.path.join(root, file)
            
            if not os.path.exists(file_path):
                continue

            #从文件路径获取日期
            file_date = os.path.basename(root)

            # if file_date < '2017-02-15':
            #     continue

            move_photo(file, file_path, total_file_count)

            
def move_file_auto_rename(file_path, target_folder):
    file = os.path.basename(file_path)  # 获取文件名（包括扩展名）
    target_path = os.path.join(target_folder, file)
    
    # 检查文件是否已经存在
    if os.path.exists(target_path):
        # 分离文件名和扩展名
        file_name, file_extension = os.path.splitext(file)
        
        # 创建新文件名，避免覆盖已存在的文件
        new_file_name = file_name + '_1' + file_extension  # 在文件名后加上 '_1'
        new_file_path = os.path.join(target_folder, new_file_name)
        
        # 移动并重命名文件
        shutil.move(file_path, new_file_path)
        logger.warning(f"文件已存在，重命名并移动: {new_file_path}")
    else:
        # 如果文件不存在，直接移动
        shutil.move(file_path, target_path)
        print(f"文件已移动: {target_path}")

count = 0

def move_photo(file2, file_path, total_file_count):
    date_taken = None
    is_target = False
    global count
    count += 1

    # 判断文件是否为照片
    if file2.lower().endswith(('.jpg', '.jpeg', '.cr2', '.nef', '.raw', '.arw', '.tif', '.rw2', '.dng', '.png')):
        date_taken = get_photo_date(file_path)
        is_target = True
    
    # 如果不是照片，判断是否为视频
    elif file2.lower().endswith(('.mp4', '.mov', '.avi', '.mkv', '.flv', '.wmv')):
        date_taken = get_video_creation_date(file_path)
        is_target = True

    # 若存在日期信息，将文件移动到相应的日期文件夹
    if date_taken:
        date_folder = date_taken.strftime('%Y-%m-%d')
        target_folder = os.path.join(dest_folder, date_folder)
        

        #判断是否在同一个文件夹
        if os.path.dirname(file_path) == target_folder or target_folder in file_path:
            content = f"文件已在目标文件夹中: {file_path} count: {count} progress: {count/total_file_count*100:.2f}%"
            print(f"\r{content:<100}", end="\r")
            return 
        try:
            if not os.path.exists(target_folder):
                os.makedirs(target_folder)
            shutil.move(file_path, target_folder)
        except:
            #如果文件已存在，重命名
            move_file_auto_rename(file_path, target_folder)
            return
            

        filename = os.path.basename(file_path)
        filename_no_ext,ext = os.path.splitext(filename)
        filedir = os.path.dirname(file_path)
        #walkdir
        for root, dirs, files in os.walk(filedir):
            for file2 in files:
                if file2 == filename:
                    continue
                if filename_no_ext in file2 and not file2.endswith(('.nef', '.cr2', '.arw', '.raw', '.rw2',)):
                    file_path2 = os.path.join(root, file2)
                    move_file_auto_rename(file_path2, target_folder)
                    # count += 1


                # for ext in ['.xmp', '.tif', '.psd', '-编辑.tif', '-编辑.psd']:
                #     targetfilename = filename_no_ext + ext
                #     dest_file_path = os.path.join(unsort_folder, targetfilename)
                #     if os.path.exists(dest_file_path):
        # for ext in ['.xmp', '.tif', '.psd', '-编辑.tif', '-编辑.psd']:
        #     targetfilename = filename_no_ext + ext
        #     dest_file_path = os.path.join(unsort_folder, targetfilename)
        #     if os.path.exists(dest_file_path):
        #         print(f'move {dest_file_path} to {target_folder}')
        #         move_file_auto_rename(dest_file_path, target_folder)
        #     if os.path.exists(file_path_no_ext + ext):
        #         move_file_auto_rename(file_path_no_ext + ext, target_folder)

        print(f"移动文件: {file_path} 到 {target_folder} progress: {count/total_file_count*100:.2f}%")
    elif is_target:
        print(f"未找到日期信息 {file_path}")
        #分类到无日期文件夹
        target_folder = os.path.join(dest_folder, '无日期')
        if not os.path.exists(target_folder):
            os.makedirs(target_folder)
        move_file_auto_rename(file_path, target_folder)


def main():
    print('开始')
    total_file_count = count_files_in_folder(src_folder)
    print(f"总文件数: {total_file_count}")
    organize_media_by_date(src_folder, dest_folder, total_file_count)
    print()
    print("完成")

if __name__ == "__main__":
    main()
    