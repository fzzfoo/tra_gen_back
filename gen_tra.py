import math
import random
from gen_eight import generate_eightshaped_tra
from gen_linear import generate_linear_tra
from visual import imagefigure
from divide_grid import get_boundary, get_grid_num, save2txt, cut_tra, random_mask
import os
import sys
import numpy as np


EARTH_RADIUS = 6371.0  # 地球半径 6371

class Logger(object):
    def __init__(self, filename="Default.log"):
        self.terminal = sys.stdout
        self.log = open(filename, "a")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        pass


def generate_random_gps(base_long=None, base_lat=None, radius=None):
    # radius_in_degrees = radius / 111300
    # u = float(random.uniform(0.0, 1.0))
    # v = float(random.uniform(0.0, 1.0))
    # w = radius_in_degrees * math.sqrt(u)
    # t = 2 * math.pi * v
    # x = w * math.cos(t)
    # y = w * math.sin(t)
    # longitude = y + base_log
    # latitude = x + base_lat

    r = np.random.randn(2)
    long_increase = math.degrees(radius / (EARTH_RADIUS * math.cos(math.radians(base_lat))))  # 经度增量
    lat_incerase = math.degrees(radius / EARTH_RADIUS)  # 纬度增量
    long_offset = long_increase * r[0]
    lat_offset = lat_incerase * r[1]
    return base_long + long_offset, base_lat + lat_offset


def generate_history_trajectory(arr, num):
    m = len(arr)
    res = []
    for i in range(num):
        temp = []
        for j in range(m):
            temp += [generate_random_gps(arr[j][0], arr[j][1], 2)]
        res += [temp]
    return res


def tra_conact(tra_day=6, circle_num=2, dist=10, tra_len=48,):
    tra = []
    print("轨迹两点距离:{}".format(dist))
    for i in range(tra_day):
        tra_o = generate_eightshaped_tra(circle_num, dist)[:tra_len]
        tra += tra_o
    # print(len(tra))
    return tra


def visual_data(tra_lists, start=0, end=48):
    ret_list = []
    for tra in tra_lists:
        tra_ = tra[start:end]
        ret_list.append(tra_)
    return ret_list


def same_tra(tra, num):
    tras = []
    for i in range(num):
        tras.append(tra)
    return tras


def get_vocab(tra_lists, name):
    """
    生成vocab.txt
    :param tra_lists:
    :param name:
    :return:
    """
    tra_p = []
    for tra in tra_lists:
        for i in tra:
            if i not in tra_p:
                tra_p.append(i)
    file_handle = open('{}vocab.txt'.format(name), mode='w')
    file_handle.writelines("<m>" + "\n")
    file_handle.writelines("<BOA>" + "\n")
    file_handle.writelines("<EOA>" + "\n")
    file_handle.writelines("*" + "\n")
    # <m> <BOA> <EOA> *
    for t in tra_p:
        if t != '<m>':
            file_handle.writelines(str(t) + "\n")
    file_handle.close()
    print("占用{}网格".format(len(tra_p) + 4))
    print("保存到 data/{}vocab.txt".format(name))

    return

# tra_e = generate_eightshaped_tra(2, 10)
# imagefigure(tra_e)
# print(len(tra_e))
# tra_l_start = generate_linear_tra([113.7085, 36.3211], [tra_e[0][0], tra_e[0][1]],  15)   # [113.78698235542979, 40],
# tra_l_end = generate_linear_tra([tra_e[-1][0], tra_e[-1][1]], [118.7443, 36.3764],   15)
# tra_l_r = tra_l[len(tra_l)-2::-1]  # 倒置
# imagefigure(tra_l_start[:-1] + tra_e + tra_l_end[1:])
# tra_es = generate_history_trajectory(tra_e, 9)
# imagefigure(tra_e, tra_es)
# min_long, min_lat, max_long, max_lat = get_boundary(tra_e)
# print("-------------------------")
# min_long, min_lat, max_long, max_lat = get_boundary(tra_es)
# print(tra_e)
# print(tra_es)


def mkdirs(name):
    if os.path.exists('data/{}'.format(name)):
        print("{}已存在，换&删！".format(name))
        sys.exit()
    try:
        os.mkdir('data/{}'.format(name))
    except Exception:
        print("创建失败")
        sys.exit()
    return 'data/{}/'.format(name)


def generate(train_num=3000, test_num=600, validate_num=300, name='1w'):
    num = [train_num, test_num, validate_num]
    name = mkdirs(name)
    sys.stdout = Logger('{}log.txt'.format(name))  # 日志信息
    print(name)
    print("train:{}  test:{}  validate:{}".format(train_num, test_num, validate_num))
    name_list = [name + "train", name + "test", name + "validate"]
    # for i in range(3):
    #     tra_single = tra_conact(tra_day=6, tra_len=48)  # 生成一条 6*48=288
    #     tra_s = generate_history_trajectory(tra_single, num[i])  # 生成条数
    #     # imagefigure(tra_single, tra_s[:5], name=name_list[i])  # 显示 5条
    #     imagefigure(tra_single, name=name_list[i])  # 显示 6day
    #     tra_grid = get_grid_num(tra_s, 1)  # 网格大小 km
    #     tra_cut = cut_tra(tra_grid)  # 截断
    #     tra_mask = random_mask(tra_cut, tra_length=48, mask_num=10)  # 后48 mask 10
    #     save2txt(tra_mask, name=name_list[i])
    #     tra_all += tra_mask
    tra_single = tra_conact(tra_day=6, dist=10, circle_num=4000, tra_len=98)  # 生成一条 6*48=288
    tra_s = generate_history_trajectory(tra_single, train_num+test_num+validate_num)  # 生成多条
    # tra_s = same_tra(tra_single, train_num+test_num+validate)  # 每条相同
    tra_grid, grid_cor = get_grid_num(tra_s, 5, name=name)  # 转成网格 km
    # imagefigure(tra_single[:48], grid_cor=grid_cor)  # 显示yi条
    imagefigure(tra=None, tras=visual_data(tra_s[:10], start=0, end=98), grid_cor=grid_cor, name=name)
    tra_cut = cut_tra(tra_grid, length=98*6)  # 截断
    tra_mask = random_mask(tra_cut, tra_length=98, mask_num=10)  # 后48 mask 10
    save2txt(tra_mask[:num[0]], name=name_list[0])
    save2txt(tra_mask[num[0]:num[0]+num[1]], name=name_list[1])
    save2txt(tra_mask[num[0]+num[1]:], name=name_list[2])
    get_vocab(tra_mask, name=name)
    print("1w个点 测试 内存 显存")
    return


generate()



