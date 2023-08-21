# slamandnavigation_ws
this workspace is describing the way to use slam&navigation in MORAI Simulation step by step


1. 리모에 라이다 배치
2. frame_id lidar로 설정
3. roslaunch wego tf_setting.launch
4. roslaunch pointcloud_to_laserscan sample_node.launch
5. roslaunch wego gmapping.launch
실행하여 맵 그리기

6. roscd wego cd maps
7. rosrun map_server mapsave
8. roslaunch naigation.laucnh

rviz로 estimated position 설정해주고
nav goal 지정해주면, 자율주행 실시

![gmapping](/gif/gmapping.gif)
![navigation](/gif/navigation.gif)