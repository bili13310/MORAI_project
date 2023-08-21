#!/usr/bin/env python3
  
import rospy
import cv2
import numpy as np
from sensor_msgs.msg import Image, CompressedImage
from cv_bridge import CvBridge

class BirdEyeView:
    def __init__(self):
        rospy.init_node('bird_eye_view', anonymous=True)
        self.bridge=CvBridge()
        self.image_sub = rospy.Subscriber("/image_jpeg/compressed", CompressedImage, self.callback)
        self.pub = rospy.Publisher("/bird_eye/compressed", CompressedImage, queue_size=10)
        rospy.spin()

    def detect_color(self, img):
        # Convert to HSV color space
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # Define range of yellow color in HSV
        yellow_lower = np.array([15, 80, 0])
        yellow_upper = np.array([45, 255, 255])

        # Define range of blend color in HSV
        white_lower = np.array([0, 0, 150])
        white_upper = np.array([255, 10, 255])
        # Threshold the HSV image to get only yellow colors
        yellow_mask = cv2.inRange(hsv, yellow_lower, yellow_upper)

        # Threshold the HSV image to get only white colors
        white_mask = cv2.inRange(hsv, white_lower, white_upper)

        # Threshold the HSV image to get blend colors
        blend_mask = cv2.bitwise_or(yellow_mask, white_mask)
        blend_color = cv2.bitwise_and(img, img, mask=blend_mask)
        return blend_color  

    def img_warp(self, img):
        self.img_x, self.img_y = img.shape[1], img.shape[0]
        # print(f'self.img_x:{self.img_x}, self.img_y:{self.img_y}')

        img_size = [640, 480]
        # ROI
        src_side_offset = [0, 240]
        src_center_offset = [200, 315]
        src = np.float32(
            [
                [0, 479],
                [src_center_offset[0], src_center_offset[1]],
                [640 - src_center_offset[0], src_center_offset[1]],
                [639, 479],
            ]
        )
        # 아래 2 개 점 기준으로 dst 영역을 설정합니다.
        dst_offset = [round(self.img_x * 0.125), 0]
        # offset x 값이 작아질 수록 dst box width 증가합니다.
        dst = np.float32(
            [
                [dst_offset[0], self.img_y],
                [dst_offset[0], 0],
                [self.img_x - dst_offset[0], 0],
                [self.img_x - dst_offset[0], self.img_y],
            ]
        )
        # find perspective matrix
        matrix = cv2.getPerspectiveTransform(src, dst)
        matrix_inv = cv2.getPerspectiveTransform(dst, src)
        warp_img = cv2.warpPerspective(img, matrix, (self.img_x, self.img_y))
        return warp_img
    

    def img_binary(self, blend_line):
        bin = cv2.cvtColor(blend_line, cv2.COLOR_BGR2GRAY)
        binary_line = np.zeros_like(bin)



    def callback(self, data):
        img = self.bridge.compressed_imgmsg_to_cv2(data)
        warp_img = self.img_warp(img)
        warp_img_msg = self.bridge.cv2_to_compressed_imgmsg(warp_img)
        self.pub.publish(warp_img_msg)
        cv2.namedWindow("img", cv2.WINDOW_NORMAL)
        cv2.namedWindow("img_warp", cv2.WINDOW_NORMAL)
        cv2.imshow("img", img)
        cv2.imshow("img_warp", warp_blend_line)
        cv2.waitKey(1)

      

if __name__ == '__main__':
    try:
        image_parser = BirdEyeView()
    except rospy.ROSInterruptException:
        pass