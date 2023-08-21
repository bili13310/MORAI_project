# camera_ws
this workspace is describing the way to use LKAS in MORAI Simulation step by step

# 1.sub_camera.py
scout_mini에 카메라는 z축 값을 0.15로 설정하고 가운데에 위치시켜주는 것만 신경써준다.

ROS로 connect 시켜준 뒤, 
명령어: rqt_image_view
실행시켜주면 현재 카메라 관점을 확인할 수 있다.

카메라ㅗ 받은 데이터를 openCV로 변환시켜 준 뒤, 해당 데이터를 출력

# 2. pub_camera.py
카메라 데이터를 받고, camera_rgb_image & camera_gray_img 두 개의 토픽에 각각ㄱ 컬러 및 흑백 이미지 메시지를 바행하는 publisher 생성

callback 메서드:
카메라로 받은 데이터를 opncv 형식으로 변환하고
gray_image에는 변환된 BGR형식의 이미지를 흑백으로 변환

컬러와 흑백으로 변환된 이미지를 다시 ROS imgmsg로 변환하여 발행

# 3. bird_eye_view
** LKAS(Lane Keeping Assistance System)
bird eye view:
시점 위치가 높은 투시도로서, 지표를 공중에서 수직으로 본 것을 도화한 지도

main문
image_parser라는 변수에 BirdEyeView 클래스의 인스턴스를 넣어준다

BirdEyeView 클래스
먼저 init 메서드를 만든다
init_node를 정의해줘야되는데
이름은 bird_eye_view로 지정하고, anonymous=True를 설정해줌으로써, 매 노드를 발행해줄때마다 이름 뒤에 임의의 숫자를 추가해줘서 나중에 발행된 노드가 많아짐에따라 발생할 충돌을 방지해준다.
CVBridge는 opencv 이미지 데이터와 ros 이미지 메시지 간의 변환을 수행하는 객체이다. 이를 인스턴스 변수 self.bridge에 할당한다.
rospy.Subscriber라는 객체를 self.image_sub 인스턴스 변수에 넣는다.
rospy.Subscriber 클래스를 사용해서 노드는 특정 토픽의 메시지를 구도하고, 그 메시지가 도착할 때마다 지정된 콜백 함수를 호출하여 처리할 수 있다.
rospy.Subscriber(name, data_class, callback, queue_size=1)
data_class: 수신할 메시지의 데이터 타입을 나타낸다.
callback: 메시지가 도착할 때 호출될 콜백 함수를 지정하는 인수. 이 함수는 수신한 데이터를 처리하거나 활용하는 데 사용된다.

**
위 예제에서 callback이 아닌 self.callback을 사용한 이유:(객체 지향 프로그래밍과 ros의 노드 구조를 고려한 것)
클래스 내부에서 콜백 함수를 메서드로 정의하면(ex. def callback) 클래스의 멤버 변수와 메서드에 접근할 수 있어서 더 편리하게 데이터를 처리하고 관리 가능.
self.callback이 아닌 callback으로 클래스 외부에 정의한다면, 클래스의 멤버 변수와 메서드에 접근하기 위해 추가적인 전역 변수나 함수 매개변수를 사용해야됨.
rospy.spin()
ros 노드를 실행하는 메서드. 노드가 계속 실행되면서 구독 및 발행 작업을 처리. 노드가 종료될 떄까지 무한 루프에서 실행
def img_warp(): opencv를 사용하여 이밎 원근 변환을 수행하는 메서드
 원근 변환: 3차원 공간의 투영을 2차원으로 변환하는 기술. 주로 bird's eye view 효과를 만듦
