import argparse


################################################################################################
#                                 8字型轨迹参数
################################################################################################
def args_of_eight():
    parser = argparse.ArgumentParser(description="Parameter of eight-shaped trajectory")

    parser.add_argument('--EARTH_RADIUS', type=float, default=6371.0, help='地球半径，km')

    parser.add_argument('--RADIUS_1_LNG', type=float, default=116.1, help='圆1经度')
    parser.add_argument('--RADIUS_1_LAT', type=float, default=39.7, help='圆1纬度')
    parser.add_argument('--RADIUS_2_LNG', type=float, default=116.1, help='圆2经度')
    parser.add_argument('--RADIUS_2_LAT', type=float, default=39.7 + 3.5972864236749222, help='圆2纬度')

    parser.add_argument('--RADIUS_1', type=float, default=200.0, help='圆1半径，km')
    # 给定两圆坐标及一圆半径，可得另一半径
    parser.add_argument('--RANDOM_ERR', type=float, default=0.01, help='经纬度误差，非完整圆')

    parser.add_argument('--circle_num', type=int, default=2, help='8字转几圈')
    parser.add_argument('--day_num', type=int, default=6, help='day_num条轨迹拼接成一条数据')
    parser.add_argument('--dist', type=float, default=10, help='轨迹上两点之间距离 km')
    parser.add_argument('--seq_length', type=int, default=48, help='每条轨迹几个点')
    parser.add_argument('--grid_length', type=int, default=5, help='网格大小，km')
    parser.add_argument('--mask_num', type=int, default=10, help='mask点个数')

    args_es = parser.parse_args()  # es = eight shaped
    # print(args_es)

    return args_es


################################################################################################
#                                 8字型轨迹参数
################################################################################################
def args_of_linear():
    parser = argparse.ArgumentParser(description="Parameter of eight-shaped trajectory")

    parser.add_argument('--EARTH_RADIUS', type=float, default=6371.0, help='地球半径，km')
    parser.add_argument('--RANDOM_ERR', type=float, default=0.3, help='经纬度误差，非完整圆')

    args_l = parser.parse_args()  # es = eight shaped
    # print(args_l)

    return args_l


################################################################################################
#                                 8字型轨迹参数
################################################################################################
def args_of_():
    parser = argparse.ArgumentParser(description="Parameter of eight-shaped trajectory")

    parser.add_argument('--EARTH_RADIUS', type=float, default=6371.0, help='地球半径，km')
    parser.add_argument('--RANDOM_ERR', type=float, default=0.3, help='经纬度误差，非完整圆')

    args_l = parser.parse_args()  # es = eight shaped
    # print(args_l)

    return args_l


if __name__ == '__main__':
    args_of_eight()
