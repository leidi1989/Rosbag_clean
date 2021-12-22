'''
Description: 
Version: 
Author: Leidi
Date: 2021-12-22 18:21:36
LastEditors: Leidi
LastEditTime: 2021-12-22 19:19:56
'''
import re
import os
import cv2
import yaml
import rospy
import rosbag
import os.path
import argparse
from cv_bridge import CvBridge
from cv_bridge import CvBridgeError

def main(rosbag_config: dict)-> None:
    
    path=r'/mnt/data_1/Data/rosbag/images/qunguang_2021-12-07-11-47-22'
    path2 =  r'/mnt/data_1/Data/rosbag/qunguang/20211209/'
    num_count = 15
    for filename in os.listdir(path2):
        paron = r"1209_qunguang1_2_2021-12-09-11-01-17_1.bag"
        if re.search(paron,filename) != None:
            print(os.path.join(path2, filename))
            try:
                bridge = CvBridge()
                topic_LIST = [0,0,0,0,0,0,0,0,0,0,0]
                print(filename)
                num_count = 15
                with rosbag.Bag(filename,'r') as bag:
                    for topic,msg,t in bag.read_messages():
                        if bool_topic(topic) >= 1:
                            cv_path = path + topic.split('/')[1]
                            topic_LIST[bool_topic(topic)] += 1
                            if topic_LIST[bool_topic(topic)] % num_count != 0 :
                                continue
                            try:
                                cv_image = bridge.compressed_imgmsg_to_cv2(msg,"bgr8")
                            except CvBridgeError as e:
                                print (e)
                            timestr = "%.6f" % msg.header.stamp.to_sec()
                            image_name = timestr+".png"
                            if not os.path.exists(cv_path):
                                os.makedirs(cv_path)
                            cv2.imwrite(cv_path+'/'+image_name,cv_image)
            except rospy.ROSInterruptException:
                pass
    return

def bool_topic(topic):
    if(topic == "/cam_left_back/csi_cam/image_raw/compressed"):
        return 0
    elif (topic == "/cam_right_back/csi_cam/image_raw/compressed"):
        return 0
    elif (topic == "/cam_right_front/csi_cam/image_raw/compressed"):
        return 0
    elif (topic == "/cam_left_front/csi_cam/image_raw/compressed"):
        return 0
    elif (topic == "/cam_front_center/csi_cam/image_raw/compressed"):
        return 1
    elif (topic == "/cam_back/csi_cam/image_raw/compressed"):
        return 2
    elif (topic == "/cam_right_fish/csi_cam/image_raw/compressed"):
        return 0
    elif (topic == "/cam_front_fish/csi_cam/image_raw/compressed"):
        return 0
    elif (topic == "/cam_back_fish/csi_cam/image_raw/compressed"):
        return 0
    elif (topic == "/cam_left_fish/csi_cam/image_raw/compressed"):
        return 0
    else : 
        return 0


                
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='rosbag_to_image.py')
    parser.add_argument('--config', '--c', dest='config', default=r'/home/leidi/hy_program/Rosbag_clean/Get_image/config/default.yaml',
                        type=str, help='rosbag config file path')
    opt = parser.parse_args()

    rosbag_config = yaml.load(open(opt.config, 'r'))

    main(rosbag_config)
