#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import String, Int8
import random
from std_msgs.msg import MultiArrayDimension
from std_msgs.msg import MultiArrayLayout
from std_msgs.msg import Int16MultiArray

def talker():
    pub = rospy.Publisher('get_speed_from_random', Int16MultiArray, queue_size=10)
    rospy.init_node('get_speed_from_random', anonymous=True)
    rate = rospy.Rate(0.1)
    while not rospy.is_shutdown():

        
        speed1 = random.randint(200, 250)
        speed2 = random.randint(200, 250)

	speed1_boolean = random.randint(0, 1)
	speed2_boolean = random.randint(0, 1)

	if speed1_boolean == 1:
	    speed1 = -speed1

	if speed2_boolean == 1:
	    speed2 = -speed2
        
        var_from_the_phone = Int16MultiArray()
        var_from_the_phone.data = [speed1, speed2]

        rospy.loginfo(var_from_the_phone)
        pub.publish(var_from_the_phone)
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
