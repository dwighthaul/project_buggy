#include "ros/ros.h"

#include "std_msgs/String.h"
#include "std_msgs/Int16.h"
#include "project_buggy/SpeedMotors.h"
#include "std_msgs/Int16MultiArray.h"
#include "std_msgs/MultiArrayDimension.h"
#include "std_msgs/MultiArrayLayout.h"

bool autonomus = false;
std_msgs::Int16MultiArray speed_motor;


void get_speed_from_random(const std_msgs::Int16MultiArray& msg){
	// ROS_INFO("GET_DATA_FROM_RANDOM [%d] - [%d]", msg.data[0], msg.data[1]);
	if(autonomus) {
//		speed_motor = msg;
	}
}

void get_speed_from_server(const project_buggy::SpeedMotors& msg){
	autonomus = msg.data_bool;

	// ROS_INFO("GET_DATA_FROM_PHONE [%d] - [%d] - %i", msg.data[0], msg.data[1], msg.data_bool);
	if(!autonomus) {
		speed_motor.data.clear();
		speed_motor.data.push_back(msg.speeds[0]);
		speed_motor.data.push_back(msg.speeds[1]);
	}
}

int main(int argc, char **argv)
{

	ros::init(argc, argv, "main");
	ros::NodeHandle n;

	ros::Publisher chatter_pub_main = n.advertise<std_msgs::Int16MultiArray&>("speed_motor_arduino", 1000);


	ros::Subscriber get_speed_from_openCV_sub = n.subscribe("get_speed_from_random", 1000, get_speed_from_random);
	ros::Subscriber get_speed_from_phone_sub = n.subscribe("get_speed_from_server", 1000, get_speed_from_server);


	ros::Rate loop_rate(1);



	// Init 

	speed_motor.data.clear();
	speed_motor.data.push_back(0);
	speed_motor.data.push_back(0);

	while (ros::ok())
	{

		ROS_INFO("Speed: [%d] - [%d] -  Mode: %i", speed_motor.data[0], speed_motor.data[1], autonomus);

		chatter_pub_main.publish(speed_motor);

		ros::spinOnce();

		loop_rate.sleep();

	}


	return 0;
}
// %EndTag(FULLTEXT)%
