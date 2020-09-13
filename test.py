# from divide_grid import get_boundary
# import math
# import random
# from gen_eight import generate_eightshaped_tra
# from gen_linear import generate_linear_tra
# from visual import imagefigure
# from gen_tra import generate_history_trajectory
import os

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
import sys
import os
from gen_tra import generate


class Logger(object):
    def __init__(self, filename="Default.log"):
        self.terminal = sys.stdout
        self.log = open(filename, "a")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        pass


path = os.path.abspath(os.path.dirname(__file__))
type = sys.getfilesystemencoding()
sys.stdout = Logger('a.txt')

print(path)
print(os.path.dirname(__file__))
print('------------------')
generate()



