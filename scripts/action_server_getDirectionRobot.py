#! /usr/bin/env python

import roslib
import rospy
import actionlib
import time

from project_buggy.msg import SpeedMotors

from slam_project_buggy.msg import setDirectionRobotAction, setDirectionRobotResult
from std_msgs.msg import Int16MultiArray, MultiArrayDimension, MultiArrayLayout


secs = 1

class serverSetDirectionRobot:



	stop_wheel= Int16MultiArray()
	stop_wheel.data = [0, 0]


	speed_wheel = Int16MultiArray()

	def __init__(self):
		rospy.init_node('set_direction')

		self.server = actionlib.SimpleActionServer('speed_from_action', setDirectionRobotAction, self.execute, False)
		self.pubToArduino = rospy.Publisher('speed_motor_arduino', Int16MultiArray, queue_size=10)

		self.server.start()
		rospy.loginfo("Server started")




	def modificator_direction(self, speed_wheel, action):
		r_speed_wheel = [speed_wheel.data[0]*2.20, speed_wheel.data[1]*2.20]
		# rospy.loginfo("Final Speed %s - %s", r_speed_wheel[0], r_speed_wheel[1])
		return r_speed_wheel



	# Work with the main server, see in src
	# def change_direction(self, speed_wheel, action):

	# 	self.publishSpeed(speed_wheel)

	# 	if action.stopWheels:
	# 		time.sleep(secs)
	# 		rospy.loginfo("Back to previous")

	# 		self.publishSpeed(self.stop_wheel)

	# def publishSpeed(self, speed_wheel):
	# 	speedArray = SpeedMotors()
	# 	speedArray.speed_right_motor = speed_wheel[0]
	# 	speedArray.speed_left_motor = speed_wheel[1]

	# 	self.pubToMain.publish(speedArray)



	# Work with the arduino
	def change_directionToArduino(self, speed_wheel, action):
		pub_speed_wheel= Int16MultiArray()
		pub_speed_wheel.data = speed_wheel

		self.publishSpeedToArduino(pub_speed_wheel)

		if action.stopWheels:
			time.sleep(secs)

			rospy.loginfo("Back to previous")

			self.publishSpeedToArduino(self.stop_wheel)




	def publishSpeedToArduino(self, speed_wheel):
		self.pubToArduino.publish(speed_wheel)




	def execute(self, action):

		speed_wheel = Int16MultiArray()

		# rospy.loginfo("Server get action %s", action.direction)

		if action.direction == "backward":
			speed_wheel.data= [-100, -100]


		if action.direction == "forward":
			speed_wheel.data= [100, 100]

		elif action.direction == "stop":
			speed_wheel.data= [0, 0]

		elif action.direction == "backward":
			speed_wheel.data= [-100, -100]

		elif action.direction == "rotate":
			if action.side == "right":
				speed_wheel.data= [100, -100]
			elif action.side == "left":
				speed_wheel.data= [-100, 100]


		speed_wheel = self.modificator_direction(speed_wheel, action)

		# rospy.loginfo(speed_wheel)

		self.change_directionToArduino(speed_wheel, action)


		self.result = setDirectionRobotResult(done = True)

		self.server.set_succeeded(self.result)









if __name__ == '__main__':
  server = serverSetDirectionRobot()
  rospy.spin()