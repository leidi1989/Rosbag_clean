#!/bin/sh
###
# @Description:
# @Version:
# @Author: Leidi
# @Date: 2022-01-14 18:00:41
 # @LastEditors: Leidi
 # @LastEditTime: 2022-01-14 18:52:18
###
rosbag_path='/mnt/data_2/Rosbag/qunguang1_2_2021-12-09-11-01-17_0.bag'
speed='30'

if [$speed == '']; then
    rosbag info $rosbag_path
    rosbag play $rosbag_path -l
else
    rosbag info $rosbag_path
    rosbag play $rosbag_path -r $speed -l
fi
