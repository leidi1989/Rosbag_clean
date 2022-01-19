#!/bin/sh
###
# @Description:
# @Version:
# @Author: Leidi
# @Date: 2022-01-14 18:00:41
 # @LastEditors: Leidi
 # @LastEditTime: 2022-01-19 13:53:36
###
rosbag_path='/mnt/data_2/Rosbag/parking/chuangyicheng_parking/chuangyicheng_parking_2022-1-18_0.bag'
speed='10'

if [$speed == '']; then
    rosbag info $rosbag_path
    rosbag play $rosbag_path -l
else
    rosbag info $rosbag_path
    rosbag play $rosbag_path -r $speed -l
fi
