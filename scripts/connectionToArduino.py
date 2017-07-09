#!/usr/bin/env python

import rospy
from rosserial_python import SerialClient, RosSerialServer
from serial import SerialException
from time import sleep
import multiprocessing


import sys

if __name__=="__main__":

    rospy.init_node("speed_motor_arduino")
    rospy.loginfo("ROS Serial Python Node")

    port_name = rospy.get_param('~port','/dev/ttyACM0')
    baud = int(rospy.get_param('~baud','57600'))

    sys.argv = rospy.myargv(argv=sys.argv)

    while not rospy.is_shutdown():
        rospy.loginfo("Connecting to %s at %d baud" % (port_name,baud) )
        try:
           client = SerialClient(port_name, baud)
           client.run()
        except KeyboardInterrupt:
             break
        except SerialException:
            sleep(1.0)
            continue
        except OSError:
            sleep(1.0)
            continue

