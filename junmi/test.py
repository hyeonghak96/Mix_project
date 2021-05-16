import cv2
import numpy as np
from img_aug import Img_aug #데이터 증강 class 불러오기

aug = Img_aug()  #데이터 증강 class 선언
augment_num = 40
save_path = '{image_save_path}/'

img = cv2.imread('{image_path}g')
images_aug = aug.seq.augment_images([img for i in range(augment_num)])

for num, aug_img in enumerate(images_aug) :
    cv2.imwrite(save_path+'plant_{}.jpg'.format(num), aug_img)
    
print('complete augmenting images')