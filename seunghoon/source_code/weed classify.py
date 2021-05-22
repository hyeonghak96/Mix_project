import os
import shutil

# 경로 설정
dir_list = os.listdir("../dataset/Tomato_D05_229/")
base_dir = "../dataset/Tomato_D05_229/"
move_dir = "../dataset/Tomato_D05_229_json/"

i = 0
while i < len(dir_list):
    file_name = base_dir + dir_list[i]
    shutil.move(file_name, move_dir)
    i += 2

