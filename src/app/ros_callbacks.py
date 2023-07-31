#!/usr/bin/env python3

import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Imu
from sensor_msgs.msg import Image, CompressedImage
from cv_bridge import CvBridge, CvBridgeError
from vision_msgs.msg import Detection2D, BoundingBox2D, ObjectHypothesisWithPose, Detection2DArray
from geometry_msgs.msg import Pose2D, PoseWithCovariance, Pose, PoseStamped
import rospy
import pyzed.sl as sl
import cv2
import numpy as np
from pathlib import Path
bridge = CvBridge()


class zed_image_callback_class():

    def __init__(self) -> None:
        self.ZED_IMG = None
        pass
    
    def callback(self, msg):
        try:
            self.ZED_IMG = bridge.imgmsg_to_cv2(msg, "bgr8")
            rospy.loginfo(rospy.get_caller_id() + " Succeed: Image received" + " Size: " + str(msg.height) + "x" + str(msg.width))
        except CvBridgeError:
            rospy.loginfo(rospy.get_caller_id() + " Error: LOL")


class odometry_callback_class():

    def __init__(self) -> None:
        self.DICTIONARY_DESARROLLO = None
        pass
    
    def callback(self, msg):
        self.DICTIONARY_DESARROLLO[0]['info']['x'] = msg.pose.position.x
        self.DICTIONARY_DESARROLLO[0]['info']['y'] = msg.pose.position.y
        self.DICTIONARY_DESARROLLO[0]['info']['z'] = msg.pose.position.z

