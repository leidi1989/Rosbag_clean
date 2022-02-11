#!/bin/sh
###
# @Description:
# @Version:
# @Author: Leidi
# @Date: 2022-01-14 18:00:41
 # @LastEditors: Leidi
 # @LastEditTime: 2022-01-19 14:20:45
###

rosbag_path='/mnt/data_2/Rosbag/parking/wudazhuoer_parking/wudazhuoer_parking_cam_back_2021-11-28_1.bag'
speed='10'

if [$speed == '']; then
    rosbag info $rosbag_path
    rosbag play $rosbag_path -l
else
    rosbag info $rosbag_path
    rosbag play $rosbag_path -r $speed -l
fi
