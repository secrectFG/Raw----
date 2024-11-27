
import os
import exifread

cam_type = ['.nef','.cr2','.arw','.rw2']
path = r'Z:\视频&照片\2016\2016-07-02'

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
                new_name = filename.replace('A7','R2')
            elif cam == 'ILCE-7RM3':
                new_name = filename.replace('A7','R3')
            elif cam == 'ILCE-6400':
                new_name = filename.replace('DSC','6400_')
            elif cam == 'NIKON D800':
                new_name = filename.replace('DSC','D800_')
            elif cam == 'DMC-GH4':
                new_name = filename.replace('_','_GH4_')
            elif cam == 'DMC-GH5':
                new_name = filename.replace('_','_GH5_')

            if not new_name:
                print(f'识别失败 {filename} cam: {cam}')
                continue
            f.close()
            os.rename(os.path.join(path,filename),os.path.join(path,new_name))
            print(filename + '->' + new_name)

            new_name_without_ext = os.path.splitext(new_name)[0]

            for ext in ['.xmp', '.tif', '.psd', '.jpg','-编辑.tif', '-编辑.psd', '-编辑.jpg', '-编辑_1.jpg']:
                if os.path.exists(os.path.join(path,file_name + ext)):
                    os.rename(os.path.join(path,file_name + ext),os.path.join(path,new_name_without_ext + ext))
                    print(file_name + ext + ' -> ' + new_name_without_ext + ext)
            

if __name__ == '__main__':
    main()