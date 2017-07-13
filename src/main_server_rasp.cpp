#include "ros/ros.h"

#include "std_msgs/String.h"
#include "std_msgs/Int16.h"
#include "project_buggy/SpeedMotors.h"
#include "std_msgs/Int16MultiArray.h"
#include "std_msgs/MultiArrayDimension.h"
#include "std_msgs/MultiArrayLayout.h"

bool autonomus = false;
bool speed_modified = true;

project_buggy::SpeedMotors speed_motors;



void setSpeed(const project_buggy::SpeedMotors& msg){
	speed_modified = true;
	speed_motors = msg;
}



void speed_from_socket_cb(const project_buggy::SpeedMotors& msg){
	ROS_INFO("ACTION");
	setSpeed(msg);
}

void speed_from_action_cb(const project_buggy::SpeedMotors& msg){
	ROS_INFO("ACTION");
	setSpeed(msg);
}




int main(int argc, char **argv)
{

	ros::init(argc, argv, "main");
	ros::NodeHandle n;

	ros::Publisher send_toArduino = n.advertise<std_msgs::Int16MultiArray&>("speed_motor_arduino", 1000);


	ros::Subscriber speed_from_socket = n.subscribe("speed_from_socket", 1000, speed_from_socket_cb);
	ros::Subscriber speed_from_action = n.subscribe("get_speed_from_server", 1000, speed_from_action_cb);


	ros::Rate loop_rate(1);



	// Init 
	speed_motors = project_buggy::SpeedMotors();
	speed_motors.speed_right_motor = 0;
	speed_motors.speed_left_motor = 0;

	while (ros::ok())
	{
		if(speed_modified){
			ROS_INFO("Speed: [%d] - [%d] -  Mode: %i", speed_motors.speed_right_motor, speed_motors.speed_left_motor, autonomus);

			std_msgs::Int16MultiArray speed = std_msgs::Int16MultiArray();
			speed.data.clear();
			speed.data.push_back(speed_motors.speed_right_motor);
			speed.data.push_back(speed_motors.speed_left_motor);


			send_toArduino.publish(speed);
			speed_modified = false;
		}

		ros::spinOnce();


		loop_rate.sleep();

	}


	return 0;
}
// %EndTag(FULLTEXT)%
