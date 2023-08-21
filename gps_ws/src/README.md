# gps_ws
this workspace is describing the way to planning & following the path in MORAI Simulation step by step

# path planning
path maker launch 파일 수정해서 경로 따야돼
준비물:
gps, imu
(scout_path_maker 참고)

실행방법:
1. ros_example_package
2. scout_ros
3. launch
4. path._maker.launch 에서 저장될 파일 이름 설정
저장하면 path 폴더에 저장
5. roslaunch scout_ros path_maker
실행 후, 로봇 움직여서 gps 경로 데이터 따기

6. scout_planner.py에 scout_ros_utils 첨부
7. 로봇에 imu 추가
8. roslaunch scout_ros_planner.launch 실행

rviz에서 경로를 따라가는 걸 확인

![path_planner](/gif/path_maker.gif)
![path_following](/gif/path_following.gif)