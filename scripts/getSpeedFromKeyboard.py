#!/usr/bin/env python
import roslib; roslib.load_manifest('teleop_twist_keyboard')
import rospy

from geometry_msgs.msg import Twist

import sys, select, termios, tty
from slam_project_buggy.msg import setDirectionRobotAction, setDirectionRobotGoal
from actionlib import SimpleActionClient


# direction_dir = keyPossible[key][0]
# angle_dir = keyPossible[key][1]
# side_dir = keyPossible[key][2]
# backToPrevious_dir = keyPossible[key][3]

class SendActionKeyboard():
    """docstring for SendActionKeyboard"""
    instructions = """
        Reading from the keyboard  and Publishing to Twist!
        ---------------------------
        Moving around:
           7    8    9
           4    5    6
           1    2    3

        ---------------------------

    """

    keyPossible = {
            '1':("backward", 40,"left",True),
            '2':("backward", 0,"",True),
            '3':("backward", 40, "right", True),

            '4':("rotate", 90, "left", True),
            '5':("stop",    0, "", False),
            '6':("rotate", 90, "right", True),

            '7':("forward", 40, "left",True),
            '8':("forward", 0, "", True),
            '9':("forward", 40, "right", True),
               }



    def __init__(self):
        print(self.instructions)
        self.settings = termios.tcgetattr(sys.stdin)
        
        rospy.init_node('send_action_from_keyboard')

        rospy.loginfo('Init Client')
        self.client = SimpleActionClient('speed_from_action', setDirectionRobotAction)

        self.client.wait_for_server()

        direction_dir = ""
        angle_dir = 0
        side_dir = ""
        backToPrevious_dir = True

        try:

            while(1):
                key = self.getKey()
                # if control-C stop
                if (key == '\x03'):
                    break


                if key in self.keyPossible.keys():
                    direction_dir = self.keyPossible[key][0]
                    angle_dir = self.keyPossible[key][1]
                    side_dir = self.keyPossible[key][2]
                    backToPrevious_dir = self.keyPossible[key][3]

                    print(direction_dir,angle_dir, side_dir, backToPrevious_dir)


                    action = setDirectionRobotGoal(direction = direction_dir, angle= angle_dir, side=side_dir, backToPrevious=backToPrevious_dir)

                    self.sendDirection(action)


                # print("print")
                # pub.publish(twist)

        except Exception as e:
            print e


        


    def sendDirection(self, action):

        self.client.send_goal(action)

        self.client.wait_for_result()

        retour = self.client.get_result()
        rospy.loginfo('Get result %s', retour)


    def getKey(self):
        tty.setraw(sys.stdin.fileno())
        select.select([sys.stdin], [], [], 0)
        key = sys.stdin.read(1)
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.settings)
        return key



if __name__=="__main__":
    SendActionKeyboard()
