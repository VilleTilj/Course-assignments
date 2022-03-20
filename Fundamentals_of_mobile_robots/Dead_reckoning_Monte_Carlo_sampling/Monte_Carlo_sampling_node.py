#!/usr/bin/env python
from copy import copy
from turtle import color
import rospy
from sensor_msgs.msg import JointState
from nav_msgs.msg import Odometry
import tf, math
import tf2_ros
from geometry_msgs.msg import Point, Pose, Quaternion, Twist, Vector3, TransformStamped
import numpy as np
import matplotlib.pyplot as plt


class Sample_simulation:
    __slots__ = ['a1', 'a2', 'a3', 'a4', 'x_sampled', 'y_sampled']

    def __init__(self) -> None:
        # Parameters for dead-reckoning uncertaintymodel
        self.a1, self.a2, self.a3, self.a4 = 50, 5, 70, 10

        # Initialize maps to simulate 100 particles for Monte Carlo sampling
        self.x_sampled = {}
        self.y_sampled = {}
        [self.x_sampled.setdefault(i, [0]) for i in range(100)]
        [self.y_sampled.setdefault(i, [0]) for i in range(100)]

    def monte_carlo_sampling(self, vx, dt, wz, rz_t_):
        # Calculate sampling motion model parameters from lecture slides
        delta_hat_trans = vx*dt
        delta_hat_rot1 = 0.5 * wz*dt
        delta_hat_rot2 = copy(delta_hat_rot1)
        xrot1 = self.a1 * np.power(delta_hat_rot1,2) + self.a2 * np.power(delta_hat_rot2,2)
        xtrans = self.a3 * np.power(delta_hat_trans,2) + self.a4 * (np.power(delta_hat_rot1,2) + np.power(delta_hat_rot2,2))

        # Simulate all 100 robots and use their previous simulation iteration value to simulate new pose
        for i in range(len(self.x_sampled)):
            delta_rot1 = delta_hat_rot1 + np.random.normal(0, xrot1) 
            delta_trans = delta_hat_trans + np.random.normal(0, xtrans)
            xrot2 = self.a1 * np.power(delta_hat_rot2,2) + self.a2 * np.power(delta_hat_trans,2)
            delta_rot2 = delta_hat_rot2 + np.random.normal(0, xrot2)

            self.x_sampled[i].append(self.x_sampled[i][-1] + delta_trans * math.cos(rz_t_ + delta_rot1))
            self.y_sampled[i].append(self.y_sampled[i][-1]+ delta_trans * math.sin(rz_t_ + delta_rot1))



prev_t = 0
prev_pos = [0, 0]
r_z = 0

position_array = []
time_array = []
psi = [0]
x_t_forward = [0]
y_t_forward = [0]
x_t_midpoint = [0]
y_t_midpoint = [0]


pub = rospy.Publisher('odometry', Odometry, queue_size=10)
odom = Odometry()
odom.header.frame_id = "Odom"
odom.child_frame_id = "robot_base"

simulation = Sample_simulation()

def callback(data, ):
    global prev_t, prev_pos, r_z
    wheel_radius = 0.1
    dist_bw_wheels = 0.4
    mid_point = True
    t = data.header.stamp.to_sec()
    time_array.append(t)
    dt = t - prev_t
    prev_t = t
    

    # Calculating robot velocity--------------------------------------

    pos = data.position
    right_vel = (pos[0] - prev_pos[0])/dt
    left_vel = (pos[1] - prev_pos[1])/dt
    prev_pos = pos
    vr = wheel_radius*right_vel
    vl = wheel_radius*left_vel
    vx = 0.5*(vr + vl)
    wz = (1/dist_bw_wheels)*(vr - vl)


    # Updating odometry-----------------------------------------------

    if mid_point:
        rz_t_ = r_z + 0.5*wz*dt   #Euler midpoint
    else:
        rz_t_ = r_z               #Euler forward

    odom.header.stamp = data.header.stamp
    odom.pose.pose.position.x = odom.pose.pose.position.x + vx*dt*math.cos(rz_t_)
    odom.pose.pose.position.y = odom.pose.pose.position.y + vx*dt*math.sin(rz_t_)
    
    x_t_forward.append(x_t_forward[-1] + vx * dt * math.cos(rz_t_))
    y_t_forward.append(y_t_forward[-1] + vx * dt * math.sin(rz_t_))

    x_t_midpoint.append(x_t_midpoint[-1] + vx * dt * math.cos(rz_t_+ 1/2 * wz * dt))
    y_t_midpoint.append(y_t_midpoint[-1] + vx * dt * math.sin(rz_t_+ 1/2 * wz * dt))



    r_z = r_z + wz*dt
    quat_array = tf.transformations.quaternion_from_euler(0, 0, r_z)
    
    odom.pose.pose.orientation.x  = quat_array[0]
    odom.pose.pose.orientation.y  = quat_array[1]
    odom.pose.pose.orientation.z  = quat_array[2]
    odom.pose.pose.orientation.w  = quat_array[3]
    odom.twist.twist = Twist(Vector3(vx, 0, 0), Vector3(0, 0, wz))
    pub.publish(odom)


    # Monte Carlo sampling -----------------------------------------------
    simulation.monte_carlo_sampling(vx, dt, wz, rz_t_)

    #Broadcasting TF---------------------------------------------------
    br = tf2_ros.TransformBroadcaster()
    t = TransformStamped()

    t.header.stamp = rospy.Time.now()
    t.header.frame_id = "Odom"
    t.child_frame_id = "robot_base"
    t.transform.translation.x = odom.pose.pose.position.x
    t.transform.translation.y = odom.pose.pose.position.y
    t.transform.translation.z = 0.0
    t.transform.rotation.x = quat_array[0]
    t.transform.rotation.y = quat_array[1]
    t.transform.rotation.z = quat_array[2]
    t.transform.rotation.w = quat_array[3]

    br.sendTransform(t)
    rospy.loginfo("Publishing odometry and TF.....................")

    
def wheel_odometry():
    rospy.init_node('wheel_odometry', anonymous=True)

    rospy.Subscriber("/joint_states", JointState, callback)
    rospy.loginfo("wheel_odometry started!")
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

    # Plot the Euler forward and midpoint curves
    plt.plot(x_t_forward, y_t_forward, label="Forward Euler")
    plt.plot(x_t_midpoint, y_t_midpoint, label="midpoint Euler")
    plt.xlabel("Robot body x-coordinate")
    plt.ylabel("Robot body y-coordinate")

    # Init point datastructures for showing Monte Carlo sampling from the 100 simulations
    xPoints = {100: [], 300: [], 500: [], 700: [], 900: []}
    yPoints = {100: [], 300: [], 500: [], 700: [], 900: []}
    for index in range(len(simulation.x_sampled)):
        for point in range(len(simulation.x_sampled[index])):
            if point in xPoints:
                # Append points if the sequence of the simulation is wanted one for the sampling
                xPoints[point].append(simulation.x_sampled[index][point])
                yPoints[point].append(simulation.y_sampled[index][point])
    
    # Plot Monte Carlo sampling points
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',]
    for i, point in enumerate(xPoints):
        plt.scatter(xPoints[point],yPoints[point], color=colors[i], s = 4)
        plt.legend()
    plt.show()


if __name__ == '__main__':
    wheel_odometry()