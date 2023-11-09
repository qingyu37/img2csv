from PIL import Image
import numpy as np
import os
import concurrent.futures

# 将 input_folder 文件夹下的所有图片转换为 csv 文件，存放在 output_folder 文件夹下
# 存储格式类似于 test.csv

input_folder = './dataset/ch4_training_images'
output_folder = './dataset/ch4_training_csv'

os.makedirs(output_folder, exist_ok=True)

image_files = [f for f in os.listdir(input_folder) if f.endswith('.jpg') or f.endswith('.png') or f.endswith('.jpeg')]


def img2csv(image_file):
    # print('Processing: ' + image_file)
    img = Image.open(os.path.join(input_folder, image_file))
    arr = np.asarray(img)
    ans = []
    for row in arr:
        flat_arr = row.reshape(-1, 3)
        tmp = []
        for col in flat_arr:
            for i in col:
                tmp.append(str(i))
        ans.append(tmp)
    csv_file = os.path.splitext(image_file)[0] + '.csv'
    with open(os.path.join(output_folder, csv_file), 'w') as f:
        for row in ans:
            f.write(','.join(row) + '\n')


# 使用线程池
with concurrent.futures.ThreadPoolExecutor(max_workers = os.cpu_count() / 2) as executor:
    futures = [executor.submit(img2csv, image_file) for image_file in image_files]
    concurrent.futures.as_completed(futures)
