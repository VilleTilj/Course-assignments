import numpy as np
import matplotlib.pyplot as plt
from visualize_mobile_robot import sim_mobile_robot
from detect_obstacle import detect_obstacle_e5t2
import math
import cvxopt

# Constants and Settings
Ts = 0.01 # Update simulation every 10ms
t_max = np.pi * 10 # total simulation duration in seconds
# Set initial state
init_state = np.array([-2., -1.0, 0.]) # px, py, theta
obstacle_center_point = np.array([-0.6, 0., 0.])
obstacle_center_point_2 = np.array([0.6, 0., 0.])
IS_SHOWING_2DVISUALIZATION = True

# Define Field size for plotting (should be in tuple)
field_x = (-2.5, 2.5)
field_y = (-2, 2)
RSI = 0.51

# MAIN SIMULATION COMPUTATION
#---------------------------------------------------------------------
def simulate_control():
    sim_iter = round(t_max/Ts) # Total Step for simulation

    # Initialize robot's state (Single Integrator)
    robot_state = init_state.copy() # numpy array for [px, py, theta]
    desired_state = np.array([2., 1., 0.]) # numpy array for goal / the desired [px, py, theta]
    current_input = np.array([0., 0., 0.]) # initial numpy array for [vx, vy, omega]

    # Store the value that needed for plotting: total step number x data length
    state_history = np.zeros( (sim_iter, len(robot_state)) ) 
    goal_history = np.zeros( (sim_iter, len(desired_state)) ) 
    input_history = np.zeros( (sim_iter, len(current_input)) ) 
    input_gtg_history = np.zeros((sim_iter, len(current_input)))
    h1_history = np.zeros((sim_iter, len(current_input)))
    h2_history = np.zeros((sim_iter, len(current_input)))


    if IS_SHOWING_2DVISUALIZATION: # Initialize Plot
        sim_visualizer = sim_mobile_robot( 'omnidirectional' ) # Omnidirectional Icon
        #sim_visualizer = sim_mobile_robot( 'unicycle' ) # Unicycle Icon
        sim_visualizer.set_field( field_x, field_y ) # set plot area
        sim_visualizer.show_goal(desired_state)
        # ADD OBJECT TO PLOT
        circle_r = 0.3
        eps = 0.2
        d_safe = circle_r + eps
        sim_visualizer.ax.add_patch( plt.Circle( (-0.6, 0), circle_r, color="red"))
        sim_visualizer.ax.add_patch( plt.Circle( (-0.6, 0), circle_r, color="red",  fill=False))
        sim_visualizer.ax.add_patch( plt.Circle( (-0.6, 0), d_safe, color="green",fill=False))

        sim_visualizer.ax.add_patch( plt.Circle( (0.6, 0), circle_r, color="red"))
        sim_visualizer.ax.add_patch( plt.Circle( (0.6, 0), circle_r, color="red",  fill=False))
        sim_visualizer.ax.add_patch( plt.Circle( (0.6, 0), d_safe, color="green",fill=False))

    for it in range(sim_iter):
        # record current state at time-step t
        state_history[it] = robot_state
        goal_history[it] = desired_state

        # IMPLEMENTATION OF CONTROLLER
        #------------------------------------------------------------
        # Compute the control input 
        # TODO: change the implementation to switching
        #------------------------------------------------------------
        k = calculate_time_varying_k(desired_state, robot_state, v0=0.6, beta=0.5)
        u_gtg = k * (desired_state - robot_state)

        # QP-based controller 
        Q_mat = 2 * cvxopt.matrix( np.eye(2), tc='d')
        c_mat = -2 * cvxopt.matrix( u_gtg[:2], tc='d')

        h1 = np.power(np.linalg.norm(robot_state - obstacle_center_point), 2) - np.power(RSI, 2)
        h2 = np.power(np.linalg.norm(robot_state - obstacle_center_point_2), 2) - np.power(RSI, 2)
        h = np.concatenate(([h1], [h2]))
        temp = np.concatenate(([robot_state[:2] - obstacle_center_point[:2]], [robot_state[:2] - obstacle_center_point_2[:2]]), axis=0)
        H = cvxopt.matrix(-2*(temp))
        # Lambda variable, 0.2 value rotates to the right of both patterns
        #y = 0.2
        #b = cvxopt.matrix(y*h)
        # Lambda = 10 goes between the two balls. 
        #y = 10
        #b = cvxopt.matrix(y*h)
        # Lambda = 100 and h^3 goes between the two balls more carefully and not touching the safe zones. 
        y = 100
        b = cvxopt.matrix(y*np.power(h,3))

        H_mat = cvxopt.matrix(H, tc='d')
        b_mat = cvxopt.matrix(b, tc='d')

        cvxopt.solvers.options['show_progress'] = False
        sol = cvxopt.solvers.qp(Q_mat, c_mat, H_mat, b_mat, verbose=False)
        
        current_input = np.array([sol['x'][0], sol['x'][1], 0])

        # record the computed input at time-step t
        input_history[it] = current_input
        input_gtg_history[it] = u_gtg
        h1_history[it] = h1
        h2_history[it] = h2

        if IS_SHOWING_2DVISUALIZATION: # Update Plot
            sim_visualizer.update_time_stamp( it*Ts )
            sim_visualizer.update_goal( desired_state )
            sim_visualizer.update_trajectory( state_history[:it+1] ) # up to the latest data
        
        #--------------------------------------------------------------------------------
        # Update new state of the robot at time-step t+1
        # using discrete-time model of single integrator dynamics for omnidirectional robot
        robot_state = robot_state + Ts*current_input # will be used in the next iteration
        robot_state[2] = ( (robot_state[2] + np.pi) % (2*np.pi) ) - np.pi # ensure theta within [-pi pi]

    # End of iterations
    # ---------------------------
    # return the stored value for additional plotting or comparison of parameters
    return state_history, goal_history, input_history, input_gtg_history, h1_history, h2_history


def calculate_time_varying_k(desired_state, robot_state, v0, beta):
    error = desired_state - robot_state
    return (v0 * (1 - math.exp(-beta * np.linalg.norm(error)))) / np.linalg.norm(error)


if __name__ == '__main__':
    
    # Call main computation for robot simulation
    state_history, goal_history, input_history, input_gtg_history, h1_history, h2_history = simulate_control()


    # ADDITIONAL PLOTTING
    #----------------------------------------------
    t = [i*Ts for i in range( round(t_max/Ts) )]

    # # Plot historical data of control input
    fig2 = plt.figure(2)
    ax = plt.gca()
    ax.plot(t, input_history[:,0], label='vx [m/s]')
    ax.plot(t, input_history[:,1], label='vy [m/s]')
    ax.plot(t, input_gtg_history[:,0], label='vx go to goal [m/s]')
    ax.plot(t, input_gtg_history[:,1], label='vy  go to goal [m/s]')
    ax.set(xlabel="t [s]", ylabel="control input")
    plt.legend()
    # plt.grid()

    fig3 = plt.figure(3)
    ax = plt.gca()
    ax.plot(t, h1_history[:,0], label='h1')
    ax.plot(t, h2_history[:,0], label='h2')
    ax.set(xlabel="t [s]", ylabel="h")
    plt.legend()
    # plt.grid()

    plt.show()