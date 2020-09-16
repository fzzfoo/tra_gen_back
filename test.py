# from divide_grid import get_boundary
# import math
# import random
# from gen_eight import generate_eightshaped_tra
# from gen_linear import generate_linear_tra
# from visual import imagefigure
# from gen_tra import generate_history_trajectory
import csv
from visual import imagefigure

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


# tra = []
# path = "data/2.csv"
# with open(path, encoding='UTF-8') as f:
#     reader = csv.reader(f)
#     for row in reader:
#         # print(row)
#         tra.append((float(row[0]), float(row[1])))

# print(tra)
# print(len(tra))
# imagefigure(tra=tra, tras=None, name='origin2', grid_cor=None)
# from tra_process import sample
# ss = sample(tra_list=[tra], sample_num=40, mode="average")
# imagefigure(tra=ss[0], tras=None, name='later', grid_cor=None)
#
# print(len(ss[0]))
# print(ss[0])

# f = open('aa.csv', 'w', encoding='utf-8')
# # 2. 基于文件对象构建 csv写入对象
# csv_writer = csv.writer(f)
# # 3. 构建列表头
# csv_writer.writerow(["姓名", "年龄", "性别"])
# # 4. 写入csv文件内容
# csv_writer.writerow(["l", '18', '男'])
# csv_writer.writerow(["c", '20', '男'])
# csv_writer.writerow(["w", '22', '女'])
# # 5. 关闭文件
# f.close()


def save2csv(tra, name="aaa"):
    f = open('{}.csv'.format(name), 'w', encoding='utf-8')
    csv_writer = csv.writer(f)
    # csv_writer.writerow(["姓名", "年龄", "性别"])
    for cor in tra:
        csv_writer.writerow([cor[0], cor[1]])
    f.close()
    print("{} Saved".format(name))
    return