img_x, img_y: 입력이미지의 너비와 높이를 변수로 지정.
img.shape: 이미지의 크기를 나타내는 튜플
img_size: 입력 이미지 크기 (없어도 되던데)
src_.._offset: 원근 변환을 위한 원본 이미지의 영역을 설정하는 오프셋
src_center_offset: 원본 이미지의 중심 영역은 특히 주변 영역에 비해 더 중요한 정보를 제공. 이를 우너근 변환을 통해 대상 이미지의 중심에 가깝게 배치하여 관심 영역을 강조
warp_img = cv2.warpPerspectrive(img, matrix, (self.img_x, self.img_y)):
원근 변환을 적용한 이미지 생성
img: 원본 이미지
matrix: 변환 메트릭스
(self.img_x, self.img_y): 이미지 사이즈
matrix: 원본 이미지에서 대상 이미지로 변활할떄는 원근 변환 메트릭스가 필요(cv2 라이브러리에 존재 고맙게도)
def callback:
subscriber가 msg를 받을 때마다 호출하는 callback 메서드
이미지를 받아와서 원근 변환을 수행한 뒤 변환된 이미지를 발행하고, 이미지 윈도우를 생성하여 원본 이미지와 변환된 이미지를 표시
cv2.waitKey(1): 키 입력을 기다리는 함수. 이 함수가 없으면 윈도우가 작동하지 않을 수 있음
*1은 1ms 동안 키 입력을 기다리는 것을 의미

![bird_eye_view](/gif/bird_eye_view.gif)

# 4.white_line_detect
# 5.yellow_line_detect
# 6. blend_line
# 7. binary_line
morai_line_detect
*
def img_warp & def img_CB은 bird_eye_view 문서 참조
hsv(색조Hue, 채도Saturation, 명도Value)
def detect_color:
이미지에서 흰색 색상을 감지하는 함수를 정의
색조
0-255
채도
0-10
명도
150-255
반쪽 베어먹은 도넛
white_mask: 결과로 바이너리 이미지. 흰색에 해당하는 픽셀은 흰색으로, 나머지는 검은색으로 표시
white_color = cv2.bitwise_and(img, img, mask=white_mask):
원본 이미지 img와 white_mask를 AND 연산
AND 연산 수행(둘 다 1일 때만 결과가 1)
mask=white_mask: white_mask가 1인 부분에서만 AND연산 수행
첫 번째 img에선 원본 이미지 & AND 연산을 위한 mask 역할
두 번째 img에서는 원본 이미지 역할
yellow_line_detect도 거의 유사
주황선을 탐색하기 위해 hsv 값을 변경
색조
15-45
채도
80-255
명도
0-255
binary_line (def img_binary 메서드 집중)
두 색을 다 탐지 하기 위해 두 색의 영역 지정
yellow_low, yellow_high
white_low, white_high
그 다음 각 색에 대한 mask 지정해주기
두 색을 동시에 masking 해주는 변수 지정
blend_mask
cv2.bitwise_or 둘 중 하나라도 1 이라면 결과가 1
def img_binary
BGR2GRAY 흑백(grayscale)로 바꾸는 과정
*
np.zeros(shape, dtype ...)
주어진 shape과 type에 따라서 0으로 새로운 배열 반환
shape: int이거나 tuple of ints
dtype: float64가 default, int8도 가능
>> np.zeros(5)
array([0., 0., 0., 0., 0.])
>> np.zeros((5,), dtype=int)
array([0, 0, 0, 0, 0])
>> s = (2, 2)
>> np.zeros(s, dtype=int)
array([[0, 0],
	[0, 0]])
	
np.zeros_lie
주어진 배열의 같은 shape과 type으로 된 0들의 배열을 반환(-> 임의의 배열을 np.zeros_lie에 넣으면 해당 배열의 내부 요소를 다 0으로 바꿔줘)
픽셀값 기준 bin이 127 이상이면 흰색(255)로 입력
나머지는 0으로 유지

![4](/gif/white_line_detect.gif)
![5](/gif/yellow_line_detect.gif)
![6](/gif/blend_line.gif)

