import cv2
import numpy as np
import re
import json
import copy
import os


def path_decom(file_path):
    """
    "path/[a-zA-Z0-9_-]+.*" 형식의
    파일 경로를 파일명, 파일 확장자, 디렉토리 경로로 분리함

    Args:
        file_path: 파일 경로, str 객체

    Returns:
        (파일명, 파일 확장자, 디렉토리 경로) 형식의 튜플 반환
        이때 튜플의 각 성분은 str 객체이다.
    """
    filename_re = re.compile(r'(?<=/)((?!/).)*(?=\..+$)')
    filename_match = filename_re.search(file_path)
    filename_index = filename_match.span()

    filename = file_path[filename_index[0]: filename_index[1]]
    filename_extension = file_path[filename_index[1]:]
    directory_path = file_path[:filename_index[0]]
    return filename, filename_extension, directory_path


def save_rotate(img_path):
    """
    "path/[a-zA-Z0-9_-]+.*" 형식의 이미지 경로를 읽어
    시계방향으로 90도, 180도, 270도 회전한 이미지를
    각각 [a-zA-Z0-9_-]+_r90.*, [a-zA-Z0-9_-]+_r180.*, [a-zA-Z0-9_-]+_r270.*
    의 파일명으로 같은 디렉토리에 각각 저장함

    Args:
        img_path: 이미지 파일 경로, str 객체
    """
    filename, filename_extension, directory_path = path_decom(img_path)

    clock90_path = directory_path + filename + '_r90' + filename_extension
    clock180_path = directory_path + filename + '_r180' + filename_extension
    clock270_path = directory_path + filename + '_r270' + filename_extension

    img_bgr = cv2.imread(img_path)
    img_clock90 = cv2.rotate(img_bgr, cv2.ROTATE_90_CLOCKWISE)
    img_clock180 = cv2.rotate(img_bgr, cv2.ROTATE_180)
    img_clock270 = cv2.rotate(img_bgr, cv2.ROTATE_90_COUNTERCLOCKWISE)

    cv2.imwrite(clock90_path, img_clock90)
    cv2.imwrite(clock180_path, img_clock180)
    cv2.imwrite(clock270_path, img_clock270)


def rotation_point(x, y, w, h):
    """
    좌상단을 (0, 0) 으로 하는 이미지 상의 라벨링된 좌표에 대하여 각각 시계방향으로 90도, 180도, 270도 회전 후
    좌표를 리턴

    Args:
        x: 라벨링된 점의 너비 방향 좌표
        y: 라벨링된 점의 높이 방향 좌표
        w: 픽셀 단위의 이미지 너비
        h: 픽셀 단위의 이미지 높이

    Returns:
       변환된 점의 좌표를 ((x1, y1), (x2, y2), (x3, y3)) 형식의 튜플로 반환.
       순서대로 시계방향으로 90도, 180도, 270도 회전환 좌표이다.
    """
    location_clock90 = (h - 1 - y, x)
    location_clock180 = (w - 1 - x, h - 1 - y)
    location_clock270 = (y, w - 1 - x)
    return location_clock90, location_clock180, location_clock270


def is_labeled(dir_path):
    pass
    # todo: 라벨링 파일 무결성 검사(json 파일과 이미지 파일의 수가 일치하는지
    # todo: 같은 이미지 파일 이름에 대한 json 파일이 존재하는지


def rotation_json(path):
    """
    디렉토리 내의 모든 라벨링된 json 파일을 각각 시계방향으로 90도, 180도, 270도 회전시킨 json 파일을 저장한 뒤
    이미지 파일을 90도, 180도, 270도 회전시켜 저장한다.

    Args:
        path: 슬래시로 구분된 디렉토리 경로, str 객체
    """
    if path[-1] != '/':
        path = path + '/'
    # 디렉토리 안의 모든 파일명을 리스트로 반환
    file_list = os.listdir(path)
    json_structure = {
        "version": "4.5.7",
        "flags": {},
        "shapes": None,
        "imagePath": None,
        "imageData": None,
        "imageHeight": None,
        "imageWidth": None
    }

    for file in file_list:
        print(file)
        if re.search(r'(_r90|_r180|_r270)\..+$', file):
            continue
        if re.search(r'\.json$', file):
            continue
        else:
            img = 0
            file_path = path + file
            name_without_extension = re.sub(r'\..+$', '', file)
            img_extension = re.findall(r'\..+$', file)[0]
            json_path = path + name_without_extension + '.json'

            img = cv2.imread(file_path)
            h, w = img.shape[:2]
            for rotate_position in range(3):
                with open(json_path, 'r') as json_file:
                    shape_json = copy.deepcopy(json.load(json_file)["shapes"])
                new_json = copy.deepcopy(json_structure)
                if rotate_position % 2 == 1:
                    new_json["imageHeight"] = h
                    new_json["imageWidth"] = w
                else:
                    new_json["imageHeight"] = w
                    new_json["imageWidth"] = h
                shapes = []
                for shape in shape_json:
                    ro_points = []
                    for point in shape["points"]:
                        x, y = point
                        rotation_x, rotation_y = rotation_point(x, y, w, h)[rotate_position]
                        ro_points.append([rotation_x, rotation_y])
                    shape["points"] = ro_points
                    shapes.append(shape)
                new_json["shapes"] = shapes
                new_name = name_without_extension + '_r' + str(90 * (rotate_position + 1))
                new_json["imagePath"] = new_name + img_extension
                new_json_name = new_name + '.json'
                with open(path + new_json_name, 'w', encoding='utf-8') as json_save:
                    json.dump(new_json, json_save, ensure_ascii=False)
                    json_save.close()
            save_rotate(file_path)

if __name__=="__main__":
    directory = input("폴더 경로('\\ 가 아닌 /로 표시된 경로'): ")
    rotation_json(directory)