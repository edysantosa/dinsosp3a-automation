# enhance gambar capcha

import cv2
import numpy as np

img = cv2.imread("gambar.png")

# invert warna
img = cv2.bitwise_not(img)

# dilate image
kernel = np.ones((2,2),np.uint8)
dilation = cv2.dilate(img,kernel,iterations = 1)
# erode image
erosion = cv2.erode(dilation,kernel,iterations = 1)
# clean 
opening = cv2.morphologyEx(erosion, cv2.MORPH_OPEN, kernel)

hasil = cv2.bitwise_not(opening)
cv2.imwrite('./hasil.png', hasil)

cv2.imshow('image',hasil)
cv2.waitKey(0)