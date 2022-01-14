#!/bin/sh
###
# @Description:
# @Version:
# @Author: Leidi
# @Date: 2022-01-14 18:00:41
# @LastEditors: Leidi
# @LastEditTime: 2022-01-14 18:25:27
###
rosbag_path='/mnt/data_2/Rosbag/parking/zhanshi1_2021-11-21-11-56-02_0.bag'
speed=''

if [$speed == '']; then
    rosbag info $rosbag_path
    rosbag play $rosbag_path
else
    rosbag info $rosbag_path
    rosbag play $rosbag_path -r $speed
fi
