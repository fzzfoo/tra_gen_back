import numpy as np
from math import sin, asin, cos, radians, fabs, sqrt, pi, degrees
from gen_eight import get_distance

# 给一组数据 确定左上右下边界 划分网格
EARTH_RADIUS = 6371.0


def get_boundary(tra_lists):
    """
    返回矩形经纬度边界  [(long,lat), .....]
    :param tra_lists:  轨迹list
    :return: max_lat, max_long, min_lat,  min_long  +- 0.02 覆盖点
    """
    max_lat, max_long, min_lat, min_long = 0, 0, 400, 400
    try:  # 多条轨迹
        for tra_l in tra_lists:
            for ll in tra_l:
                long = ll[0]
                lat = ll[1]
                max_lat = max(max_lat, lat)
                max_long = max(max_long, long)
                min_lat = min(min_lat, lat)
                min_long = min(min_long, long)
                # print(long, lat)
                # print("min_long{}, min_lat{}, max_long{}, max_lat{}".format(min_long, min_lat, max_long, max_lat))
    except Exception:  # 单条
        print("单条轨迹 & Exception")
        for ll in tra_lists:
            long = ll[0]
            lat = ll[1]
            max_lat = max(max_lat, lat)
            max_long = max(max_long, long)
            min_lat = min(min_lat, lat)
            min_long = min(min_long, long)
            # print(long, lat)
            # print("min_long{}, min_lat{}, max_long{}, max_lat{}".format(min_long, min_lat, max_long, max_lat))

    return min_long - 0.02, min_lat - 0.02, max_long + 0.02, max_lat + 0.02


def dist2long_lat(dist, RADIUS_LAT=39.7):
    """
    弧长/半径 再化为角度
    :param dist:  距离 km
    :param RADIUS_LAT:  当前纬度 考虑经纬度差异
    :return:
    """
    # TODO: Right?
    long_increase = degrees(dist / (EARTH_RADIUS * cos(radians(RADIUS_LAT))))  # 经度增量
    lat_incerase = degrees(dist / EARTH_RADIUS)  # 纬度增量
    print("网格长{}km 转换成经纬度增量___经度：{} 纬度：{}".format(dist, long_increase, lat_incerase))

    return long_increase, lat_incerase


def get_grid_num(tra_lists, dist, name='None'):
    """
    :param name:
    :param tra_lists: 多条轨迹列表
    :param dist: 网格长度
    :return:
    """
    origin_long, origin_lat, end_long, end_lat = get_boundary(tra_lists)  # 起终点经纬度
    long_increase, lat_incerase = dist2long_lat(dist)
    row_num = int((end_long - origin_long) / long_increase) + 1  # 计算每行网格数
    col_num = int((end_lat - origin_lat) / lat_incerase) + 1
    print("总网格数:{}*{}行={}".format(row_num, col_num, row_num * col_num))
    # tra_lists = cut_tra(tra_lists)
    grid_cor = get_grid_boundary(origin_long, origin_lat, long_increase, lat_incerase, row_num, col_num)
    grid_core_cor = get_grid_cor(origin_long, origin_lat, long_increase, lat_incerase, row_num, col_num)
    grid_distance(grid_core_cor, col_num*row_num, name)
    tra_list_grid = []
    for tra in tra_lists:
        tra_grid = []
        for i in tra:
            long = i[0]
            lat = i[1]
            num = int((long - origin_long) / long_increase) + \
                  int((lat - origin_lat) / lat_incerase) * row_num + 1
            tra_grid.append(num)
        tra_list_grid.append(tra_grid)

    return tra_list_grid, grid_cor


