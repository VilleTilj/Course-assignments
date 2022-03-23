import numpy as np
import matplotlib.pyplot as plt
from visualize_mobile_robot import sim_mobile_robot
from detect_obstacle import detect_obstacle_e5t2
import math

# Constants and Settings
Ts = 0.01 # Update simulation every 10ms
t_max = np.pi # total simulation duration in seconds
# Set initial state
init_state = np.array([-2., -.5, 0.]) # px, py, theta
obstacle_center_point = np.array([0., 0., 0.])
IS_SHOWING_2DVISUALIZATION = True

# Define Field size for plotting (should be in tuple)
field_x = (-2.5, 2.5)
field_y = (-2, 2)


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

    if IS_SHOWING_2DVISUALIZATION: # Initialize Plot
        sim_visualizer = sim_mobile_robot( 'omnidirectional' ) # Omnidirectional Icon
        #sim_visualizer = sim_mobile_robot( 'unicycle' ) # Unicycle Icon
        sim_visualizer.set_field( field_x, field_y ) # set plot area
        sim_visualizer.show_goal(desired_state)
        # ADD OBJECT TO PLOT
        circle_r = 0.5
        eps = 0.2
        d_safe = circle_r + eps
        sim_visualizer.ax.add_patch( plt.Circle( (0,0), circle_r, color="red"))
        sim_visualizer.ax.add_patch( plt.Circle( (0,0), circle_r, color="red",  fill=False))
        sim_visualizer.ax.add_patch( plt.Circle( (0,0), d_safe, color="green",fill=False))
 

    for it in range(sim_iter):
        # record current state at time-step t
        state_history[it] = robot_state
        goal_history[it] = desired_state

        # IMPLEMENTATION OF CONTROLLER
        #------------------------------------------------------------
        # Compute the control input 
        # TODO: change the implementation to switching
        #------------------------------------------------------------
        if np.linalg.norm(robot_state - obstacle_center_point) < d_safe:
            k = calculate_time_varying_k(desired_state, robot_state, v0=8, beta=0.5)
            current_input = k * (robot_state - obstacle_center_point)
        
        elif np.linalg.norm(robot_state - obstacle_center_point) >= d_safe + eps:
            k = calculate_time_varying_k(desired_state, robot_state, v0=12, beta=0.5)
            current_input = k * (desired_state - robot_state)
            
        # record the computed input at time-step t
        input_history[it] = current_input

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
    return state_history, goal_history, input_history


def calculate_time_varying_k(desired_state, robot_state, v0, beta):
    error = desired_state - robot_state
    return (v0 * (1 - math.exp(-beta * np.linalg.norm(error)))) / np.linalg.norm(error)


if __name__ == '__main__':
    
    # Call main computation for robot simulation
    state_history, goal_history, input_history = simulate_control()


    # ADDITIONAL PLOTTING
    #----------------------------------------------
    t = [i*Ts for i in range( round(t_max/Ts) )]

    # # Plot historical data of control input
    fig2 = plt.figure(2)
    ax = plt.gca()
    ax.plot(t, input_history[:,0], label='vx [m/s]')
    ax.plot(t, input_history[:,1], label='vy [m/s]')
    ax.plot(t, input_history[:,2], label='omega [rad/s]')
    ax.set(xlabel="t [s]", ylabel="control input")
    plt.legend()
    # plt.grid()

    # Plot historical data of state
    fig3 = plt.figure(3)
    ax = plt.gca()
    ax.plot(t, state_history[:,0], label='px [m]')
    ax.plot(t, state_history[:,1], label='py [m]')
    ax.plot(t, state_history[:,2], label='theta [rad]')
    ax.plot(t, goal_history[:,0], ':', label='goal px [m]')
    ax.plot(t, goal_history[:,1], ':', label='goal py [m]')
    ax.plot(t, goal_history[:,2], ':', label='goal theta [rad]')
    ax.set(xlabel="t [s]", ylabel="state")
    plt.legend()
    plt.grid()

    plt.show()
