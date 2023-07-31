#!/usr/bin/env python3
import sys
sys.path.append('/home/pqbas/miniconda3/envs/iot/lib/python3.8/site-packages') #JORGE
from watchdog.events import EVENT_TYPE_OPENED
from flask import Flask, render_template, jsonify, Response, send_file
import threading
import time
import logging
import cv2
from dictionaries import DICTIONARY_DESARROLLO, DICTIONARY_INDUSTRIAL
sys.path.append('/home/pqbas/miniconda3/envs/dl/lib/python3.8/site-packages')
sys.path.append('/home/pqbas/catkin_ws/src/blueberry/src/detection')
sys.path.append('/home/pqbas/catkin_ws/src/blueberry/src/detection/object_detection_models/yolov5')
logging.basicConfig(level=logging.INFO, force=True)

video = None
ZED_IMG = None
SIMULATOR = False # True / False - Verdadero si quiere usar el simulador

if SIMULATOR == False:

    from std_msgs.msg import String
    from sensor_msgs.msg import Imu
    from sensor_msgs.msg import Image, CompressedImage
    from cv_bridge import CvBridge, CvBridgeError
    from vision_msgs.msg import Detection2D, BoundingBox2D, ObjectHypothesisWithPose, Detection2DArray
    from geometry_msgs.msg import Pose2D, PoseWithCovariance, Pose, PoseStamped
    import pyzed.sl as sl
    import cv2
    import numpy as np
    from pathlib import Path
    from ros_callbacks import zed_image_callback_class, odometry_callback_class
    from ros_classes import ROSNode
    
    zed_image_callback_ = zed_image_callback_class()
    odometry_callback_ = odometry_callback_class()
    bridge = CvBridge()

    def zed_image_callback(msg):
        global ZED_IMG
        zed_image_callback_.ZED_IMG = ZED_IMG
        zed_image_callback_.callback(msg)
        ZED_IMG = zed_image_callback_.ZED_IMG

    def odometry_callback(msg):
        global DICTIONARY_DESARROLLO
        odometry_callback_.DICTIONARY_DESARROLLO = DICTIONARY_DESARROLLO
        odometry_callback_.callback(msg)
        DICTIONARY_DESARROLLO = odometry_callback_.DICTIONARY_DESARROLLO
    
    node = ROSNode("iot_node")
    node.create_subscriber("/zed2i/zed_node/right_raw/image_raw_color", Image, zed_image_callback)
    node.create_subscriber("/zed2i/zed_node/pose", PoseStamped, odometry_callback)


from flask_callbacks import obtener_imagen_camara

def create_app():
    global video, ZED_IMG
    app = Flask(__name__)
    
    if SIMULATOR == False:
        threading.Thread(target=lambda: node.run())
    else:
        if video == None:
            video = cv2.VideoCapture(0)

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/functions.js')
    def functions():
        return render_template('functions.js')

    @app.route('/datos_desarrollo',methods=['GET'])
    def solicitud_desarrollo():
        return jsonify(DICTIONARY_DESARROLLO)
    
    @app.route('/datos_industrial',methods=['GET'])
    def solicitud_industrial():
        return jsonify(DICTIONARY_INDUSTRIAL)

    @app.route('/camera')
    def imagen_camara():
        return Response(obtener_imagen_camara(video, ZED_IMG, SIMULATOR),
                        mimetype='multipart/x-mixed-replace; boundary=frame')
    
    @app.route('/upao_logo.png')
    def returnLogoUpao():
        return send_file("templates/upao_logo.png", mimetype='image/png')
    
    @app.route('/robot.png')
    def returnRobot():
        return send_file("templates/robot.png", mimetype='image/png')

    return app

if __name__ == '__main__':
    app = create_app()
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    app.run(debug=True, port=5000)