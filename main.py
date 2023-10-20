import cv2
import os
import os.path as osp
import argparse
import glob
import numpy as np
from tqdm import *
import multiprocessing
import threading

def load_color_dict(dir):
    color_dict=dict()
    with open(dir,'r') as f:
        for i, line in enumerate(f.readlines()):
            line = "".join(filter(lambda s:s in '0123456789 ', line))
            key_num = line.split(" ")
            key_value=list()
            for key in key_num:
                if key != "":
                    key_value.append(int(key))
            assert key_value[0] == i, "标签文件有误，请检查"
            color_dict[key_value[0]]=key_value[1:4]

    return color_dict

def trans(file, color_dict, cfg, pbar):
    gray_label = cv2.imread(file,0)
    hight, width = gray_label.shape
    color_label = np.zeros([hight, width, 3])
    for row in range(hight):
        for column in range(width):
            color_label[row, column, :] = color_dict[gray_label[row, column]]
    cv2.imwrite(osp.join(cfg['out_dir'], file.split('/')[-1]), color_label)
    pbar.update(1)

def trans_chunk(start, end, filelist, color_dict, cfg, pbar):
    for i in range(start, end + 1):
        file = filelist[i]
        trans(file, color_dict, cfg, pbar) 

def parallel_trans(num_processes, filelist, color_dict, cfg, pbar):
    # 计算每个进程要处理的数据量
    n = len(filelist)
    chunk_size = n // num_processes
    # 创建进程池
    
    # 计算结果
    for i in range(num_processes):
        start = i * chunk_size
        end = (i + 1) * chunk_size - 1
        if i == num_processes - 1:
            end = n - 1
        t = threading.Thread(target=trans_chunk, args=(start, end, filelist, color_dict, cfg, pbar))
        t.start()
 




def main(cfg):
    assert cfg['image_dir'] != None, "请指定图片目录"
    filelist = glob.glob("{}/*.*".format(cfg['image_dir']))
    color_dict = load_color_dict(cfg["label_color_file"])
    assert cfg['out_dir'] != None, "请指定输出目录"
    if not osp.exists(cfg['out_dir']):
        os.mkdir(cfg['out_dir'])
    print('开始转换！')
    pbar = tqdm(total = len(filelist))
    num_of_process=int(cfg["threads"])
    parallel_trans(num_of_process, filelist, color_dict, cfg, pbar)
    # for file in filelist:
    #     trans(file, color_dict, cfg, pbar)



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--image_dir', default =None)
    parser.add_argument('--out_dir', default = None)
    parser.add_argument('--label_color_file', default = 'label_color.txt')
    parser.add_argument('--threads', default = 4)
    args = parser.parse_args()
    cfgs = vars(args)
    main(cfgs)