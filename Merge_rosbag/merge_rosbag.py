'''
Description: 
Version: 
Author: Leidi
Date: 2022-01-14 15:24:17
LastEditors: Leidi
LastEditTime: 2022-01-14 16:20:32
'''
import os
import yaml
import argparse
from rosbag import Bag

 
def main(rosbag_config):
    """[rosbag融合]

    Args:
        rosbag_config (dict): [rosbag融合信息字典]
    """
    
    rosbag_input_folder_list = []
    if rosbag_config['rosbag_input_folder'] is not None and os.path.exists(rosbag_config['rosbag_input_folder']):
        rosbag_input_folder = rosbag_config['rosbag_input_folder']
        for n in os.listdir(rosbag_input_folder):
            rosbag_input_folder_list.append(os.path.join(rosbag_config['rosbag_input_folder'], n))
            
    rosbag_input_path_list = []
    if rosbag_config['rosbag_input_path_list'] is not None:
        for n in rosbag_config['rosbag_input_path_list']:
            rosbag_input_path_list.append(n)
            
    total_rosbag_input_list = rosbag_input_folder_list + rosbag_input_path_list
    
    if 0 == len(total_rosbag_input_list):
        print("Rosbag input is empty, return!")
        return
    
    rosbag_output_path = rosbag_config['rosbag_output_path']
    
    total_msg_count = 0
    topics_list = []
    print('Star merge rosbag:')
    with Bag(rosbag_output_path, 'w') as output_bag: 
        for n in total_rosbag_input_list:
            print('Merge roabag {}:'.format(n))
            included_count = 0
            with Bag(n, 'r') as ib:
                for topic, message, time in ib:
                    if topic not in topics_list:
                        topics_list.append(topic)
                    output_bag.write(topic, message, time)
                    included_count += 1
                    print('{} add topic: {:>60}, time: {:>30}.'
                          .format(rosbag_output_path, topic, time))
            total_msg_count += included_count
            
    print('\nMerge rosbag end:')
    print('Total msg count: {}'.format(total_msg_count))
    print('Total topic count: {}'.format(len(topics_list)))
    print('Total topic:')
    for n in topics_list:
        print(n)
    
    return
 
if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='merge_rosbag.py')
    parser.add_argument('--config', '--c', dest='config', default=r'/home/leidi/hy_program/Rosbag_clean/Merge_rosbag/config/default.yaml',
                        type=str, help='rosbag config file path')
    opt = parser.parse_args()
    
    rosbag_config = yaml.load(open(opt.config, 'r'))
        
    main(rosbag_config)
    