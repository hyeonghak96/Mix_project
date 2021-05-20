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

def image_blur(path, blur_size):
    """
        path 에 있는 이미지를 블러 처리하여 저장함

        Args:
            img_path: 이미지 파일 경로, str 객체
            blur_size: 블러 크기, 홀수 int 객체
        """
    filename, filename_extension, directory_path = path_decom(path)
    blur_path = directory_path + filename + '_augblur' + str(blur_size) + filename_extension
    bgr_image = cv2.imread(path)
    blur = cv2.GaussianBlur(bgr_image, ksize=(blur_size, blur_size), sigmaX=50)
    cv2.imwrite(blur_path, blur)


def blur_json(path, blur_size):
    """
    디렉토리 내의 모든 라벨링된 이미지 파일을 블러 처리하여 *_augblur.* 형식의 이름으로 저장

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
        if re.search(r'.*(_augblur).*\..+$', file):
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

            with open(json_path, 'r') as json_file:
                shape_json = copy.deepcopy(json.load(json_file)["shapes"])
            new_json = copy.deepcopy(json_structure)
            new_json["imageHeight"] = h
            new_json["imageWidth"] = w
            shapes = []
            for shape in shape_json:
                ro_points = []
                for point in shape["points"]:
                    x, y = point
                    ro_points.append([x, y])
                shape["points"] = ro_points
                shapes.append(shape)
            new_json["shapes"] = shapes
            new_name = name_without_extension + '_augblur' + str(blur_size)
            new_json["imagePath"] = new_name + img_extension
            new_json_name = new_name + '.json'
            with open(path + new_json_name, 'w', encoding='utf-8') as json_save:
                json.dump(new_json, json_save, ensure_ascii=False)
                json_save.close()

            image_blur(file_path, blur_size)

if __name__=="__main__":
    directory = input("폴더 경로('\\ 가 아닌 /로 표시된 경로'): ")
    size = input("블러 크기(홀수인 양의 정수): ")
    size = int(size)
    if size % 2 == 0:
        raise TypeError("블러 크기는 홀수인 양의 정수여야 합니다.")
    blur_json(directory, size)
