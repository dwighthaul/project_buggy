#!/usr/bin/env python
# license removed for brevity
import rospy
import array
from std_msgs.msg import Int8, Int16
import random
from std_msgs.msg import MultiArrayDimension
from std_msgs.msg import MultiArrayLayout
from project_buggy.msg import SpeedMotors
from std_msgs.msg import Int8MultiArray, Int16MultiArray
import json


import socket



HOST = ''				 # Symbolic name meaning all available interfaces
PORT = 50007			  # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((HOST, PORT))

def talker():

	val1 = 0
	val2 = 0

	pub = rospy.Publisher('speed_from_socket', SpeedMotors, queue_size=10)

	rospy.init_node('speedFromSocket', anonymous=True)
	rate = rospy.Rate(10) # 10hz
	while not rospy.is_shutdown():

#	print 'val1 ', val1, 'val2 ', val2

		data = ""

		s.listen(1)
		conn, addr = s.accept()
#		print 'Connected by ', addr

		while 1:
			data = conn.recv(1024)

			if not data: break


			Jsondata = json.loads(data)

			try:
				print(str(Jsondata) + "\n")

				val1 = Jsondata['speed_left']
				val2 = Jsondata['speed_right']
				is_autonomus = Jsondata['is_autonomus']

				var_from_socket = SpeedMotors()
				var_from_socket.speed_right_motor = val1
				var_from_socket.speed_left_motor = val2

				var_from_socket.mode = "socket"


				pub.publish(var_from_socket)
			except Exception:
				pass


#		rate.sleep()

if __name__ == '__main__':
	try:
		talker()
	except rospy.ROSInterruptException:
		pass
