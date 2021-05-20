import cv2
import numpy as np
import random
import re
import json
import copy
import os
import pathlib

# 이미지 자동 합성 및 증강  테스트입니다.
# 일단 단순하게 검은색 배경을 잘라서 덧씌우는것 뿐이므로 부자연스럽게 보임. 차후에 개선할 것

def foreground_mask(img_bgr):
    """
    soybean(from kaggle) 데이터의 검은색 마스크를 제거하고 식물이 존재하는 곳을 True 로 하는
    바이너리 이미지 반환

    Args:
        img_bgr: bgr 이미지, 3차원 numpy ndarray 객체

    Returns:
        식물이 존재하는 곳을 True 로 하는 바이너리 이미지, 2차원 numpy ndarray 객체
    """
    img_hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
    lower = np.array([0, 0, 0])
    upper = np.array([179, 5, 5])
    chroma_filter = cv2.inRange(img_hsv, lower, upper)
    chroma_inv = cv2.bitwise_not(chroma_filter)

    kernel_erosion = np.ones((5, 5), np.uint8)
    kernel_dilation = np.ones((3, 3), np.uint8)

    # morphology open
    morph_erosion = cv2.morphologyEx(chroma_inv, cv2.MORPH_ERODE, kernel=kernel_erosion)
    morph_dilate = cv2.morphologyEx(morph_erosion, cv2.MORPH_DILATE, kernel=kernel_dilation)
    cv2.imshow('color_filter', chroma_inv)
    cv2.imshow('morph_dilate', morph_dilate)
    return morph_dilate

img_grass = cv2.imread("./test_image/grass18.jpg")
img_soil = cv2.imread("./test_image/soil1.jpg")

# 전경 크기
heigth_grass, width_grass = img_grass.shape[:2]

# 배경 크기
heigth_soil, width_soil = img_soil.shape[:2]

# 합성 가능한 좌표 범위
x_max = width_soil - width_grass
y_max = heigth_soil - heigth_grass

# 합성할 좌표 지정
x = random.randrange(0, x_max)
y = random.randrange(0, y_max)
w = x + width_grass
h = y + heigth_grass

# 크로마키 영역과 영상 전체 hsv로 변경
hsv_img = cv2.cvtColor(img_grass, cv2.COLOR_BGR2HSV)

# offset try and catch
# H: 색상, S: 채도, V: 명도
lower = np.array([0, 0, 0])
upper = np.array([179, 10, 10])

# 마스크 생성
# hsv_img: img_grass 를 hsv로 변환한 것
mask_inv = foreground_mask(img_grass)
mask = cv2.bitwise_not(mask_inv)

# 합성할 좌표 지정
roi = img_soil[y:h, x:w]

# 전경에서 크로마키를 제외한 부분의 좌표
fg = cv2.bitwise_and(img_grass, img_grass, mask=mask_inv)

# 배경에서 크로마키 부분의 좌표
bg = cv2.bitwise_and(roi, roi, mask=mask)

# 처리한 이미지 합성
img_soil[y:h, x:w] = fg + bg

# 출력
cv2.imshow('chromakey', img_grass)
cv2.imshow('added', img_soil)
cv2.waitKey()
cv2.destroyAllWindows()
