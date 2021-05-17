import cv2
import numpy as np
"""
자동 객체 인식을 위한 기초 전처리 
"""


# 색범위 필터링
def color_filter(img, lower, upper):
    """
    색상 필터링
    참고) 필터링할 색 범위 지정(hsv system)에 대하여
    hsv 색공간은 h -> theta(θ), s -> r, v -> z 인 원주좌표계로 생각할 수 있다.
    그러나 opencv 에서 색상(h) 범위는 0~179, 채도(s) 범위 0 ~ 255, 명암(v) 범위 0 ~ 255 이므로
    원주좌표계 상에 표현된 hsv 값을 opencv의 스케일에 맞게 변환하여야 한다.

    Args:
        img: 처리 전 이미지, 3차원 numpy ndarray 객체
        lower: hsv 색공간에서 하한선, 길이가 3인 numpy array 객체
        upper: hsv 색공간에서 상한선, 길이가 3인 numpy array 객체

    returns:
        지정 범위의 색을 제외한것을 False, 지정 범위의 색을 포함한것을 True로 하는 binary 이미지,
        2차원 numpy ndarray 객체
    """
    mask = cv2.inRange(img, lower, upper)
    result = cv2.bitwise_and(img, img, mask=mask)
    # mask_inverse = cv2.bitwise_not(mask)
    # result_inverse = cv2.bitwise_and(img_grass, img_grass, mask=mask_inverse)
    return mask

# 경계선 감지
def boundary(img):
    """
    이미지의 경계선을 감지. 블러 처리 후 Canny edge filter 사용

    Args:
        img: 경계선을 감지할 이미지, cv2 img 객체

    returns:
        경계선을 True로 하는 binary 이미지, 2차원 numpy ndarray 객체
   """
    blur = cv2.GaussianBlur(img, ksize=(3, 3), sigmaX=50)
    result = cv2.Canny(blur, 100, 200)
    return result

# 객체 탐지(레이블링)
def labeling(binary_mask, front_image, filter_size):
    """
    이어진 부분을 한 객체로 인식하고 인식된 부분을 직사각형으로 라벨링하여 표시하는 함수

    Args:
        binary_mask: component 인식을 위한 binary 이미지, numpy ndarray 객체
        front_image: 인식 결과를 합성할 원본 이미지, numpy ndarray 객체
        filter_size: threshold 크기, 이 값보다 작은 크기의 component는 무시한다, int 객체

    returns:
        binary 이미지를 분석하여 객체를 인식하고 그 결과를 원본 이미지에 라벨링한 bgr 이미지 리턴,
        3차원 numpy ndarray 객체
    """
    count, labels, stats, centroids = cv2.connectedComponentsWithStats(binary_mask)
    # img_gbr = cv2.cvtColor(binary_mask, cv2.COLOR_GRAY2BGR)

    for i in range(1, count):
        (x, y, w, h, area) = stats[i]
        if area < filter_size:
            continue
        cv2.rectangle(front_image, (x, y, w, h), (255, 0, 0))

    return front_image

def point_clustering(image_path):
    """
    경계선 검출, 색상 검출, morphology, conponent 인식 순으로 이미지를 처리한 후 레이블 클러스터링을 통해
    식물을 인식하기 위한 함수

    Args:
        image_path: 분석 대상 이미지 경로, str 객체

    returns:
        이미지 클러스터링을 위해 component를 인식후 centroid 와 함께 라벨링한 bgr 이미지, 3차원 numpy ndarray
    """
    image_bgr = cv2.imread(image_path)
    image_hsv = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV)

    # 색상 필터 적용을 위한 파라미터
    lower = np.array([26, 25, 25])
    upper = np.array([83, 245, 245])

    # 경계선 감지, 색상 감지
    boundary_mask = boundary(image_hsv)
    color_mask = color_filter(image_hsv, lower, upper)

    # 마스크 and 연산
    merged_mask = cv2.bitwise_and(boundary_mask, color_mask)

    # morphology 연산
    morph_gradient = cv2.morphologyEx(merged_mask, cv2.MORPH_CLOSE, None)
    morph_open = cv2.morphologyEx(morph_gradient, cv2.MORPH_OPEN, None)

    # component 인식
    count, labels, stats, centroids = cv2.connectedComponentsWithStats(morph_open)

    for i in range(1, count):
        (x, y) = centroids[i]
        (x_area, y_area, w, h, area) = stats[i]
        if area < 50:
            continue
        cv2.circle(image_bgr, (int(x), int(y)), 10, (255, 0, 0), 2)
        cv2.rectangle(image_bgr, (x_area, y_area, w, h), (0, 0, 255))

    return image_bgr

def label_clustering(image_path):
    """
    경계선 검출, 색상 검출, conponent 인식 순으로 이미지를 처리한 후 레이블 클러스터링을 통해
    식물을 인식하기 위한 함수

    Args:
        image_path: 분석 대상 이미지 경로, str 객체

    returns:
        이미지 클러스터링을 위해 component를 인식후 라벨링한 bgr 이미지, 3차원 numpy ndarray
        """
    image_bgr = cv2.imread(image_path)
    image_hsv = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV)

    # 색상 필터 적용을 위한 파라미터
    lower = np.array([26, 25, 25])
    upper = np.array([83, 245, 245])

    # 경계선 감지, 색상 감지
    boundary_mask = boundary(image_hsv)
    color_mask = color_filter(image_hsv, lower, upper)

    # 마스크 and 연산
    merged_mask = cv2.bitwise_and(boundary_mask, color_mask)

    # component 인식 후 레이블링
    result = labeling(merged_mask, image_bgr, 70)
    return result

def plant_boundary(image_path):
    """
    식물의 경계를 검출하는 함수

    Args:
        image_path: 분석 대상 이미지의 경로, str 객체

    returns:
        식물의 경계를 검출한 binary 이미지, 2차원 numpy ndarray
    """
    image_bgr = cv2.imread(image_path)
    image_hsv = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV)
    image_gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)

    # 색 범위 변수, 노랑~파랑의 범위 내에서 적절히 조정하였음
    lower1 = np.array([26, 70, 70])
    upper1 = np.array([83, 250, 250])

    # CLAHE
    # 히스토그램 균일화
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    clahe_image = clahe.apply(image_gray)

    # 경계검출, 색상 검출
    boundary_canny = boundary(clahe_image)
    color_mask = color_filter(image_hsv, lower1, upper1)

    # 이진화된 영상에 and 연산 수행
    combined_mask = cv2.bitwise_and(boundary_canny, color_mask)

    # 모폴로지 연산: 그래디언트
    morph_gradient = cv2.morphologyEx(combined_mask, cv2.MORPH_GRADIENT, None)

    return morph_gradient


def main():
    boundary_img1 = plant_boundary("./test_image/for_rec.jpg")
    boundary_img2 = plant_boundary("./test_image/se1.png")


    # case1_img1 = point_clustering("./test_image/for_rec.jpg")
    # case1_img2 = point_clustering("./test_image/se1.png")
    #
    # case2_img1 = label_clustering("./test_image/for_rec.jpg")
    # case2_img2 = label_clustering("./test_image/se1.png")

    cv2.imshow('boundary_img1', boundary_img1)
    cv2.imshow('boundary_img2', boundary_img2)
    # cv2.imshow('case1_img1', case1_img1)
    # cv2.imshow('case1_img2', case1_img2)
    # cv2.imshow('case2_img1', case2_img1)
    # cv2.imshow('case2_img2', case2_img2)
    cv2.waitKey()
    cv2.destroyAllW

if __name__ == "__main__":
    main()


