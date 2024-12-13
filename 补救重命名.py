import exifread
import os
path = r'Z:\照片\2017\2017-11-13 雷姆浴衣'

for filename in os.listdir(path):
    if filename.endswith(('.ARW.xmp','.NEF.xmp','.ARW-编辑.tif','.ARW-编辑.jpg', '.NEF-编辑.tif', '.NEF-编辑.jpg')):
        newfilename = filename.replace('.ARW', '').replace('.NEF', '')
        os.rename(os.path.join(path, filename), os.path.join(path, newfilename))
        print(f'Renamed {filename} to {newfilename}')




