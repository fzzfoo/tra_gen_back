import numpy as np
import math
from math import sin, asin, cos, radians, fabs, sqrt, pi, degrees

EARTH_RADIUS = 6371
RADIUS_1 = 200  # kilometers
RADIUS_2 = 200  # km
RADIUS_1_LNG = 116.1  # 圆1经度
RADIUS_1_LAT = 39.7  # 经度
RADIUS_2_LNG = 116.1  # 经度
RADIUS_2_LAT = 40.1  # 经度
SPEED = 20  # km/min


def hav(theta):
    s = sin(theta / 2)
    return s * s


def get_distance(lat0, lng0, lat1, lng1):
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


def next_point_clw(arc_len, previous_angle, RADIUS, RADIUS_LNG, RADIUS_LAT):
    """
    用圆心坐标+弧度,给定当前点信息，返回下一点坐标
    顺时针
    """
    arc_radian = arc_len / RADIUS
    lng_increase = degrees(sin(previous_angle + arc_radian) * RADIUS / (EARTH_RADIUS * cos(RADIUS_LAT)))
    lat_incerase = degrees(cos(previous_angle + arc_radian) * RADIUS / (EARTH_RADIUS))  # 纬度增量

    # TODO(zf):噪声&漂移，高斯
    return RADIUS_LNG + lng_increase, RADIUS_LAT + lat_incerase, previous_angle + arc_radian


def next_point_anticlw(arc_len, previous_angle, RADIUS, RADIUS_LNG, RADIUS_LAT):
    """
    逆时针
    """
    arc_radian = arc_len / RADIUS
    lng_increase = degrees(sin(previous_angle + arc_radian) * RADIUS / (EARTH_RADIUS * cos(RADIUS_LAT)))
    lat_incerase = degrees(cos(previous_angle + arc_radian) * RADIUS / (EARTH_RADIUS))  # 纬度增量

    # TODO(zf):
    return RADIUS_LNG + lng_increase, RADIUS_LAT - lat_incerase, previous_angle + arc_radian


def in_out_point():
    """
    圆上起点，终点?
    """
    arr = np.random.rand(2)  # 0-1之间
    angle_in = pi * arr[0] + pi  # 圆上起点相对于初始边夹角
    angle_out =pi * arr[1] - 0.5 * pi

    return angle_in, angle_out


def generate_clw(pre_angle, arc,):
    """
    生成顺时针的一段轨迹
    """
    tra_0 = []
    while True:
        next_lng, next_lat, pre_angle = next_point_clw(arc, pre_angle,
                                                       RADIUS_1, RADIUS_1_LNG, RADIUS_1_LAT)
        if pre_angle < 2*pi:
            tra_0.append((next_lng, next_lat))
        else:
            break
    return tra_0, pre_angle-2*pi


def generate_clw_tail(pre_angle, arc, angle_out):
    """
    生成顺时针的离开轨迹
    """
    tra_3 = []
    while True:
        next_lng, next_lat, pre_angle = next_point_clw(arc, pre_angle,
                                                       RADIUS_1, RADIUS_1_LNG, RADIUS_1_LAT)
        if pre_angle < angle_out:
            tra_3.append((next_lng, next_lat))
        else:
            tra_3.append((next_lng, next_lat))
            break
    return tra_3


def generate_anticlw(pre_angle, arc,):
    tra_1 = []
    while True:
        next_lng, next_lat, pre_angle = next_point_clw(arc, pre_angle,
                                                       RADIUS_2, RADIUS_2_LNG, RADIUS_2_LAT)
        if pre_angle < 2*pi:
            tra_1.append((next_lng, next_lat))
        else:
            break
    return tra_1, pre_angle-2*pi


def generate(turns, arc, ):
    """
    生成一条轨迹
    """
    tra_list = []
    angle_in, angle_out = in_out_point()
    in_lng, in_lat, pre_angle = next_point_clw(angle_in * RADIUS_1, 0,
                                               RADIUS_1, RADIUS_1_LNG, RADIUS_1_LAT)
    tra_list.append((in_lng, in_lat))

    # TODO(zf)：arc_length
    for i in range(turns):
        tra_1, pre_angle = generate_clw(pre_angle, arc, )
        tra_list = tra_list + tra_1
        tra_2, pre_angle = generate_anticlw(pre_angle, arc, )
        tra_list = tra_list + tra_2

    tra_3 = generate_clw_tail(pre_angle, arc, angle_out)
    tra_list = tra_list + tra_3

    return tra_list

# TODO(zf): 进入离开，两段直线

