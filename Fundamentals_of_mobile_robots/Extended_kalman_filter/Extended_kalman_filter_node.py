#!/usr/bin/env python
from cmath import cos, sin
from copy import copy
from operator import truediv
from time import process_time, time
from turtle import color, dot, shape
from unittest import result
from xml.dom.minidom import Element
from xmlrpc.client import Transport

from httplib2 import ProxyInfo

import rospy
from sensor_msgs.msg import JointState
from geometry_msgs.msg import PoseWithCovarianceStamped
import tf, math
import tf2_ros
from geometry_msgs.msg import Point, Pose, Quaternion, Twist, Vector3, TransformStamped
import numpy as np
import matplotlib.pyplot as plt



# init some needed values for calculations -----------------------------
prev_t = 0
prev_pos = [0, 0]
r_z = [0]
psi = [0]
delta_hat_trans = 0
delta_hat_rot1 = 0
delta_hat_rot2 = 0
epsilon_rot1 =  np.random.normal(0, 0.2)
epsilon_rot2 =  np.random.normal(0, 0.2)
epsilon_trans = np.random.normal(0, 0.2)



# Arrays for plotting later --------------------------------------------
pose_x_pred = [0]
pose_y_pred = [0]
pose_x_updated = [0]
pose_y_updated = [0]
pose_yaw_updated = [0]

x_hat_neg = [np.array(np.zeros((3,1)))]
x_hat_pos = [np.array(np.zeros((3,1)))]
time_array = [0]
covariance_array_neg = [np.zeros((3, 3))]
covariance_array_pos = [np.zeros((3, 3))]
zk = [0]
zk_hat = [0]


# global constants
L0 = [7.5, -4]
L1 = [-5, 8]
L2 = [-7, -6.5]
RK = np.diag([0.0025, 0.0025, 0.0025])


pub = rospy.Publisher('Pose', PoseWithCovarianceStamped, queue_size=10)
pose = PoseWithCovarianceStamped()
pose.header.frame_id = "Odom"


#publisher for the data

def posePub(x, cov):

    #Publishing posewithcovariance---------------------------------------
    l = cov.tolist()
    pose.header.stamp = rospy.Time.now()
    pose.pose.pose.position.x = float(x[0])
    pose.pose.pose.position.y = float(x[1])
    quat_array = tf.transformations.quaternion_from_euler(0, 0, float(x[2]))
    pose.pose.pose.orientation.x  = quat_array[0]
    pose.pose.pose.orientation.y  = quat_array[1]
    pose.pose.pose.orientation.z  = quat_array[2]
    pose.pose.pose.orientation.w  = quat_array[3]
    pose.pose.covariance[0] = l[0][0]
    pose.pose.covariance[1] = l[0][1]
    pose.pose.covariance[2] = l[0][2]
    pose.pose.covariance[3] = l[1][0]
    pose.pose.covariance[4] = l[1][1]
    pose.pose.covariance[5] = l[1][2]
    pose.pose.covariance[6] = l[2][0]
    pose.pose.covariance[7] = l[2][1]
    pose.pose.covariance[8] = l[2][2]
    pub.publish(pose)

    #Broadcasting TF---------------------------------------------------
    br = tf2_ros.TransformBroadcaster()
    t = TransformStamped()

    t.header.stamp = rospy.Time.now()
    t.header.frame_id = "Odom"
    t.child_frame_id = "robot_base_kf"
    t.transform.translation.x = pose.pose.pose.position.x
    t.transform.translation.y = pose.pose.pose.position.y
    t.transform.translation.z = 0.0
    t.transform.rotation.x = quat_array[0]
    t.transform.rotation.y = quat_array[1]
    t.transform.rotation.z = quat_array[2]
    t.transform.rotation.w = quat_array[3]

    br.sendTransform(t)

# measurement receives the information about measurements and updates the position.
def measurement(data):
    global x_hat_pos
    print("Measurement received ------------------------------------------------")

    z = np.array(np.shape((3,1)))
    
    zk_hat1 = np.sqrt(np.power((L0[0]- x_hat_neg[-1][0]), 2) + np.power(L0[1] - x_hat_neg[-1][1], 2))
    zk_hat2 = np.sqrt(np.power((L1[0] - x_hat_neg[-1][0]), 2) + np.power(L1[1] - x_hat_neg[-1][1], 2))
    zk_hat3 = np.sqrt(np.power((L2[0] - x_hat_neg[-1][0]), 2) + np.power(L2[1] - x_hat_neg[-1][2], 2))
    
    H = np.matrix([
        [2*(x_hat_neg[-1][0] - L0[0]), 2*(x_hat_neg[-1][1] - L0[1]), 0],
        [2*(x_hat_neg[-1][0] - L1[0]), 2*(x_hat_neg[-1][1] - L1[1]), 0],
        [2*(x_hat_neg[-1][0] - L2[0]), 2*(x_hat_neg[-1][1] - L2[1]), 0]
    ], dtype=float)

    # calculate error of the measurement theta
    theta_k = np.random.normal(0, RK, 1)
    zk = [data.position[0] + theta_k, data.position[1] + theta_k, data.position[2] + theta_k]
    

    Kk = covariance_array_neg[-1] @ H.getH() @ np.linalg.inv((H @ covariance_array_neg[-1] @ H.getH()) + RK)
    covariance_array_pos.append((np.eye(np.shape(covariance_array_pos[0])[0]) \
                            - Kk @ H) @ covariance_array_neg[-1])

    z = np.array([zk[0]- zk_hat1, zk[1] - zk_hat2, zk[2] - zk_hat3])
    z = z.reshape((3,1))
    x = np.array([[float(x_hat_neg[-1][0])], [float(x_hat_neg[-1][1])], [float(x_hat_neg[-1][2])]])
    x_hat_pos.append(np.add(x, Kk @ z))
    
    pose_x_updated.append(float(x_hat_neg[-1][0]))
    pose_y_updated.append(float(x_hat_neg[-1][1]))
    pose_yaw_updated.append(float(x_hat_neg[-1][2]))

    # publish results -----------------------------------------------------------------------------
    posePub(x_hat_pos[-1], covariance_array_pos[-1])


