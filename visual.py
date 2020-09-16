import folium
import random
from folium import plugins
from math import sin, asin, cos, radians, fabs, sqrt, pi, degrees, atan
import math


def imagefigure(tra=None, tras=None, name='other', grid_cor=None):
    # tras多条   tra 一条
    """
    格式
    多条：[[(long,lat),(long,lat),(long,lat).......], [...], [...], ......]
    一条：[(long,lat),(long,lat),(long,lat).......]
    :param tra:
    :param tras:
    :param name:
    :param grid_cor:
    :return:
    """
    if tra is not None:
        my_map = folium.Map(location=[tra[0][1], tra[-1][0]], zoom_start=9, control_scale=True)
    elif tras is not None:
        my_map = folium.Map(location=[tras[0][0][1], tras[0][-1][0]], zoom_start=9, control_scale=True)

    if tra is not None:
        for i in range(len(tra)):
            tra[i] = tra[i][::-1]
        folium.PolyLine(tra, color='#4CF0E8', weight=1, opacity=1).add_to(my_map)
        marker_cluster = plugins.MarkerCluster().add_to(my_map)
        for i in range(len(tra)):
            temp = 0
            if i != 0:
                temp = geoDegree(tra[i - 1][0], tra[i - 1][1], tra[i][0], tra[i][1])
            folium.Marker([tra[i][0], tra[i][1]], tooltip=str(i), popup=str(temp),
                          icon=folium.Icon(color="red", icon="fa-fighter-jet", prefix="fa",
                                           angle=(temp + (3 / 2 * pi)) % (2 * pi))).add_to(marker_cluster)

    if tras is not None:
        for j in range(len(tras)):
            # 多条的
            for i in range(len(tras[j])):
                tras[j][i] = tras[j][i][::-1]
            folium.PolyLine(tras[j], color='#AD18C' + str(j), weight=1, opacity=1).add_to(my_map)
            marker_cluster = plugins.MarkerCluster().add_to(my_map)
            for i in range(len(tras[j])):
                tem = 0
                if i != 0:
                    tem = geoDegree(tras[j][i - 1][0], tras[j][i - 1][1], tras[j][i][0], tras[j][i][1])
                folium.Marker([tras[j][i][0], tras[j][i][1]], tooltip=str(i), popup=str(tem),
                              icon=folium.Icon(icon="fa-fighter-jet", prefix="fa",
                                               angle=(tem + (3 / 2 * pi)) % (2 * pi))).add_to(marker_cluster)

    my_map.add_child(folium.LatLngPopup())
    if grid_cor is not None:
        gj = folium.GeoJson(data={"type": "MultiLineString","coordinates": grid_cor})
        my_map.add_child(gj)
    my_map.save(name + 'map.html')


def geoDegree(lng1, lat1, lng2, lat2):
    """
    公式计算两点间方位角
    方位角：是与正北方向、顺时针之间的夹角
    """
    lng1, lat1, lng2, lat2 = map(radians, [float(lng1), float(lat1), float(lng2), float(lat2)])
    dlon = lng2 - lng1
    y = sin(dlon) * cos(lat2)
    x = cos(lat1) * sin(lat2) - sin(lat1) * cos(lat2) * cos(dlon)
    brng = degrees(math.atan2(y, x))
    brng = (brng + 360) % 360
    return brng / 180 * pi
