import sys
sys.path.append('/home/pqbas/miniconda3/envs/iot/lib/python3.8/site-packages')
from watchdog.events import EVENT_TYPE_OPENED
from flask import Flask, render_template, jsonify


SIMULATOR = True # True / False - Verdadero si quiere usar el simulador

DICTIONARY = {
    'topic1': -1,
    'topic2': -1
    }



def subscriber_ros():
    
    if SIMULATOR == True:
        # Iterar sobre el diccionario y generar valores aleatorios
        # actualizando el diccionario
        print("SIMULATOR -- ON")

    else:
        # hacer 'import rospy.py'
        # iterar el diccionario y suscribirse a cada topico del diccionario,
        # actualiza el diccionario en base a los valores del topic
        print("SIMULATOR -- OFF")


    return



app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/functions.js')
def index():
    return render_template('functions.js')

@app.route('/datos',methods=['GET'])
def solicitud():
    return jsonify(DICTIONARY)




if __name__ == '__main__':
    app.run(debug=True, port=5000)