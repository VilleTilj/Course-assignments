import numpy as np
import matplotlib.pyplot as plt
from visualize_mobile_robot import sim_mobile_robot
from detect_obstacle import detect_obstacle_e5t2
import math

# Constants and Settings
Ts = 0.01 # Update simulation every 10ms
t_max = np.pi*4 # total simulation duration in seconds
# Set initial state
init_state = np.array([-2., 1., 0.]) # px, py, theta
IS_SHOWING_2DVISUALIZATION = True

# Define Field size for plotting (should be in tuple)
field_x = (-2.5, 2.5)
field_y = (-2, 2)
d_safe = 0.4
eps = 0.1

# Init logging messages
GTG = "State: Go to goal"
AVOID = "State: Avoid obstacle"
MOVE_WALL_C = "State: Wall Following clockwise"
MOVE_WALL_CC = "State: Wall Following counter clockwise" 
NO_READING = "No reading, Go to goal"
INIT = "State: Initing"

# Compute the positions that is detected by the range sensor
# to be used in visualization and in control algorithm
def compute_sensor_endpoint(robot_state, sensors_dist):

    # NOTE: we assume sensor position is in the robot's center
    sens_N = len(sensors_dist)
    obst_points = np.zeros((3,sens_N))

    for i in range(sens_N):
        reading = np.array([sensors_dist[i]*np.cos(robot_state[2]), sensors_dist[i]*np.sin(robot_state[2]), 1])

        sensor_rot = np.array([[np.cos(np.pi/4*i), -np.sin(np.pi/4*i), 0],
                               [np.sin(np.pi/4*i), np.cos(np.pi/4*i), 0],
                               [0, 0, 1]
        ])

        rob_rot = np.array([[np.cos(robot_state[2]), -np.sin(robot_state[2]), robot_state[0]],
                            [np.sin(robot_state[2]), np.cos(robot_state[2]), robot_state[1]],
                            [0, 0, 1]
        ])

        obst_points[:, i] = rob_rot @ sensor_rot @ reading

    return obst_points[:2,:] # only return x and y values


# MAIN SIMULATION COMPUTATION
#---------------------------------------------------------------------
def simulate_control():
    sim_iter = round(t_max/Ts) # Total Step for simulation

    # Initialize robot's state (Single Integrator)
    robot_state = init_state.copy() # numpy array for [px, py, theta]
    desired_state = np.array([2., 0., 0.]) # numpy array for goal / the desired [px, py, theta]
    current_input = np.array([0., 0., 0.]) # initial numpy array for [vx, vy, omega]
    x_ts = np.array([np.inf, np.inf, np.inf])

    # Init state
    state = INIT

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
        obst_vertices = np.array( [ [-1., -1.5], [1., -1.5], [1., 1.5], [-1., 1.5], \
                [-1., 1.], [0.5, 1.], [0.5, -1.], [-1., -1.], [-1., -1.5] ]) 
        sim_visualizer.ax.plot( obst_vertices[:,0], obst_vertices[:,1], '--r' )

        # get sensor reading
        sensors_dist = detect_obstacle_e5t2( robot_state[0], robot_state[1], robot_state[2]) 
        # compute and plot sensor reading endpoint
        obst_points = compute_sensor_endpoint(robot_state, sensors_dist)
        pl_sens, = sim_visualizer.ax.plot(obst_points[0], obst_points[1], '.', marker='X')
        pl_txt = [sim_visualizer.ax.text(obst_points[0,i], obst_points[1,i], str(i)) for i in range(len(sensors_dist))]

    
    for it in range(sim_iter):
        # record current state at time-step t
        state_history[it] = robot_state
        goal_history[it] = desired_state

        # Get information from sensors
        sensors_dist = detect_obstacle_e5t2( robot_state[0], robot_state[1], robot_state[2]) 
        # compute and plot sensor reading endpoint
        obst_points = compute_sensor_endpoint(robot_state, sensors_dist)

        # IMPLEMENTATION OF CONTROLLER
        #------------------------------------------------------------
        # Compute the control input
        
        # Find closest sensor measurement on wall  
        min_id = np.argmin(sensors_dist)
        x_0 = np.concatenate((obst_points[:, min_id], [0]))

        # Calculate control inputs 
        k = calculate_time_varying_k(desired_state, robot_state, v0=5, beta=0.5)
        u_gtg = k*(desired_state - robot_state)
        u_avo = k*(robot_state - x_0)
        u_wf_c = k * np.array([[0, 1, 0], [-1, 0, 0], [0, 0, 1]]) @ u_avo
        u_wf_cc = k * np.array([[0, -1, 0], [1, 0, 0], [0, 0, 1]]) @ u_avo

        
        # if there is a reading from the sensor
        if sensors_dist[min_id] < 0.99:
            state, x_ts = state_machine(state, robot_state, desired_state, x_ts,u_gtg, u_avo, u_wf_c, u_wf_cc, x_0)
            
            # Follow lates state rules   
            if state == AVOID:
                current_input = u_avo
            elif state == GTG:
                current_input = u_gtg
            elif state == MOVE_WALL_C:
                current_input = u_wf_c
            elif state == MOVE_WALL_CC:
                current_input = u_wf_cc

        else:
            current_input = u_gtg
            if state != NO_READING:
                state = NO_READING
                print(NO_READING)

        # record the computed input at time-step t
        input_history[it] = current_input

        if IS_SHOWING_2DVISUALIZATION: # Update Plot
            sim_visualizer.update_time_stamp( it*Ts )
            sim_visualizer.update_goal( desired_state )
            sim_visualizer.update_trajectory( state_history[:it+1] ) # up to the latest data
            # update sensor visualization
            pl_sens.set_data(obst_points[0], obst_points[1])
            for i in range(len(sensors_dist)): pl_txt[i].set_position((obst_points[0,i], obst_points[1,i]))
        
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
    return state_history, goal_history, input_history


def state_machine(current_state, robot_state, desired_state, x_ts ,u_gtg, u_avo, u_wf_c, u_wf_cc, x0):
    eps = 0.2
    d_safe = 0.2
    
    if d_safe - eps < np.linalg.norm(robot_state - x0) < d_safe + eps and np.transpose(u_gtg) @ u_wf_c > 0:
        if current_state != MOVE_WALL_C and current_state != MOVE_WALL_CC: # 
            current_state = MOVE_WALL_C
            x_ts = robot_state
            print(MOVE_WALL_C)

    elif d_safe - eps < np.linalg.norm(robot_state - x0) < d_safe + eps and np.transpose(u_gtg) @ u_wf_cc > 0:
        if current_state != MOVE_WALL_CC  and current_state != MOVE_WALL_C:
            print(MOVE_WALL_CC)
            x_ts = robot_state
            current_state = MOVE_WALL_CC

    elif np.linalg.norm(robot_state - x0) < d_safe - eps:
        if current_state != AVOID and current_state != GTG:
            current_state = AVOID
            print(AVOID)

    elif np.linalg.norm(robot_state - desired_state) < np.linalg.norm(robot_state - x_ts) and np.transpose(u_avo) @ u_gtg > 0:
        if current_state != GTG and current_state != AVOID:
            print(GTG)
            current_state = GTG

    return current_state, x_ts


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
    # fig2 = plt.figure(2)
    # ax = plt.gca()
    # ax.plot(t, input_history[:,0], label='vx [m/s]')
    # ax.plot(t, input_history[:,1], label='vy [m/s]')
    # ax.plot(t, input_history[:,2], label='omega [rad/s]')
    # ax.set(xlabel="t [s]", ylabel="control input")
    # plt.legend()
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
