#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import String
from monitor.msg import jetson_data

string = "RAM 1652/7854MB (lfb 1237x4MB) CPU [1%@2035,0%@2035,0%@2035,4%@2035,1%@2035,6%@2035] BCPU@31C MCPU@31C GPU@29.5C PLL@31C Tboard@27C Tdiode@27.25C PMIC@100C thermal@30.1C VDD_IN 2451/2471 VDD_CPU 306/311 VDD_GPU 153/153 VDD_SOC 612/612 VDD_WIFI 0/10 VDD_DDR 828/828"
string = string.split(" ")

def jetson_monitor():
    pub = rospy.Publisher('jetson_info', jetson_data, queue_size=10)
    rospy.init_node('jetson_monitor', anonymous=True)
    rate = rospy.Rate(1) # 10hz
    while not rospy.is_shutdown():
        #hello_str = "hello world %s" % rospy.get_time()
        data = jetson_data()
        global string
        CPU_percentage = string[5]
        CPU_percentage = CPU_percentage.split("[")
        CPU_percentage = CPU_percentage[1]
        CPU_percentage = CPU_percentage.split("]")
        CPU_percentage = CPU_percentage[0]
        CPU_percentage = CPU_percentage.split("%@")
        for i in range(5):
            CPU_percentage[i + 1] = CPU_percentage[i + 1].split(",")
            CPU_percentage[i + 1] = CPU_percentage[i + 1][1]
        del CPU_percentage[-1]
        data.CPU1_percentage = int(CPU_percentage[0])
        data.CPU2_percentage = int(CPU_percentage[1])
        data.CPU3_percentage = int(CPU_percentage[2])
        data.CPU4_percentage = int(CPU_percentage[3])
        data.CPU5_percentage = int(CPU_percentage[4])
        data.CPU6_percentage = int(CPU_percentage[5])

        RAM = string[1]
        RAM = RAM.split("/")
        RAM[1] = RAM[1].split("M")
        data.RAM_max = int(RAM[1][0])
        data.RAM_min = int(RAM[0])
        data.RAM_percentage = (data.RAM_min*100)/data.RAM_max
        
        rospy.loginfo("Nothing")
        pub.publish(data)
        rate.sleep()
        

"""
import rospy
from std_msgs.msg import String
from monitor.msg import jetson_data

def talker():
    pub = rospy.Publisher('chatter', String, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(0.2) # 10hz
    while not rospy.is_shutdown():
        hello_str = "hello world %s" % rospy.get_time()
        rospy.loginfo(hello_str)
        pub.publish(hello_str)
        rate.sleep()

"""

if __name__ == '__main__':
    try:
        jetson_monitor()
    except rospy.ROSInterruptException:
        pass