def get_grid_boundary(origin_long, origin_lat, long_increase, lat_incerase, row_num, col_num):
    """
    计算网格边界，线
    :param origin_long:
    :param origin_lat:
    :param long_increase:
    :param lat_incerase:
    :param row_num:
    :param col_num:
    :return:
    """
    cor = []
    for col in range(col_num):
        col_ = []
        ori = []
        end = []
        # orig_long, orig_lat = origin_long, origin_lat + col*lat_incerase
        # end_long, end_lat = origin_long + long_increase*row_num, origin_lat + col*lat_incerase
        ori.append(origin_long)
        ori.append(origin_lat + col*lat_incerase)
        end.append(origin_long + row_num*long_increase)  # row_num 每行网格数
        end.append(origin_lat + col*lat_incerase)
        col_.append(ori)
        col_.append(end)
        cor.append(col_)

    for row in range(row_num):
        col_ = []
        ori = []
        end = []
        ori.append(origin_long + row*long_increase)
        ori.append(origin_lat)
        end.append(origin_long + row*long_increase)
        end.append(origin_lat + col_num*lat_incerase)
        col_.append(ori)
        col_.append(end)
        cor.append(col_)

    return cor


def get_grid_cor(origin_long, origin_lat, long_increase, lat_incerase, row_num, col_num):
    """
    计算每个网格中心坐标，[[(long,lat),....], [], .......]
    :param origin_long:
    :param origin_lat:
    :param long_increase:
    :param lat_incerase:
    :param row_num:
    :param col_num:
    :return:
    """
    origin_core_long = origin_long + long_increase/2
    origin_core_lat = origin_lat + lat_incerase/2
    grid_cor = []
    for c in range(col_num):  # 行数
        for r in range(row_num):
            core_long = origin_core_long + r*long_increase
            core_lat = origin_core_lat + c*lat_incerase
            grid_cor.append((core_long, core_lat))
    return grid_cor


def grid_distance(cor_lists, num, name,):
    """
    生成距离矩阵
    :param cor_lists:
    :param num:  矩阵纬度
    :param name:
    :return:
    """
    dist_matirx = np.zeros((num, num), dtype=float)
    for i in range(len(cor_lists)):
        for j in range(len(cor_lists)):
            dist = get_distance(cor_lists[i][1], cor_lists[i][0], cor_lists[j][1], cor_lists[j][0])
            dist_matirx[i][j] = dist
    np.save("{}dist_matrix.npy".format(name), dist_matirx)
    print("保存到 {}dist_matrix.npy ".format(name))
    return


def cut_tra(tra_lists, length=288):
    """
    截断轨迹到length长 288
    :param tra_lists:
    :param length:
    :return:
    """
    tra_list_cut = []
    print("轨迹长{}".format(len(tra_lists[0])))
    for tra in range(len(tra_lists)):
        # print("第{}条轨迹长{}".format(tra, len(tra_lists[tra])))
        if len(tra_lists[tra]) < length:
            print("轨迹{}长度小于{}".format(tra, length))
            return
        tra_list_cut.append(tra_lists[tra][:length])
    return tra_list_cut


def save2txt(tra_grid, name='train'):
    """
    写入成txt
    :param name:
    :param tra_grid:
    :return:
    """
    user = 0
    day = [str(int(20200901+i)) for i in range(len(tra_grid))]
    file_handle = open('{}.txt'.format(name), mode='w')
    for tra_ in range(len(tra_grid)):
        tra = ""
        for i in tra_grid[tra_]:
            tra = tra + str(i) + " "
        tra_str = str(user) + "\t" + str(day[tra_]) + "\t" + tra + "\n"
        file_handle.writelines(tra_str)
    file_handle.close()
    print("保存到 {}.txt".format(name))
    return


def random_mask(tra_lists, tra_length=48, mask_num=10):
    """
    mask 一部分
    :param tra_lists: 多个用户？
    :param tra_length:
    :param mask_num:
    :return:
    """
    for tra in range(len(tra_lists)):
        a = np.random.randint(low=0, high=tra_length, size=mask_num * 2)
        mask_list = []
        for i in a:
            if i not in mask_list:
                mask_list.append(i)
        for i in range(mask_num):
            tra_lists[tra][mask_list[i] + len(tra_lists[tra]) - tra_length] = "<m>"
    return tra_lists


