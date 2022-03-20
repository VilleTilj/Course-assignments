import numpy as np
import matplotlib.pyplot as plt
from visualize_mobile_robot import sim_mobile_robot
import math

# Constants and Settings
Ts = 0.01 # Update simulation every 10ms
t_max = np.pi # total simulation duration in seconds
# Set initial state
init_state = np.array([0., 0., 0.]) # px, py, theta
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
    # Initialize robot's state simulation for k values 2 and 3.

    desired_state = np.array([math.cos(2*Ts), math.sin(2*Ts), 0]) # numpy array for goal / the desired [px, py, theta]
    current_input = np.array([0., 0., 0.]) # initial numpy array for [vx, vy, omega]

    # Store the value that needed for plotting: total step number x data length
    # Init state and input histories to 3 different simulations 
    state_history = np.zeros( (sim_iter, len(robot_state)) ) 
    goal_history = np.zeros( (sim_iter, len(desired_state)) ) 
    input_history = np.zeros( (sim_iter, len(current_input)) ) 
    error_history = np.zeros( (sim_iter, len(current_input)) ) 

    if IS_SHOWING_2DVISUALIZATION: # Initialize Plot
        sim_visualizer = sim_mobile_robot( 'omnidirectional' ) # Omnidirectional Icon
        #sim_visualizer = sim_mobile_robot( 'unicycle' ) # Unicycle Icon
        sim_visualizer.set_field( field_x, field_y ) # set plot area
        sim_visualizer.show_goal(desired_state)

    for it in range(sim_iter):
        desired_state = np.array([math.cos(2*Ts*it), math.sin(2*Ts*it), 0])
        # record current state at time-step t with all simulation cases
        state_history[it] = robot_state
        goal_history[it] = desired_state

        # IMPLEMENTATION OF CONTROLLER
        #------------------------------------------------------------
        # Compute the control input
        k, error_history[it] = calculate_time_varying_k(desired_state, robot_state, v0=5, beta=1)
        dx = np.array([-2*math.sin(2* Ts* it), 2*math.cos(2*Ts*it), 0])
        current_input = k * (desired_state - robot_state) + dx
        #------------------------------------------------------------

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

        # Update desired state if we consider moving goal position
        #desired_state = desired_state + Ts*(-1)*np.ones(len(robot_state))

    # End of iterations
    # ---------------------------
    # return the stored value for additional plotting or comparison of parameters
    return state_history, goal_history, input_history, error_history


def calculate_time_varying_k(desired_state, robot_state, v0, beta):
    error = desired_state - robot_state
    return (v0 * (1 - math.exp(-beta * np.linalg.norm(error)))) / np.linalg.norm(error), error


if __name__ == '__main__':
    
    # Call main computation for robot simulation
    state_history, goal_history, input_history, error_history = simulate_control()


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
    plt.grid()

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

    # Plot 3 different simulations poses
    fig4 = plt.figure(4)
    ax = plt.gca()
    ax.plot(t, state_history[:,0], label='px, v0=5, beta=0.5 [m]')
    ax.plot(t, state_history[:,1], label='py, v0=5, beta=0.5 [m]')
    ax.plot(t, state_history[:,2], label='theta, v0=5, beta=0.5 [rad]')
    ax.plot(t, goal_history[:,0], ':', label='goal px [m]')
    ax.plot(t, goal_history[:,1], ':', label='goal py [m]')
    ax.plot(t, goal_history[:,2], ':', label='goal theta [rad]')
    ax.set(xlabel="t [s]", ylabel="state")
    plt.legend()
    plt.grid()

    # Plot 3 different simulations velocities
    fig2 = plt.figure(5)
    ax = plt.gca()
    ax.plot(t, input_history[:,0], label='vx, v0=5, beta=1.0 [m/s]')
    ax.plot(t, input_history[:,1], label='vy, v0=5, beta=1.0 [m/s]')
    ax.plot(t, input_history[:,2], label='omega, v0=5, beta=1.0 [rad/s]')
    ax.set(xlabel="t [s]", ylabel="control input")
    plt.legend()
    plt.grid()

    fig4 = plt.figure(6)
    ax = plt.gca()
    ax.plot(t, error_history[:, 0], label="error vx [m/s]")
    ax.plot(t, error_history[:, 1], label="error vy [m/s]")
    ax.plot(t, error_history[:, 2], label="error omega [ras/s]")
    ax.set(xlabel="t [s]", ylabel="state")
    plt.legend()
    plt.grid()

    plt.show()
