'''
Description: 
Version: 
Author: Leidi
Date: 2021-12-22 18:21:36
LastEditors: Leidi
LastEditTime: 2021-12-23 11:04:12
'''
import os
import cv2
import yaml
import shutil
import rosbag
import argparse
from cv_bridge import CvBridge
from cv_bridge import CvBridgeError


def main(rosbag_config):
    
    if not os.path.exists(rosbag_config['image_output_folder']):
        print('Create images folder:')
        os.makedirs(rosbag_config['image_output_folder'])
    else:
        shutil.rmtree(rosbag_config['image_output_folder'])
        print('Create images folder:')
        os.makedirs(rosbag_config['image_output_folder'])
        
    print('Start get image:')
    topic_image_output_count_dict = {x:0 for x in rosbag_config['rosbag_topic']}
    if rosbag_config['rosbag_folder'] == None and rosbag_config['rosbag_path'] != None:
        bridge = CvBridge()
        topic_dict = {x:0 for x in rosbag_config['rosbag_topic']}
        with rosbag.Bag(rosbag_config['rosbag_path'], 'r') as bag:
            for topic, msg, t in bag.read_messages():
                if topic in topic_dict:
                    image_output_path = os.path.join(rosbag_config['image_output_folder'], topic.split('/')[1])
                    topic_dict[topic] += 1
                    if 0 == (topic_dict[topic] % rosbag_config['fps']):
                        cv_image = bridge.compressed_imgmsg_to_cv2(msg, "bgr8")
                        image_name = '%.6f.png' % msg.header.stamp.to_sec()
                        print('Create topic message: {:>60} to image: {:>50}'.format(topic, image_name))
                        cv2.imwrite(os.path.join(image_output_path, image_name), cv_image)
                        topic_image_output_count_dict[topic] += 1
    else:
        for filename in os.listdir(rosbag_config['rosbag_folder']):
            rosbag_path = os.path.join(rosbag_config['rosbag_folder'], filename)
            bridge = CvBridge()
            topic_dict = {x:0 for x in rosbag_config['rosbag_topic']}
            with rosbag.Bag(rosbag_path,'r') as bag:
                for topic, msg, t in bag.read_messages():
                    if topic in topic_dict:
                        image_output_path = os.path.join(rosbag_config['image_output_folder'], topic.split('/')[1])
                        if not os.path.exists(image_output_path):
                            os.makedirs(image_output_path)
                        topic_dict[topic] += 1
                        if 0 == (topic_dict[topic] % rosbag_config['fps']):
                            cv_image = bridge.compressed_imgmsg_to_cv2(msg, "bgr8")
                            image_name = '%.6f.png' % msg.header.stamp.to_sec()
                            print('Create topic message: {:>60} to image: {:>50}'.format(topic, image_name))
                            cv2.imwrite(os.path.join(image_output_path, image_name), cv_image)
                            topic_image_output_count_dict[topic] += 1
    print('Total topic message create image:')
    for key, velue in topic_image_output_count_dict.items():
        print('{}: \t {}'.format(key, velue))
        
    return

    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='rosbag_to_image.py')
    parser.add_argument('--config', '--c', dest='config', default=r'/home/leidi/hy_program/Rosbag_clean/Get_image/config/default.yaml',
                        type=str, help='rosbag config file path')
    opt = parser.parse_args()
    
    rosbag_config = yaml.load(open(opt.config, 'r'))
        
    main(rosbag_config)
