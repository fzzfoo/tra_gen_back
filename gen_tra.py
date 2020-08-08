import math
import random
from gen_eight import generate_eightshaped_tra
from gen_linear import generate_linear_tra
from visual import imagefigure


def generate_random_gps(base_log=None, base_lat=None, radius=None):
    radius_in_degrees = radius / 111300
    u = float(random.uniform(0.0, 1.0))
    v = float(random.uniform(0.0, 1.0))
    w = radius_in_degrees * math.sqrt(u)
    t = 2 * math.pi * v
    x = w * math.cos(t)
    y = w * math.sin(t)
    longitude = y + base_log
    latitude = x + base_lat
    return longitude, latitude


def generate_history_trajectory(arr, num):
    m = len(arr)
    res = []
    for i in range(num):
        temp = []
        for j in range(m):
            temp += [generate_random_gps(arr[j][0], arr[j][1], 5000)]
        res += [temp]
    return res


tra_e = generate_eightshaped_tra(1, 15)
tra_l_start = generate_linear_tra([113.7085, 36.3211], [tra_e[0][0], tra_e[0][1]],  15)   # [113.78698235542979, 40],
tra_l_end = generate_linear_tra([tra_e[-1][0], tra_e[-1][1]], [118.7443, 36.3764],   15)
print(tra_l_start[-1])
print(tra_e[0])
# imagefigure(tra_l)
imagefigure(tra_e)
# tra_l_r = tra_l[len(tra_l)-2::-1]  # 倒置
# imagefigure(tra_l_start[:-1] + tra_e + tra_l_end[1:])




