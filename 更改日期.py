import os
from PIL import Image
import piexif
from datetime import datetime

def change_photo_date(photo_path, new_date):
    # 读取图像
    img = Image.open(photo_path)
    
    # 获取现有的 EXIF 数据
    exif_dict = piexif.load(img.info['exif']) if 'exif' in img.info else {}
    
    # 目标日期格式 "YYYY:MM:DD HH:MM:SS"
    new_exif_date = new_date.strftime('%Y:%m:%d %H:%M:%S')
    
    # 更新拍摄日期 (DateTimeOriginal, 0x9003)
    if piexif.ExifIFD.DateTimeOriginal in exif_dict['Exif']:
        exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal] = new_exif_date.encode('utf-8')
    
    # 重新编码 EXIF 数据并将其写回图片
    exif_bytes = piexif.dump(exif_dict)
    
        # 确保图片保留原始质量（如果是 JPEG 格式）
    if photo_path.lower().endswith(('jpg', 'jpeg')):
        img.save(photo_path, exif=exif_bytes, quality=100, optimize=True)  # 保持高质量，避免压缩
    else:
        img.save(photo_path, exif=exif_bytes)  # 对于其他格式，直接保存
    print(f"Updated date for {photo_path} to {new_exif_date}")

def update_photos_in_folder(folder_path, new_date):
    # 遍历文件夹中的所有文件
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(('jpg', 'jpeg')):
                photo_path = os.path.join(root, file)
                change_photo_date(photo_path, new_date)

# 设置新的拍摄日期
new_date = datetime(2024, 1, 18, 0, 0, 0)

# 调用函数更新文件夹中的所有照片
update_photos_in_folder(r'I:\同步用\新建文件夹', new_date)