# 8. sliding_window
# 9. LKAS
morai_sliding_window
?
def img_binary
binary_line[bin != 0] = 1
bin의 픽셀값이 0아 아니면 1로 넣겠다
픽셀값 0과 1 차이는 없는데 무슨 말인지..
7.binary_line에서는 127 이상이면 모두 255(흰색)과 매치가 안돼
def dtect_nothing
self.img_x 원본 이미지의 값
self.nwindows = 10
self.window_height = 원본 이미지의 y에서 self.nwindows(10)을 나눈 값
self.nothing_left_x_base: 원본 이미지의 x축의 왼쪽에서부터 14%를 차지하는 부분
self.nothing_right_x_base: 원본 이미지의 x축의 오른쪽에서부터 14%를 차지하는 부분
self.nothing_pixel_left_x: 0으로 구성된 (0, 10)의 행렬에 원본 이미지의 왼쪽에서 14% 부분까지를 더한 배열
self.nothing_pixel_right_x: 위와 유사
self.nothing_pixel_y:
list_comprehension을 사용하여 창들의 y-좌표 ㅗㄱ록 생성
*list_comprehension:
파이썬에서 리스트를 생성하는 효율적인 방법 중 하나. 반복문과 조건식을 사용해서 리스트를 생성하는데 사용
ex)
even_double = [x * 2 for x in range(1, 11) if x % 2 == 0]
1부터 10까지 x가 짝수일 경우에만 2를 곱해서 리스트에 입력
self.nothing_pixel_y:
self.window_height: 원본 이미지를 10으로 나눈 정수값
10개 창의 높이가 정의 됐어.
각 창의 중간 좌표를 찍기 위해
self.window_height / 2
여기서 list_comprehension이 들어가
위에서부터 차례대로 각 window의 y축 중간값 설정
0부터 9까지 총 10번 반복
def window_search:
이미지에서 차선을 검출하기 위해 히스토그램을 생성하고 분석하는 과정을 보여줌. 히스토그램은 이미지에서 픽셀 값의 분포를 나타내며, 여기서는 픽셀 분포를 이용해 차선의 위치를 추정하려고 함.
bottom_half_y = binary_line.shape[0] / 2: 이미지의 아래 절반의 y-좌표 값을 계산.
?
왜 이미지의 하단 반만 생성해?

np.sum()
A = array([[0,1,2],[3,4,5])
>> np.sum(A)
15
>> np.sum(A, axis=0)
array([3, 5, 7])
>> np.sum(A, axis=1)
array([3, 12])
histogram = ... :
이미지의 아래 절반 영역에 대한 히스토그램 생성. 'np.sum'을 활용하여 각 열의 픽셀 값을 더해서 히스토그램을 계산. 이미지의 각 열마다 흰색 픽셀의 개수가 계산됨
midpoint:
히스토그램을 중앙에서 절반으로 나누기 위한 중앙 지점을 계산
left_x_base:
왼쪽 차선의 기준 x좌표를 계산. 히스토그램의 왼쪽 절반에서 가장 높은 값을 가지는 열의 인덱스를 찾음
right_x_base:
오른쪽 차선
if left_x_base -- 0:
왼쪽 차선의 기준 x좌표가 0인지 확인. 이전 단계에서 왼쪽 차선의 위치를 히스토그램을 통해 찾지 못한 경우
left_x_current = self.nothing_left_x_base:
nothing_left_x_base 값을 현재 왼쪽 차선의 좌표로 설정한다. 즉 아무것도 없는 영역을 감지한 경우, 아므것도 없는 영역을 왼쪽 차선의 기준 위치로 설정한다.
else: 왼쪽 차선의 기준 x좌표가 0아 아니라면
left_x_current = left_x_base:
left_x_base 값을 현재 왼쪽 차선의 x좌표로 설정
if right_x_base == midpoint:
오른쪽 차선의 기준 x좌표가 중앙 지점과 같은지 확인
...
out_img = ... :
binary_line 이미지를 컬러 이미지로 변환해서 out_img에 저장. d이를 통해 검출된 차선을 시각화할 준비. np.dstack은 행렬을 쌓아서 3차원 배열을 생성. 3개의 동일 이미지를 쌓아서 컬러 채널을 만듦

![8](/gif/LKAS.gif)