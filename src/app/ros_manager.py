import os
import rospy

def callback(data):
   rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)