import os
import rospy
import sys
sys.path.append('/home/pqbas/miniconda3/envs/dl/lib/python3.8/site-packages')
sys.path.append('/home/pqbas/catkin_ws/src/blueberry/src/detection')
sys.path.append('/home/pqbas/catkin_ws/src/blueberry/src/detection/object_detection_models/yolov5')

import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Imu
from sensor_msgs.msg import Image, CompressedImage
from cv_bridge import CvBridge, CvBridgeError
from vision_msgs.msg import Detection2D, BoundingBox2D, ObjectHypothesisWithPose, Detection2DArray
from geometry_msgs.msg import Pose2D, PoseWithCovariance, Pose
import rospy
import pyzed.sl as sl
import cv2
import numpy as np
from pathlib import Path

bridge = CvBridge()

def test_callback(data):
   rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)



def zed_image_callback(msg):
    # Get the image inside the msg
    img0 = None
    
    try:
        img0 = bridge.imgmsg_to_cv2(msg, "bgr8")
        rospy.loginfo(rospy.get_caller_id() + " Succeed: Image received" + " Size: " + str(msg.height) + "x" + str(msg.width))
        return img0
    except CvBridgeError:
        rospy.loginfo(rospy.get_caller_id() + " Error: LOL")
        return None