# callback is for updating the estimate of the robots location according to wheel angular velocities
def callback(data):
    global prev_t, prev_pos, r_z, delta_hat_trans, delta_hat_rot1, delta_hat_rot2, covariance_array_neg, covariance_array_pos, x_hat_pos
    print("angular velocity received ------------------------------------------------")
    wheel_radius = 0.1
    dist_bw_wheels = 0.4
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

    # calculate motion model uncertainty------------------------------

    delta_hat_trans = vx*dt
    delta_hat_rot1 = 0.5*wz*dt
    delta_hat_rot2 = 0.5*wz*dt

    delta_rot1 = delta_hat_rot1 + epsilon_rot1
    delta_rot2 = delta_hat_rot2 + epsilon_rot2
    delta_trans = delta_hat_trans + epsilon_trans

    # Calculate A, L, M and Q matrixes -------------------------------

    # for L matrix the differential equations are calculated using Matlab
    L = np.matrix([
        [math.cos(r_z[-1] + delta_rot1), -delta_trans*(r_z[-1] + delta_rot1), 0],
        [math.sin(r_z[-1] + delta_rot1), -delta_trans*(r_z[-1] + delta_rot1), 0],
        [0 , 0, 0]
    ], dtype=float)

    M = np.matrix([
        [np.power(epsilon_rot1, 2), 0, 0],
        [0, np.power(epsilon_rot2, 2), 0],
        [0, 0, np.power(epsilon_trans, 2)]
    ], dtype=float)


    A = np.matrix([
        [1, 0, -delta_trans*math.sin(delta_rot1 + r_z[-1])],
        [0, 1, delta_trans*math.cos(delta_rot1 + r_z[-1])],
        [0, 0, 1]
    ], dtype=float)

    Q = np.diag([0.001 , 0.0002, 0.0002])
    epsilon = np.random.normal(0, np.abs(Q), 1)

    # calculating predict calculations -------------------------
    
    rz_t_ = r_z[-1] + 0.5*wz*dt   #Euler midpoint

    # predicted Motion modeĺ

    x = x_hat_pos[-1][0]
    y = x_hat_pos[-1][1]
    psi = x_hat_pos[-1][2]

    x_hat_neg.append([
        x + vx * dt * math.cos(rz_t_+ 1/2 * wz * dt) + epsilon,
        y + vx * dt * math.sin(rz_t_+ 1/2 * wz * dt) + epsilon,
        psi + wz*dt + epsilon
    ])
    pose_x_pred.append(x + vx * dt * math.cos(rz_t_+ 1/2 * wz * dt) + epsilon)
    pose_y_pred.append(y + vx * dt * math.sin(rz_t_+ 1/2 * wz * dt) + epsilon)

    # covariance before update
    covariance_array_neg.append((A @ covariance_array_pos[-1] @ A.getH()) + Q)

     # publish results ------------------------------------------
    posePub(x_hat_neg[-1], covariance_array_neg[-1])
    
def wheel_odometry():

    rospy.init_node('wheel_odometry', anonymous=True)
    rospy.Subscriber("/joint_states", JointState, callback)
    rospy.loginfo("Extended Kalman filter started!")
    rospy.Subscriber("/Landmark_dist", JointState, measurement)
    rospy.spin()

    plt.figure(1)
    plt.plot(pose_x_pred, pose_y_pred, label='Predicted pose')
    plt.plot(pose_x_updated, pose_y_updated, label='Updated pose')
    
    plt.scatter(L0[0], L0[1], label='Landmark 1')
    plt.scatter(L1[0], L1[1], label='Landmark 2')
    plt.scatter(L2[0], L2[1], label='Landmark 3')
    plt.xlabel("Robot body x-coordinate")
    plt.ylabel("Robot body y-coordinate")

    plt.legend()

    plt.figure(2)
    plt.plot(pose_x_updated, time_array, label='X-plot')
    plt.plot(pose_y_updated, time_array, label='Y-plot')
    plt.plot(pose_yaw_updated, time_array, label='Yaw-plot')
    plt.xlabel('Plot values')
    plt.ylabel('Time: (s)')
    plt.legend()
    plt.show()


if __name__ == '__main__':
    wheel_odometry()