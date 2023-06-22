#!/usr/bin/env python3
import sys
sys.path.append('/home/pqbas/miniconda3/envs/iot/lib/python3.8/site-packages') #JORGE
from watchdog.events import EVENT_TYPE_OPENED
from flask import Flask, render_template, jsonify
import random
import threading



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


if __name__ == '__main__':
    #subscriber_ros()
    app.run(debug=True, port=5000)