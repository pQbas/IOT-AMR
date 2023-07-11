#!/usr/bin/env python3
import sys
sys.path.append('/home/pqbas/miniconda3/envs/iot/lib/python3.8/site-packages') #JORGE
from watchdog.events import EVENT_TYPE_OPENED
from flask import Flask, render_template, jsonify, Response
import random
import threading
import time
import logging
import signal
import os
import cv2


sys.path.append('/home/pqbas/miniconda3/envs/dl/lib/python3.8/site-packages')
sys.path.append('/home/pqbas/catkin_ws/src/blueberry/src/detection')
sys.path.append('/home/pqbas/catkin_ws/src/blueberry/src/detection/object_detection_models/yolov5')

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

def zed_image_callback(msg):
    # Get the image inside the msg
    global ZED_IMG
    
    try:
        ZED_IMG = bridge.imgmsg_to_cv2(msg, "bgr8")
        rospy.loginfo(rospy.get_caller_id() + " Succeed: Image received" + " Size: " + str(msg.height) + "x" + str(msg.width))
    except CvBridgeError:
        rospy.loginfo(rospy.get_caller_id() + " Error: LOL")


def odometry_callback(msg):
    # Get the image inside the msg
    global DICTIONARY_DESARROLLO
    DICTIONARY_DESARROLLO[0]['info']['x'] = msg.pose.position.x
    DICTIONARY_DESARROLLO[0]['info']['y'] = msg.pose.position.y
    DICTIONARY_DESARROLLO[0]['info']['z'] = msg.pose.position.z
    return


from background_thread import BackgroundThreadFactory, TASKS_QUEUE
logging.basicConfig(level=logging.INFO, force=True)

video = None
ZED_IMG = None
SIMULATOR = False # True / False - Verdadero si quiere usar el simulador


DICTIONARY_DESARROLLO = [{
		"topic_name": "/odom",
		"topic_name2show": "odometría",
		"info": {
			"x": -1,
			"y": -1,
			"z": -1
		}
	},
	{
		"topic_name": "/odrive_dual_control",
		"topic_name2show": "velocidad M1 M2",
		"info": {
			"eje M1": -1,
			"eje M2": -1
		}
	},
	{
		"topic_name": "/pistones_status",
		"topic_name2show": "pistones",
		"info": {
			"voltaje p1": -1,
			"corriente p1": -1,
			"voltaje p2": -1,
			"corriente p2": -1,
			"voltaje p3": -1,
			"corriente p3": -1,
			"voltaje p4": -1,
			"corriente p4": -1
		}
	}
]

DICTIONARY_INDUSTRIAL = [{
		"topic_name": "/odom2",
		"topic_name2show": "odometría",
		"info": {
			"x": -1,
			"y": -1,
			"z": -1
		}
	},
	{
		"topic_name": "/odrive_dual_control2",
		"topic_name2show": "velocidad M1 M2",
		"info": {
			"eje M1": -1,
			"eje M2": -1
		}
	},
	{
		"topic_name": "/pistones_status2",
		"topic_name2show": "pistones",
		"info": {
			"voltaje p1": -1,
			"corriente p1": -1,
			"voltaje p2": -1,
			"corriente p2": -1,
			"voltaje p3": -1,
			"corriente p3": -1,
			"voltaje p4": -1,
			"corriente p4": -1
		}
	},
    	{
		"topic_name": "/testing_topic_industrial",
		"topic_name2show": "another_topic",
		"info": {
			"info p1": -1,
			"info2 p1": -1,
			"info p2": -1,
			"info2 p2": -1,
			"info p3": -1,
			"info2 p3": -1,
			"info p4": -1,
			"info2 p4": -1
		}
	}
]
    


def subscriber_ros():
    
    if SIMULATOR == True:
        # Iterar sobre el diccionario y generar valores aleatorios
        # actualizando el diccionario
        print("SIMULATOR -- ON")
        
        for topic in DICTIONARY:
            random_number = random.randint(10,15) + random.random()
            DICTIONARY[topic] = random_number
        
        #print(DICTIONARY[topic])
        #sys.exit()  # JORGE: Commentarlo, lo uso para pruebas

    else:
        print("SIMULATOR -- OFF")

        import os
        import rospy
        # from ros_manager import test_callback, zed_image_callback
        from std_msgs.msg import String
        from sensor_msgs.msg import Image, CompressedImage
        threading.Thread(target=lambda: rospy.init_node('iot_node', disable_signals=True)).start()
        # rospy.Subscriber("data_simulated", String, test_callback)
        rospy.Subscriber("/zed2i/zed_node/right_raw/image_raw_color", Image, zed_image_callback)
        rospy.Subscriber("/zed2i/zed_node/pose", PoseStamped, odometry_callback)

        # hacer 'import rospy.py'
        # iterar el diccionario y suscribirse a cada topico del diccionario,
        # actualiza el diccionario en base a los valores del topic
    return


def create_app():
    global video
    app = Flask(__name__)
    
    if SIMULATOR == False:
        subscriber_ros()
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
        return Response(obtener_imagen_camara(),
                        mimetype='multipart/x-mixed-replace; boundary=frame')
    return app


def obtener_imagen_camara():
    global video 
    global ZED_IMG
    # Captura el fotograma actual de la cámara

    if SIMULATOR == False:
        # print(ZED_IMG.shape)
        if ZED_IMG is not None:
            ret, jpeg = cv2.imencode('.jpg', ZED_IMG)
            frame_bytes = jpeg.tobytes()
            # Devuelve el fotograma como respuesta al cliente
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n\r\n')

    else:
        ret, frame = video.read()
        if ret:
            # Convierte el fotograma a formato JPEG
            ret, jpeg = cv2.imencode('.jpg', frame)
            # Genera el fotograma codificado en bytes
            frame_bytes = jpeg.tobytes()
            # Devuelve el fotograma como respuesta al cliente
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n\r\n')


if __name__ == '__main__':
    
    # Start the threa
    #app.run(debug=True, port=5000)

    # Crea un objeto VideoCapture para acceder a la cámara
    app = create_app()
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    app.run(debug=True, port=5000)
