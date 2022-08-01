'''
Description: 
Version: 
Author: Leidi
Date: 2022-04-26 20:03:19
LastEditors: Leidi
LastEditTime: 2022-04-26 20:04:21
'''
import cv2

image_input_path = r'/home/leidi/Desktop/2022-04-26-19-41-11/cross_view_input_net_image/0.000000.png'
image_output_path = r'/home/leidi/Desktop/2022-04-26-19-41-11/cross_view_input_net_image/0.000000_resize.png'
image = cv2.imread(image_input_path)
image = cv2.resize(image, (1280*3, 720*2))
cv2.imwrite(image_output_path, image)
# cv2.imshow('one', image)
# cv2.waitKey(0)