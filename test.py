# from divide_grid import get_boundary
# import math
# import random
# from gen_eight import generate_eightshaped_tra
# from gen_linear import generate_linear_tra
# from visual import imagefigure
# from gen_tra import generate_history_trajectory

# train_dataset_path = "data/train.txt"
# with open(train_dataset_path) as f:
#     for line in f:
#         temp = line.strip().split('\t')
#         # trainuser.append(int(temp[0]))
#         # traintime.append(day_dic[temp[1]])
#         # traintime.append(1)  # 都是1?????????????????
#         # trainday.append(int(temp[1]))
#         traj = temp[2].split(' ')  # 长度不固定
#         # traindata.append(traj)
#         print(len(traj))

# os.mkdir("aaa")
# print(os.path.exists('aaa') )


# class Logger(object):
#     def __init__(self, filename="Default.log"):
#         self.terminal = sys.stdout
#         self.log = open(filename, "a")
#
#     def write(self, message):
#         self.terminal.write(message)
#         self.log.write(message)
#
#     def flush(self):
#         pass
#
#
# path = os.path.abspath(os.path.dirname(__file__))
# type = sys.getfilesystemencoding()
# sys.stdout = Logger('a.txt')
#
# print(path)
# print(os.path.dirname(__file__))
# print('------------------')
# generate()

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


def concat_txt(name="concat"):
    """
    拼接两个txt
    :param name:
    :return:
    """
    name_1 = "data/8_10_5_5000/train.txt"
    name_2 = "data/8_10_5t/train.txt"
    # user = 0
    # day = 20200901  # [str(int(20200901 + i)) for i in range(len(tra_grid))]
    file_handle = open('data/concat/{}.txt'.format(name), mode='w')  # a 追加
    with open(name_1) as f:
        for line in f:
            temp = line.strip().split('\t')
            tra_str = str(temp[0]) + "\t" + str(temp[1]) + "\t" + temp[2] + "\n"
            file_handle.writelines(tra_str)
    with open(name_2) as f:
        for line in f:
            temp = line.strip().split('\t')
            tra_str = str(temp[0]) + "\t" + str(temp[1]) + "\t" + temp[2] + "\n"
            file_handle.writelines(tra_str)
    file_handle.close()
    print("保存到 data/concat/{}.txt".format(name))





