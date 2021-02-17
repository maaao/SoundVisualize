import numpy as np
import cv2

def nothing(x):
    pass

img = cv2.imread("data/images/test/denki/0.png")
img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
img_split = cv2.split(img_hsv)

threshold_val = 64
cv2.namedWindow("img_bin")
cv2.createTrackbar('threshold_val', "img_bin", threshold_val, 255,  nothing)

while True:
    threshold_val = cv2.getTrackbarPos("threshold_val", "img_bin")

    ret, img_bin = cv2.threshold(img_split[0], threshold_val, 255, cv2.THRESH_TOZERO)
    
    cv2.imshow("img", img)
    cv2.imshow("img_hsv", img_split[0])
    cv2.imshow("img_hsv1", img_split[1])
    cv2.imshow("img_hsv2", img_split[2])
    cv2.imshow("img_bin", img_bin)
    img_bin = img_bin*0
    
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
         break