import numpy as np
import matplotlib.pyplot as plt
from visualize_mobile_robot import sim_mobile_robot

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
    robot_state2 = init_state.copy()
    robot_state3 = init_state.copy()
    desired_state = np.array([2., 2., 0.]) # numpy array for goal / the desired [px, py, theta]
    current_input = np.array([0., 0., 0.]) # initial numpy array for [vx, vy, omega]

    # Store the value that needed for plotting: total step number x data length
    # Init state and input histories to 3 different simulations 
    state_history = np.zeros( (sim_iter, len(robot_state)) ) 
    state_history2 = np.zeros( (sim_iter, len(robot_state)) )
    state_history3 = np.zeros( (sim_iter, len(robot_state)) )
    goal_history = np.zeros( (sim_iter, len(desired_state)) ) 
    input_history = np.zeros( (sim_iter, len(current_input)) ) 
    input_history2 = np.zeros( (sim_iter, len(current_input)) ) 
    input_history3 = np.zeros( (sim_iter, len(current_input)) ) 

    if IS_SHOWING_2DVISUALIZATION: # Initialize Plot
        sim_visualizer = sim_mobile_robot( 'omnidirectional' ) # Omnidirectional Icon
        #sim_visualizer = sim_mobile_robot( 'unicycle' ) # Unicycle Icon
        sim_visualizer.set_field( field_x, field_y ) # set plot area
        sim_visualizer.show_goal(desired_state)

    for it in range(sim_iter):
        # record current state at time-step t with all simulation cases
        state_history[it] = robot_state
        state_history2[it] = robot_state2
        state_history3[it] = robot_state3
        goal_history[it] = desired_state

        # IMPLEMENTATION OF CONTROLLER
        #------------------------------------------------------------
        # Compute the control input
        k = 1
        current_input = k * (desired_state - robot_state)

        k2 = 2
        current_input2 = k2 * (desired_state - robot_state2)

        k3 = 3
        current_input3 = k3 * (desired_state - robot_state3)
        #------------------------------------------------------------

        # record the computed input at time-step t
        input_history[it] = current_input
        input_history2[it] = current_input2
        input_history3[it] = current_input3

        if IS_SHOWING_2DVISUALIZATION: # Update Plot
            sim_visualizer.update_time_stamp( it*Ts )
            sim_visualizer.update_goal( desired_state )
            sim_visualizer.update_trajectory( state_history[:it+1] ) # up to the latest data
        
        #--------------------------------------------------------------------------------
        # Update new state of the robot at time-step t+1
        # using discrete-time model of single integrator dynamics for omnidirectional robot
        robot_state = robot_state + Ts*current_input # will be used in the next iteration
        robot_state[2] = ( (robot_state[2] + np.pi) % (2*np.pi) ) - np.pi # ensure theta within [-pi pi]

        robot_state2 = robot_state2 + Ts*current_input2 # will be used in the next iteration
        robot_state2[2] = ( (robot_state2[2] + np.pi) % (2*np.pi) ) - np.pi # ensure theta within [-pi pi]

        robot_state3 = robot_state3 + Ts*current_input3 # will be used in the next iteration
        robot_state3[2] = ( (robot_state3[2] + np.pi) % (2*np.pi) ) - np.pi # ensure theta within [-pi pi]

        # Update desired state if we consider moving goal position
        #desired_state = desired_state + Ts*(-1)*np.ones(len(robot_state))

    # End of iterations
    # ---------------------------
    # return the stored value for additional plotting or comparison of parameters
    return state_history, state_history2, state_history3, goal_history, input_history, input_history2, input_history3


if __name__ == '__main__':
    
    # Call main computation for robot simulation
    state_history, state_history2, state_history3, goal_history, input_history, input_history2, input_history3 = simulate_control()


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
    ax.plot(t, state_history[:,0], label='px k=1 [m]')
    ax.plot(t, state_history[:,1], label='py k=1 [m]')
    ax.plot(t, state_history[:,2], label='theta k=1 [rad]')
    ax.plot(t, state_history2[:,0], label='px k=2 [m]')
    ax.plot(t, state_history2[:,1], label='py k=2 [m]')
    ax.plot(t, state_history2[:,2], label='theta k=2 [rad]')
    ax.plot(t, state_history3[:,0], label='px k=3 [m]')
    ax.plot(t, state_history3[:,1], label='py k=3 [m]')
    ax.plot(t, state_history3[:,2], label='theta k=3 [rad]')
    ax.plot(t, goal_history[:,0], ':', label='goal px [m]')
    ax.plot(t, goal_history[:,1], ':', label='goal py [m]')
    ax.plot(t, goal_history[:,2], ':', label='goal theta [rad]')
    ax.set(xlabel="t [s]", ylabel="state")
    plt.legend()
    plt.grid()

    # Plot 3 different simulations velocities
    fig2 = plt.figure(5)
    ax = plt.gca()
    ax.plot(t, input_history[:,0], label='vx k=1 [m/s]')
    ax.plot(t, input_history[:,1], label='vy k=1 [m/s]')
    ax.plot(t, input_history[:,2], label='omega k=1 [rad/s]')
    ax.plot(t, input_history2[:,0], label='vx k=2 [m/s]')
    ax.plot(t, input_history2[:,1], label='vy k=2 [m/s]')
    ax.plot(t, input_history2[:,2], label='omega k=2 [rad/s]')
    ax.plot(t, input_history3[:,0], label='vx k=3 [m/s]')
    ax.plot(t, input_history3[:,1], label='vy k=3 [m/s]')
    ax.plot(t, input_history3[:,2], label='omega k=3 [rad/s]')
    ax.set(xlabel="t [s]", ylabel="control input")
    plt.legend()
    plt.grid()


    plt.show()
