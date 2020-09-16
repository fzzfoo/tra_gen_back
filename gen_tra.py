import math
import random
from gen_eight import generate_eightshaped_tra
from gen_linear import generate_linear_tra
from visual import imagefigure
from tra_process import get_boundary, get_grid_num, save2txt, cut_tra, random_mask
import os
import sys
import numpy as np
import csv


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


def tra_conact(tra_day=6, circle_num=2, dist=10, tra_len=48, mode="gen", path="data/1.csv"):
    tra = []
    for i in range(tra_day):
        if mode == "gen":
            print("轨迹两点距离:{}".format(dist))
            tra_o = generate_eightshaped_tra(circle_num, dist)[:tra_len]
        elif mode == "load":
            tra_o = load_csv(path)
        tra += tra_o
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


def load_csv(path=None):
    tra = []
    # path = "data/1.csv"
    with open(path) as f:
        reader = csv.reader(f)
        for row in reader:
            # print(row)
            tra.append((float(row[0]), float(row[1])))
    print("载入轨迹{}, 共{}个点".format(path, len(tra)))
    return tra


def divide_data(tra, name, num):
    """
    划分训练测试验证，并保存
    :param tra:
    :param name:
    :param num:
    :return:
    """
    random.shuffle(tra)
    save2txt(tra[:num[0]], name=name[0])
    save2txt(tra[num[0]:num[0]+num[1]], name=name[1])
    save2txt(tra[num[0]+num[1]:], name=name[2])
    print("All saved")
    return


def generate(train_num=3000, test_num=600, validate_num=300, name='t_100_5'):
    num_list = [train_num, test_num, validate_num]
    name = mkdirs(name)
    sys.stdout = Logger('{}log.txt'.format(name))  # 日志信息
    print(name)
    print("train:{}  test:{}  validate:{}".format(train_num, test_num, validate_num))
    name_list = [name + "train", name + "test", name + "validate"]
    tra_single = tra_conact(tra_day=6, dist=10, circle_num=4, tra_len=100, mode="load", path="data/1.csv")
    # 生成一条数据 6*48=288  或者读取数据
    tra_s = generate_history_trajectory(tra_single, train_num+test_num+validate_num)  # 生成多条
    # tra_s = same_tra(tra_single, train_num+test_num+validate)  # 每条相同
    tra_grid, grid_cor = get_grid_num(tra_s, 5, name=name)  # 转成网格 km
    # imagefigure(tra=tra_single[:100], grid_cor=grid_cor, name=name)  # 显示yi条
    imagefigure(tra=None, tras=visual_data(tra_s[:5], start=0, end=100), grid_cor=grid_cor, name=name)
    tra_cut = cut_tra(tra_grid, length=100*6)  # 截断
    tra_mask = random_mask(tra_cut, tra_length=100, mask_num=10, mode='seg', segment=1)  # 后48 mask 10
    # tra_mask_ = random_mask(tra_cut[1950:], tra_length=48, mask_num=15)
    # tra_mask += tra_mask_
    divide_data(tra=tra_mask, name=name_list, num=num_list)
    get_vocab(tra_mask, name=name)
    print("t1 100 个点 连续mask10个")
    return


generate()

# TODO:
#  不同masknum： 不同的masknum能否运行？
#  不同稀疏程度 ： 调整两点距离，生成再拼接？  网格问题
#  连续缺失(混合？)：mode="seg"

