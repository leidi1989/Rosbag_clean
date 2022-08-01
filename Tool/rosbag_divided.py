#!/usr/bin/python3 
'''
Date         : 2021-10-27 10:32:09
LastEditors  : lx <m335800283@outlook.com>
LastEditTime : 2021-12-14 13:25:48
FilePath     : /rosbag_divided/rosbag_divided.py
'''

import os
import re
import sys
import getopt
import readline
# from icecream import ice
sys.path.append('./')

def main(argv):
    inputfile = ''
    outputfile = ''
    cmd_str = ' '
    
    try:
        opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
        print ('usecase: rosbag_divided.py -i <inputfile> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('usecase: rosbag_divided.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
            rosbag_info_res = os.popen("rosbag info {}".format(inputfile))
        elif opt in ("-o", "--ofile"):
            outputfile = arg
    input_str = input(
        '''\rPlease select filter criteria:
            \r[1]  t.secs,t.nsecs
            \r[2]  topic\r\n''')
    if input_str in ("1"):
        st=et=0
        errorr_count=1
        data = rosbag_info_res.read()
        print(data)
        try:
            time_res = re.search(r"start:.*\((\d+).\d+\)\send:.*\((\d+).\d+\)",data)
            st = time_res.group(1)
            et = time_res.group(2)
        except:
            st=et=-1
        while(errorr_count):
            if errorr_count>3:
                return 
            input_time = input("Please enter the start time and end time  the field of [{} , {}] (separated by spaces)  :\n".format(st,et)).split()
            if len(input_time)!=2 or  not input_time[0].isdigit() or not input_time[1].isdigit() or int(input_time[0])<0 or int(input_time[1])<0 or int(input_time[1])-int(input_time[0])<0:
                errorr_count+=1
                print("Input  error!")
            else:
                st=input_time[0]
                et=input_time[1]
                cmd_str = 'rosbag filter {} {} "t.secs >= {} and t.secs <= {}"'.format(inputfile,outputfile,st,et) 
                break
    elif input_str in ("2"):
        input_str="\rchoose topic :\n"
        topic_list = []
        for line in rosbag_info_res.readlines():
            re_res = re.search(r"\s+(.*)\s+\d+\s+msgs",line)
            if re_res != None:
                topic_list.append(re_res.group(1))
        if len(topic_list)<=0:
            print("topic not find!")
            return 
        else:
            for index,topic in enumerate(topic_list):
                input_str+=("[{}] {}\n".format(index,topic))
            choseed_topic_list =[int(x) if x.isdigit() else None for x in  input(input_str).split()]
            if len(choseed_topic_list)<1:
                print("input error!")
                return 
            res_list = []
            for topic_id in choseed_topic_list:
                if topic_id==None or topic_id<0 or topic_id>(len(topic_list)-1):
                    continue
                res_list.append(topic_id)
            res_list = list(set(res_list))
            for topic_id in res_list:
                if topic_id != res_list[-1]:
                    cmd_str+="topic == '{}' or ".format(topic_list[topic_id].strip())
                else:
                    cmd_str+="topic == '{}'".format(topic_list[topic_id].strip())
            cmd_str = 'rosbag filter {} {} "{}"'.format(inputfile,outputfile,cmd_str)
            print(cmd_str)
    else:
        print("input error!")
        return 
    res = os.system(cmd_str)
    if not res:
        print("done!")
    else:
        print("faild!")

         
    
if __name__=='__main__':
    main(sys.argv[1:])