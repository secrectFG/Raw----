import os
import concurrent.futures
from psd_tools import PSDImage
from PIL import Image

def process_psd(psd_folder, tiff_folder, filename):
    # if filename.lower().endswith('.psd'):
    print(f"Processing {filename}...")
    psd_path = os.path.join(psd_folder, filename)
    tiff_path = os.path.join(tiff_folder, os.path.splitext(filename)[0] + '.tif')
    
    # 打开PSD文件
    psd = PSDImage.open(psd_path)
    
    # 创建一个列表来存储所有图层
    layers = []
    
    # 递归函数来处理所有图层，包括组内的图层
    def process_layers(layer_container):
        for layer in layer_container:
            if layer.is_group():
                process_layers(layer)
            else:
                # 将图层转换为PIL Image对象
                layer_image = layer.composite()
                if layer_image.mode != 'RGBA':
                    print(f"Layer {layer.name} is not in RGBA mode, converting...")
                    layer_image = layer_image.convert('RGBA')
                layers.append(layer_image)
    
    # 处理所有图层
    process_layers(psd)
    
    # 如果没有图层，至少保存合成图像
    if not layers:
        layers.append(psd.composite())
    
    # 保存为多页TIFF
    layers[0].save(tiff_path, format='TIFF', compression='tiff_deflate', save_all=True, append_images=layers[1:])
    
    return f"处理完成: {filename}"

def convert_psd_to_tiff(psd_folder, tiff_folder, max_workers=3):
    # 确保目标文件夹存在
    if not os.path.exists(tiff_folder):
        os.makedirs(tiff_folder)

    # 获取所有PSD文件
    psd_files = [f for f in os.listdir(psd_folder) if f.lower().endswith('.psd')]

    # 使用ThreadPoolExecutor并行处理文件
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_file = {executor.submit(process_psd, psd_folder, tiff_folder, filename): filename for filename in psd_files}
        for future in concurrent.futures.as_completed(future_to_file):
            filename = future_to_file[future]
            try:
                result = future.result()
                print(result)
            except Exception as exc:
                print(f'{filename} 生成了一个异常: {exc}')

    print("所有文件处理完成!")

def main():
    # 源PSD文件夹路径
    psd_folder = r'F:\temp psd'

    # 目标TIFF文件夹路径
    tiff_folder = r"I:\tif-temp"

    # 设置同时处理的文件数
    max_workers = 1

    convert_psd_to_tiff(psd_folder, tiff_folder, max_workers)

if __name__ == "__main__":
    main()
