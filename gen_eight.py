from math import sin, asin, cos, radians, fabs, sqrt, pi, degrees
import numpy as np
from args import args_of_eight
from visual import imagefigure, geoDegree



args = args_of_eight()
EARTH_RADIUS = args.EARTH_RADIUS  # 地球半径 6371

RADIUS_1_LNG = 116.0  # 圆1经度
RADIUS_1_LAT = 39.5  # 经度
RADIUS_2_LNG = 116.3  # 120.1
RADIUS_2_LAT = 39.8  # 39.7 + 3.5972864236749222
RADIUS_1 = 20.0  # 圆1半径
#
RANDOM_ERR = 0.01
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


RADIUS_2 = get_distance(RADIUS_2_LAT, RADIUS_2_LNG, RADIUS_1_LAT, RADIUS_1_LNG) - RADIUS_1
# print("两圆心距离:{}km".format(get_distance(RADIUS_1_LAT, RADIUS_1_LNG, RADIUS_2_LAT, RADIUS_2_LNG)))
# print("圆1半径:{}km, 圆2半径:{}km".format(RADIUS_1, RADIUS_2))
ANG = geoDegree(RADIUS_1_LNG, RADIUS_1_LAT, RADIUS_2_LNG, RADIUS_2_LAT)  # pi / 4


def next_point_clw(arc_len, previous_angle, RADIUS, RADIUS_LNG, RADIUS_LAT):
    """
    给定前一点，顺时针方向返回下一点坐标 clw=clockwise
    https://www.jianshu.com/p/ba69d991f1af
    :param arc_len: 相比前一点经过的弧长
    :param previous_angle: 前一点的圆心角
    :param RADIUS: 圆半径
    :param RADIUS_LNG: 圆坐标
    :param RADIUS_LAT:
    :return: 下一点坐标，圆心角
    """
    arc_radian = arc_len / RADIUS  # 弧度
    lng_increase = degrees(sin(previous_angle - arc_radian) * RADIUS / (EARTH_RADIUS * cos(radians(RADIUS_LAT))))
    # print(EARTH_RADIUS * cos(radians(RADIUS_LAT)))
    lat_incerase = degrees(cos(previous_angle - arc_radian) * RADIUS / (EARTH_RADIUS))  # 纬度增量
    e_lng, e_lat = random_err()  # 添加两个维度的噪声
    lng_increase = (1 + e_lng) * lng_increase
    lat_incerase = (1 + e_lng) * lat_incerase
    return RADIUS_LNG - lng_increase, RADIUS_LAT + lat_incerase, previous_angle - arc_radian


def next_point_anticlw(arc_len, previous_angle, RADIUS, RADIUS_LNG, RADIUS_LAT):
    """
    anticlw = anti-clockwise
    """
    arc_radian = arc_len / RADIUS
    lng_increase = degrees(sin(previous_angle + arc_radian) * RADIUS / (EARTH_RADIUS * cos(radians(RADIUS_LAT))))
    lat_incerase = degrees(cos(previous_angle + arc_radian) * RADIUS / (EARTH_RADIUS))  # 纬度增量

    e_lng, e_lat = random_err()  # 添加两个维度的噪声
    lng_increase = (1 + e_lng) * lng_increase
    lat_incerase = (1 + e_lng) * lat_incerase
    return RADIUS_LNG + lng_increase, RADIUS_LAT - lat_incerase, previous_angle + arc_radian


def in_out_point():
    """

    :return: 起点终点圆心角
    """
    arr = np.random.rand(2)  # 0-1之间
    angle_in = pi * arr[0]   # 圆上起点相对于初始边夹角
    angle_out = pi * arr[1] + pi

    return 0.5 * pi, 1.5 * pi


def generate_clw(pre_angle, arc, ):
    """
    生成圈上的一段轨迹_顺时针
    :param pre_angle: 前一点圆心角
    :param arc: 弧长
    :return:
    """

    tra_0 = []
    while True:
        next_lng, next_lat, pre_angle = next_point_clw(arc, pre_angle,
                                                       RADIUS_1, RADIUS_1_LNG, RADIUS_1_LAT)
        if pre_angle > 0 - ANG:
            tra_0.append((next_lng, next_lat))
        else:
            break
    pre_angle = 0 - ANG - (arc - (0 - ANG - pre_angle) * RADIUS_1) / RADIUS_2
    return tra_0, pre_angle  # (0 - ANG - pre_angle) * RADIUS_1 / RADIUS_2


