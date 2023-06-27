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


from background_thread import BackgroundThreadFactory, TASKS_QUEUE
logging.basicConfig(level=logging.INFO, force=True)


SIMULATOR = True # True / False - Verdadero si quiere usar el simulador

DICTIONARY = [{
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
        from ros_manager import callback
        from std_msgs.msg import String
        threading.Thread(target=lambda: rospy.init_node('iot_node', disable_signals=True)).start()
        rospy.Subscriber("data_simulated", String, callback)
        # hacer 'import rospy.py'
        # iterar el diccionario y suscribirse a cada topico del diccionario,
        # actualiza el diccionario en base a los valores del topic
    return



def obtener_imagen_camara():
    # Crea un objeto VideoCapture para acceder a la cámara
    video = cv2.VideoCapture(0)
    
    # Captura el fotograma actual de la cámara
    ret, frame = video.read()
    
    # Convierte el fotograma a formato JPEG
    ret, jpeg = cv2.imencode('.jpg', frame)
    
    # Genera el fotograma codificado en bytes
    frame_bytes = jpeg.tobytes()
    
    # Devuelve el fotograma como respuesta al cliente
    yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n\r\n')


def create_app():

    app = Flask(__name__)

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/functions.js')
    def functions():
        return render_template('functions.js')

    @app.route('/datos',methods=['GET'])
    def solicitud():
        return jsonify(DICTIONARY)
    
    @app.route('/camera')
    def imagen_camara():
        return Response(obtener_imagen_camara(),
                        mimetype='multipart/x-mixed-replace; boundary=frame')

    
    notification_thread = BackgroundThreadFactory.create('notification')

    # this condition is needed to prevent creating duplicated thread in Flask debug mode
    if not (app.debug == 'development') == 'true':
        notification_thread.start()

        original_handler = signal.getsignal(signal.SIGINT)

        def sigint_handler(signum, frame):
            notification_thread.stop()

            # wait until thread is finished
            if notification_thread.is_alive():
                notification_thread.join()

            original_handler(signum, frame)

        try:
            signal.signal(signal.SIGINT, sigint_handler)
        except ValueError as e:
            logging.error(f'{e}. Continuing execution...')

    return app

if __name__ == '__main__':
    #subscriber_ros()
    # Start the threa
    #app.run(debug=True, port=5000)
    
    app = create_app()
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    app.run(debug=True, port=5000)