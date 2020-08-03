import numpy as np
import math
from math import sin, asin, cos, radians, fabs, sqrt, pi, degrees

EARTH_RADIUS = 6371
RADIUS_1 = 200  # kilometers
RADIUS_2 = 200  # km
RADIUS_1_LNG = 116.1  # 经度
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


def next_point(lng, lat, arc_len, previous_angle, RADIUS, RADIUS_LNG, RADIUS_LAT):
    """
    给定当前点信息，返回下一点坐标
    """
    arc_radian = arc_len / RADIUS
#     angle, _, _ = get_angle_from_side(get_distance(lat,lng,RADIUS_LAT,
#                                                    RADIUS_LNG - degrees(RADIUS/(EARTH_RADIUS*cos(RADIUS_LAT)))),
#                                       RADIUS, RADIUS)# 与初始边夹角
#     angle =  previous_angle # 与初始边夹角
    side_l = side_len(RADIUS, RADIUS, arc_radian)
    lng_increase = degrees(cos((pi-arc_radian)/2 - previous_angle) * side_l / (2*pi*EARTH_RADIUS))
    lat_incerase = degrees(sin((pi-arc_radian)/2 - previous_angle) * side_l / (2*pi*EARTH_RADIUS*cos(RADIUS_LAT)))# 纬度增量
#     print(lng_increase,lat_incerase)
#     print(side_len(RADIUS, RADIUS, arc_radian))
    return lng+lng_increase, lat+lat_incerase, previous_angle+arc_radian


def get_angle_from_side(a, b, c):
    """
    输入三边返回三个角的弧度
    """
    A = radians(degrees(math.acos((a*a-b*b-c*c)/(-2*b*c))))
    B = radians(degrees(math.acos((b*b-a*a-c*c)/(-2*a*c))))
    C = radians(degrees(math.acos((c*c-a*a-b*b)/(-2*a*b))))
    return A, B, C


def side_len(side_a, side_b, angle_C):
    """
    已知两边及夹角求第三遍边
    """
    return sqrt(side_a**2 + side_b**2 - 2*side_a*side_b*cos(angle_C))



ang, _, _ = get_angle_from_side(get_distance(39.7,116.0,RADIUS_1_LAT,
                                            RADIUS_1_LNG - degrees(RADIUS_1/(EARTH_RADIUS*cos(RADIUS_1_LAT)))),
                                RADIUS_1, RADIUS_1)# 与初始边夹角
print(ang)
next_point(116.0,39.7,30,ang, RADIUS_1,RADIUS_1_LNG,RADIUS_1_LAT)