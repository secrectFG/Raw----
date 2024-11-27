import os
import shutil
import requests
from bs4 import BeautifulSoup
#日志
import mylogger
logger = mylogger.logger



# 搜索文件的函数
def search_files(query):
    url = 'http://localhost:8081'  # Everything的HTTP服务地址（默认端口80）
    params = {'s': query}  # 's' 是Everything用来接受搜索查询的参数
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        return response.text  # 返回搜索结果（可以是XML或其他格式）
    else:
        print(f"搜索请求失败，状态码：{response.status_code}")
        return None  # 出现错误时返回None
    
def serarch_and_move(query):
    # print(f"正在搜索文件: {query}")
    # 示例使用
    results = search_files(query)
    # 解析HTML
    soup = BeautifulSoup(results, 'html.parser')
    # 找到文件列表
    file_rows = soup.find_all('tr', class_=['trdata1', 'trdata2'])

    # 提取文件信息
    file_list = []
    for row in file_rows:
        file_name = row.find('td', class_='file').get_text(strip=True)
        file_path = row.find('td', class_='pathdata').get_text(strip=True)
        # file_size = row.find('td', class_='sizedata').get_text(strip=True)
        # modified_date = row.find('td', class_='modifieddata').get_text(strip=True)
        
        file_list.append({
            'name': file_name,
            'path': file_path,
            # 'size': file_size,
            # 'modified_date': modified_date
        })

    cam_type = ['.nef','.cr2','.arw','.rw2']

    extlist = []
    filenamelist = []

    #如果有两个同名相机文件，则输出警告
    for file in file_list:
        filename = file['name']
        file_name, file_extension = os.path.splitext(filename)
        if file_extension.lower() in cam_type:
            extlist.append(file_extension)
            filenamelist.append(f'{filename} at {file["path"]}')

    if len(extlist) >= 2:
        print("警告：存在多个相机文件类型")
        logger.info(f"警告：存在多个相机文件类型: {filenamelist}")
    else:
        # 打印文件列表
        for file in file_list:
            filename = file['name']
            file_name, file_extension = os.path.splitext(filename)
            if file_extension == '.xmp':
                #找到同名文件
                for f in file_list:
                    filename2 = f['name']
                    file_name2, file_extension2 = os.path.splitext(filename2)
                    if file_name2 == file_name and file_extension2.lower() in ['.nef','.cr2','.arw','.rw2']:
                        filedir2 = f['path']
                        filedir = file['path']
                        if filedir == filedir2:
                            print(f'pass {filename}')
                            continue
                        filepath = os.path.join(filedir, filename)
                        #移动xmp文件
                        try:
                            shutil.move(filepath, filedir2)
                            print(f"移动文件: {filepath} 到 {filedir2}")
                        except Exception as e:
                            logger.info(f"移动文件: {filepath} 失败 {e}")
                        

def main():
    # serarch_and_move('_A7_0816')
    path = r"Z:\视频&照片\2018\2018-05-13"
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.xmp'):
                # filedir = os.path.join(root, file)
                filename = os.path.splitext(file)[0]
                serarch_and_move(filename)

if __name__ == '__main__':
    main()