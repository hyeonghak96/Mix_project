import cv2
import numpy as np

# 이미지 읽기
img_grass = cv2.imread("./test_image/for_rec.jpg")

# 높이, 너비 인식
heigth_grass, width_grass = img_grass.shape[:2]

# hsv형식으로 변환
hsv_grass = cv2.cvtColor(img_grass, cv2.COLOR_BGR2HSV)

# 마스킹할 색 범위 지정(hsv system)
# 초록 계열은 식물, 나머지는 식물이 아니라 필요없으니까
lower = np.array([26, 0, 0])
upper = np.array([86, 255, 255])

# 지정한 색 범위로 마스크 생성
mask = cv2.inRange(hsv_grass, lower, upper)
mask_inverse = cv2.bitwise_not(mask)

# 1차 처리: 색범위로 필터링
process1 = cv2.bitwise_and(img_grass, img_grass, mask=mask)
process1_inverse = cv2.bitwise_and(img_grass, img_grass, mask=mask_inverse)

# 1.5차 처리: 블러(경계선 과적합 방지)
# ksize: 블러 크기
blur = cv2.GaussianBlur(process1, ksize=(3,3), sigmaX=0)

# 2차처리: 캐니 엣지 필터 사용
# 경계선 얻음
process2 = cv2.Canny(blur, 10, 250)


# todo: 채도, 명암 표준화 해야함
# todo: 경계선 감지 부분에서(2차처리) 색범위로 필터링된 검은색 부분에 대해서는 경계선을 그리지 않도록 할것
# todo: 위 작업들을 완료한 후 경계선의 x, y 방향 최소, 최대 좌표값을 구하여 직사각형을 그리면 open cv로도 객체 인식이 가능하지 않나..



# 1차 처리 및 2차처리 이미지 디스플레이
cv2.imshow('1st_process', process1)
cv2.imshow('2nd_process', process2)
cv2.waitKey()
cv2.destroyAllWindows()


