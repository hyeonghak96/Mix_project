import numpy as np
import cv2
from matplotlib import pyplot as plt

'''
img = cv2.imread('..//img_for_prep//1.jpg')
img.shape  # (1024, 1536, 3)

# crop image
height, width = img.shape[:2]
startRow = int(height*.15)
startCol = int(width*.08)
endRow = int(height*.85)
endCol = int(width*.92)

cropped = img[startRow:endRow, startCol:endCol]
cv2.imwrite('..//img_for_prep//1_7.jpg', cropped)
'''

'''
# grabCut
img = cv2.imread('..//img_for_prep//1_7.jpg')
print(img.shape)

mask = np.zeros(img.shape[:2], np.uint8)  # uint8 : unsigned int8 (0 ~ 255)

bgdModel = np.zeros((1, 65), np.float64)
fgdModel = np.zeros((1, 65), np.float64)

rect = (1, 1, 1290, 716)
cv2.grabCut(img, mask, rect, bgdModel, fgdModel, 1, cv2.GC_INIT_WITH_RECT)

mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
img = img*mask2[:, :, np.newaxis]

cv2.imwrite('..//img_for_prep//1_8.jpg', img)
'''

# resize
img = cv2.imread('..//img_for_prep//1_8.jpg')
resized = cv2.resize(img, (249, 223))
cv2.imwrite('..//img_for_prep//1_9.jpg', resized)
