#! /usr/bin/env python
from cProfile import label
import math
from time import time
import rospy
import tf
from sensor_msgs.msg import JointState
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Point, Pose, Quaternion, Twist, Vector3
import matplotlib.pyplot as plt


position_array = []
time_array = []
psi = [0]
x_t_forward = [0]
y_t_forward = [0]
x_t_midpoint = [0]
y_t_midpoint = [0]
R = 0.1
D = 0.4


rospy.init_node('odometry_publisher')

odom_pub = rospy.Publisher("odom", Odometry, queue_size=50)
odom_broadcaster = tf.TransformBroadcaster()



def callback(data):
    rospy.loginfo(data.position[0])
    


def get_pos(data):

    # Get positions of the wheels and save to array
    right_hinge = data.position[0]
    left_hinge = data.position[1]
    position_array.append( (right_hinge, left_hinge) )
    
    # Get time of the point and save to array
    second = int(data.header.stamp.secs)
    nsecond = int(data.header.stamp.nsecs)
    T = second + (nsecond * 10**(-9))
    time_array.append(T)

    if len(position_array) == 2:
        delta_time = (time_array[1]-time_array[0]) 
        # Calculate wheels angular velocities
        right_ginge_ang_vel = (position_array[1][0] - position_array[0][0]) / delta_time
        left_ginge_ang_vel = (position_array[1][1] - position_array[0][1]) / delta_time
        
        # Calculate wheel velocities
        vel_r = R * right_ginge_ang_vel
        vel_l = R * left_ginge_ang_vel

        # Calculate robot's body linear and angular speed (twist)
        body_vel_x = 1/2 * (vel_r + vel_l)
        body_twist_w_z = 1/D * (vel_r - vel_l)

        # Calculate pose trajectory with forward euler and euler midpoint 
        x_t_forward.append(x_t_forward[-1] + body_vel_x * delta_time * math.cos(psi[-1]))
        y_t_forward.append(y_t_forward[-1] + body_vel_x * delta_time * math.sin(psi[-1]))

        x_t_midpoint.append(x_t_midpoint[-1] + body_vel_x * delta_time * math.cos(psi[-1]+ 1/2 * body_twist_w_z * delta_time))
        y_t_midpoint.append(y_t_midpoint[-1] + body_vel_x * delta_time * math.sin(psi[-1]+ 1/2 * body_twist_w_z * delta_time))

        psi.append(psi[-1] + body_twist_w_z * delta_time)



        # Create odometry
        odom_quat = (0,0,0,psi[-1])

        # first, we'll publish the transform over tf
        odom_broadcaster.sendTransform(
            (x_t_forward[-1], y_t_forward[-1], 0.),
            odom_quat,
            data.header.stamp,
            "robot_base",
            "Odom"
        )

        # next, we'll publish the odometry message over ROS
        odom = Odometry()
        odom.header.stamp.secs = int(time_array[1])
        odom.header.stamp.nsecs = data.header.stamp.nsecs
        odom.header.frame_id = "Odom"

        # set the position
        odom.pose.pose = Pose(Point(x_t_forward[-1], y_t_forward[-1], 0.), Quaternion(0,0,0, psi[-1]))

        # set the velocity
        odom.child_frame_id = "robot_base"
        odom.twist.twist = Twist(Vector3(body_vel_x, 0, 0), Vector3(0, 0, psi[-1]))

        # publish the message
        odom_pub.publish(odom)


        # Delete the first element in the arrays because they are not needed
        position_array.pop(0)
        time_array.pop(0)



def listener():    
    rospy.Subscriber("joint_states", JointState, get_pos)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

    plt.plot(x_t_forward, y_t_forward, label="Forward Euler")
    plt.plot(x_t_midpoint, y_t_midpoint, label="midpoint Euler")
    plt.xlabel("Robot body x-coordinate")
    plt.ylabel("Robot body y-coordinate")
    plt.legend()
    plt.show()


if __name__ == '__main__':
    listener()