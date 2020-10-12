#!/usr/local/bin/python3
import sys
import cv2
import numpy as np
import imutils
import pytesseract

input_img = cv2.imread('80.png')
grey = cv2.cvtColor(input_img, cv2.COLOR_BGR2GRAY)
cv2.imwrite('80_grey.png', grey)
ret, newimage = cv2.threshold(grey, 50,255,cv2.THRESH_BINARY_INV)
cv2.imwrite('80_result.png', newimage)
temp = pytesseract.image_to_string(newimage,config='--psm 6')
print("temp=", temp)
