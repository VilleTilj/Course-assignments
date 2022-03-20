# Fundamentals of Mobile Robots

## Course brochure
This course introduces some answers to the basic questions of "where am I?" and "where have I seen?" and "How do I get there?", which are called location, mapping and planning, respectively, in the robotic community. More specifically,
- Students will learn basics about range sensors (Lidar, Radar, Sonar), radio based (GNSS, UWB), egomotion sensors (IMUs, wheel odometry) and their noise characteristics and probabilistic modeling.
- Students will learn about coordinate frames and sensor kinematics, that is, how to calculate sensor output in different coordinate frames.
- Students will learn how to fuse information comming from different sources (sensors, maps, control inputs,etc) using Bayes filters in particular Kalman filters and particle filters, and to use those to localize moving platforms.
- Students will learn about basic world model representations and how to build them (map building) from sensor inputs.
- Students will learn important deterministic route planning methods: Dynamic programming (DP), Dijkstra, A*,
- Student will also learn planning under uncertainty with MDP (Markov Decision Processes)

Notes:
* The focus of the planning part of the course will be on point robots, to avoid some complications which will rise due to differential kinematics of contact with ground.
* Although the focus of examples and presentation is on mobile robots moving on a 2D plane, most of the methods are applicable to higher dimenstions (manipulators or moving in 3D).


Core learning objectives:
+ Deterministic planning methods: dynamic programming, Dijkstra, A*
+ Bayesian filtering
+ Localization using Kalman filters and particle filters.
+ Occupancy grid mapping
+ Sensor technologies (LiDAR, Radar, Sonar, Leddar, IMU, GNSS, UWB), sensor models (LiDAR, Sonar, IMU) and their uncertainty
+ Motion control: path smoothing, path following and trajectory tracking

## Folders
The folders in the repo are different excercises on the course. 