def generate_clw_tail(pre_angle, arc, angle_out, ):
    """
    结束条件判断
    :param pre_angle:
    :param arc:
    :param angle_out: 终点圆心角
    :return:
    """
    tra_3 = []
    while True:
        next_lng, next_lat, pre_angle = next_point_clw(arc, pre_angle,
                                                       RADIUS_1, RADIUS_1_LNG, RADIUS_1_LAT)
        if pre_angle > angle_out - ANG:
            tra_3.append((next_lng, next_lat))
        else:
            tra_3.append((next_lng, next_lat))
            break
    return tra_3


def generate_anticlw(pre_angle, arc,):
    """
    逆时针
    """
    tra_1 = []
    while True:
        next_lng, next_lat, pre_angle = next_point_anticlw(arc, pre_angle,
                                                           RADIUS_2, RADIUS_2_LNG, RADIUS_2_LAT)
        if pre_angle < 2 * pi - ANG:
            tra_1.append((next_lng, next_lat))
        else:
            break
    pre_angle = (arc - (pre_angle - 2*pi + ANG) * RADIUS_2) / RADIUS_1 + 2*pi - ANG
    return tra_1, pre_angle  # (2 * pi - ANG - pre_angle) * RADIUS_2 / RADIUS_1 + 2*pi


def random_err():
    """
    :return: 坐标噪声系数
    """
    e = np.random.rand(2) * 2 - 1
    return e[0]*RANDOM_ERR, e[1]*RANDOM_ERR


def generate_eightshaped_tra(turns, arc, ):
    """
    生成一条轨迹
    :param turns: 绕八字圈数，
    :param arc: 两点之间的弧长
    :return: 列表 tra_list = [(lng,lat),....]
    """
    # TODO(zf)：arc 匀速否？
    print("两圆心距离:{}km".format(get_distance(RADIUS_1_LAT, RADIUS_1_LNG, RADIUS_2_LAT, RADIUS_2_LNG)))
    print("圆1半径:{}km, 圆2半径:{}km".format(RADIUS_1, RADIUS_2))
    tra_list = []
    angle_in, angle_out = in_out_point()
    next_lng, next_lat, pre_angle = next_point_clw(0, angle_in - ANG,
                                                   RADIUS_1, RADIUS_1_LNG, RADIUS_1_LAT)  # 起点坐标

    tra_list.append((next_lng, next_lat))

    for i in range(turns):
        tra_1, pre_angle = generate_clw(pre_angle, arc,)
        tra_list = tra_list + tra_1
        # pre_angle = pre_angle - ANG  # 放函数里
        tra_2, pre_angle = generate_anticlw(pre_angle, arc,)
        tra_list = tra_list + tra_2
        # pre_angle = pre_angle - ANG

    tra_3 = generate_clw_tail(pre_angle, arc, angle_out,)
    tra_list = tra_list + tra_3

    # print("生成轨迹 1 条")
    # print(len(tra_1))
    # print(len(tra_2))
    # print(len(tra_3))
    # print(tra_1[-1])
    # print(tra_2[-1])
    # print(tra_3[:2])

    return tra_list  # tra_1 + tra_2


# def imagefigure():
#     traject = np.loadtxt("data.txt")
#     for i in range(len(traject)):
#         traject[i] = traject[i][::-1]
#     my_map = folium.Map(location=[traject[0][0], traject[-1][1]], zoom_start=7, control_scale=True)
#     folium.PolyLine(traject, color='blue', weight=1, opacity=1).add_to(my_map)
#     marker_cluster = plugins.MarkerCluster().add_to(my_map)
#     for i in range(len(traject)):
#         folium.Marker([traject[i][0], traject[i][1]]).add_to(marker_cluster)
#     my_map.add_child(folium.LatLngPopup())
#     my_map.save('my_map.html')

# traject = generate_eightshaped_tra(2, 15)
# for i in range(len(traject)):
#     print(traject[i])
# np.savetxt("data.txt", traject)
# imagefigure()

# print(get_distance(39.6924, 113.7084, 39.7, 113.7806))

# tra_e = generate_eightshaped_tra(2, 15)
# imagefigure(tra_e)
# tra_o = generate_eightshaped_tra(2, 10)
# print(len(tra_o))



