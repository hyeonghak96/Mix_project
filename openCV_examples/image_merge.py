import cv2
import numpy as np
import matplotlib.pylab as plt

img_grass = cv2.imread("./test_image/grass18.jpg")
img_soil = cv2.imread("./test_image/soil1.jpg")

heigth_grass, width_grass = img_grass.shape[:2]
heigth_soil, width_soil = img_soil.shape[:2]

# 좌표계산
x = (width_soil - width_grass) // 2
y = heigth_soil - heigth_grass

w = x + width_grass
h = y + heigth_grass

# 크로마키 지정
chromakey = img_grass[:2, :2, :]
offset = 30

# 크로마키 영역과 영상 전체 hsv로 변경
hsv_chroma = cv2.cvtColor(chromakey, cv2.COLOR_BGR2HSV)
hsv_img = cv2.cvtColor(img_grass, cv2.COLOR_BGR2HSV)

# offset try and catch
# H: 색상, S: 채도, V: 명도
chroma = hsv_chroma[:, :, 0]
lower = np.array([0, 0, 0])
upper = np.array([179, 0, 0])

# 마스크 생성
# hsv_img: img_grass 를 hsv로 변환한 것
mask = cv2.inRange(hsv_img, lower, upper)
mask_inv = cv2.bitwise_not(mask)

# 합성할 좌표 지정
roi = img_soil[y:h, x:w]

# 전경에서 크로마키를 제외한 부분의 좌표
fg = cv2.bitwise_and(img_grass, img_grass, mask=mask_inv)
print(fg)

# 배경에서 크로마키 부분의 좌표
bg = cv2.bitwise_and(roi, roi, mask=mask)

# 처리한 이미지 합성
img_soil[y:h, x:w] = fg + bg

# 출력
cv2.imshow('chromakey', img_grass)
cv2.imshow('added', img_soil)
cv2.waitKey()
cv2.destroyAllWindows()
