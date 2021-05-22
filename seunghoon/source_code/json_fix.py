import os
import json

# 경로 설정
dir_list = os.listdir("../dataset/Tomato_P04/out/")
base_dir = "../dataset/Tomato_P04/out/"

i = 1
while i < len(dir_list):
    file_name = base_dir + dir_list[i]

    with open(file_name, "r", encoding="utf-8") as f:
        json_data = f.read()

    json_data = json_data[1:-1].replace("'", '"').replace('"null"', 'null')
    print(json_data)

    with open(file_name, 'w', encoding="utf-8") as f:
        f.write(json_data)

    with open(file_name, "r", encoding="utf-8") as f:
        json_data = json.load(f)

    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent="\t")

    i += 2

'''
i = 1
file_name = base_dir + dir_list[i]

with open(file_name, "r", encoding="utf-8") as f:
    json_data = json.load(f)

json_data["imageData"] = "null"

print(json_data)
'''

'''
i = 0
while i < (len(dir_list)):
    # 개별 파일 이름
    file_name = base_dir + dir_list[i]

    with open(file_name, "r", encoding="utf-8") as f:
        print(i)
        json_data = json.load(f)

    # group_id 값 변경
    for j in range(len(json_data["shapes"])):
        json_data["shapes"][j]["group_id"] = 5

    # 변경 내용 저장
    with open(file_name, 'w', encoding="utf-8") as f:
        json.dump(json_data, f, indent="\t")

    i += 2
'''
'''
for i in range(len(dir_list)):
    # 개별 파일 이름
    file_name = base_dir + dir_list[i]

    with open(file_name, "r") as f:
        json_data = json.load(f)

    # group_id 값 변경
    for j in range(len(json_data["shapes"])):
        json_data["shapes"][j]["group_id"] = "null"

    # imagePath 값 변경
    json_data["imagePath"] = dir_list[0][:-4] + "jpeg"

    # imageData 값 변경
    json_data["imageData"] = "null"

    json.dumps(json_data)

    # 변경 내용 저장
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent="\t")
'''
