import numpy as np
import os
import shutil

dir_list = os.listdir("../dataset/Tomato_D05")

rand_int = np.random.choice(len(dir_list), 229, replace=False)

for i in rand_int:
    shutil.move("../dataset/Tomato_D05/" + dir_list[i], "../dataset/Tomato_D05_299/")
