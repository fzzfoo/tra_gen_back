import numpy as np
import math
from math import sin, asin, cos, radians, fabs, sqrt, pi, degrees,atan
import numpy as np
import os
import folium
import random
from folium import plugins


EARTH_RADIUS = 6371
RANDOM_ERR = 0.01
# RADIUS_1 = 200  # kilometers
# RADIUS_2 = 200  # km
# RADIUS_1_LNG = 116.1  # 圆1经度
# RADIUS_1_LAT = 39.7  # 纬度
# RADIUS_2_LNG = 116.1  # 经度
# RADIUS_2_LAT = 39.7 + 3.5972864236749222  # 纬度

# SPEED = 20  # km/min


def hav(theta):
    s = sin(theta / 2)
    return s * s


def get_distance(lng0, lat0, lng1, lat1):
    """
    用haversine公式计算球面两点间的距离 km
    """
    # 经纬度转换成弧度
    lat0 = radians(lat0)
    lat1 = radians(lat1)
    lng0 = radians(lng0)
    lng1 = radians(lng1)

    dlng = fabs(lng0 - lng1)
    dlat = fabs(lat0 - lat1)

    h = hav(dlat) + cos(lat0) * cos(lat1) * hav(dlng)
    distance = 2 * EARTH_RADIUS * asin(sqrt(h))
    return distance  # km


def random_err():
    """
    :return: 坐标噪声系数
    """
    e = np.random.rand(2) * 2 - 1
    return e[0]*RANDOM_ERR, e[1]*RANDOM_ERR


def get_new_lat(lng, lat, dist, flag2):
    e_lat = random_err()[0]
    lat_increase = flag2 * degrees(dist / EARTH_RADIUS)
    new_lat = lat + lat_increase * (1 + e_lat)
    return new_lat


def get_new_lng(lng, lat, dist, flag1):
    e_lng = random_err()[1]
    lng_increase = flag1 * degrees(dist / (EARTH_RADIUS * cos(radians(lat))))
    new_lng = lng + lng_increase * (1 + e_lng)
    return new_lng


def generate_linear_tra(loc1, loc2, n):
    """
    给定起点终点，距离
    :param loc1: 起点
    :param loc2:
    :param n:
    :return: 轨迹坐标
    """
    len1 = get_distance(loc1[0], loc1[1], loc2[0], loc1[1])
    len2 = get_distance(loc2[0], loc1[1], loc2[0], loc2[1])
    l = get_distance(loc1[0], loc1[1], loc2[0], loc2[1])
    m = l // n
    flag1, flag2 = 1, 1
    if loc2[0] < loc1[0]:
        flag1 = -1
    if loc2[1] < loc1[1]:
        flag2 = -1

    step1, step2 = len1 / m, len2 / m
    arr = []
    arr += [loc1]
    for i in range(int(m)):
        arr += [[get_new_lng(arr[-1][0], arr[-1][1], step1, flag1),
                 get_new_lat(arr[-1][0], arr[-1][1], step2, flag2)]]
    # arr += [loc2]
    return arr

# traject = generate(2, 15)
# np.savetxt("data.txt", traject)
# his_tra=generate_history_trajectory(traject, 9)
# imagefigure(his_tra, traject)

# res = generate_linear_tra([120.157884, 30.097175], [118.610000, 28.148523], 15)
