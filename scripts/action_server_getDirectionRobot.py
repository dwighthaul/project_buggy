#! /usr/bin/env python

import roslib
import rospy
import actionlib
import time

from project_buggy.msg import SpeedMotors

from slam_project_buggy.msg import setDirectionRobotAction, setDirectionRobotResult
from std_msgs.msg import Int16MultiArray, MultiArrayDimension, MultiArrayLayout


secs = 2

class serverSetDirectionRobot:


	buffer_speed_wheel = [0, 0]



	def __init__(self):
		rospy.init_node('set_direction')

		self.server = actionlib.SimpleActionServer('set_direction', setDirectionRobotAction, self.execute, False)
		self.pub = rospy.Publisher('get_speed_from_server', SpeedMotors, queue_size=10)

		self.server.start()
		rospy.loginfo("Server started")





	def change_direction(self, speed_wheel, action):

		self.publishSpeed(speed_wheel)
		time.sleep(secs)


		if action.backToPrevious:
			rospy.loginfo("Back to previous")
			self.publishSpeed(self.buffer_speed_wheel)


	def modificator_direction(self, speed_wheel, action):
		speed_wheel = [speed_wheel[0]*2.20, speed_wheel[1]*2.20]
		rospy.loginfo("Final Speed %s - %s", speed_wheel[0], speed_wheel[1])
		return speed_wheel


	def publishSpeed(self, speed_wheel):
		speedArray = SpeedMotors()
		speedArray.speeds = speed_wheel
		speedArray.data_bool = False

		self.pub.publish(speedArray)




	def execute(self, action):


		speed_wheel= [0, 0]

		rospy.loginfo("Server get action %s", action.direction)

		if action.direction == "backward":
			speed_wheel= [-100, -100]


		if action.direction == "forward":
			speed_wheel= [100, 100]

		elif action.direction == "stop":
			speed_wheel= [0, 0]

		elif action.direction == "backward":
			speed_wheel= [-100, -100]

		elif action.direction == "rotate":
			if action.side == "right":
				speed_wheel= [100, -100]
			elif action.side == "left":
				speed_wheel= [-100, 100]



		speed_wheel = self.modificator_direction(speed_wheel, action)

		self.change_direction(speed_wheel, action)






		self.result = setDirectionRobotResult(done = True)

		self.server.set_succeeded(self.result)









if __name__ == '__main__':
  server = serverSetDirectionRobot()
  rospy.spin()