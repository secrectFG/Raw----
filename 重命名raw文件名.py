
import os
import exifread

cam_type = ['.nef','.cr2','.arw','.rw2']
path = r'Z:\视频&照片\2017\2017-11-16'

def main():
    for filename in os.listdir(path):
        file_name, file_extension = os.path.splitext(filename)
        # print(filename)
        if file_extension.lower() in cam_type:
            #读取相机型号
            f = open(os.path.join(path,filename),'rb')
            tags = exifread.process_file(f)
            new_name = None
            cam = tags['Image Model'].values
            if cam == 'ILCE-7RM2':
                new_name = filename.replace('A7','A7R2')
            elif cam == 'ILCE-7RM3':
                cam = 'A7R3'
            if not new_name:
                print(f'识别失败 {filename}')
                continue
            f.close()
            os.rename(os.path.join(path,filename),os.path.join(path,new_name))
            print(filename + '->' + new_name)

            for ext in ['.xmp', '.tif', '.psd', '.jpg','-编辑.tif', '-编辑.psd', '-编辑.jpg']:
                if os.path.exists(os.path.join(path,file_name + ext)):
                    os.rename(os.path.join(path,file_name + ext),os.path.join(path,new_name + ext))
                    print(file_name + ext + ' -> ' + new_name + ext)
            

if __name__ == '__main__':
    main()