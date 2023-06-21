import random
from flask import Flask, request, Response, jsonify, make_response, send_file, render_template, send_from_directory
from waitress import serve

#Clases locales
from RMDato import RMDato

#Variables globales
a_RMDato = []
a_RMDato.append(RMDato("Nombre1",1))
a_RMDato.append(RMDato("Nombre2",2))



app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/valores", methods=['GET'])
def valores():
    return ', '.join([str(x) for x in a_RMDato])

if __name__ == "__main__":
  #nos conectamos al servidor al puerto 8080, por ejemplo http://127.0.0.1:8080
  app.run(host='0.0.0.0', threaded=True, port=8080, debug=True)
  #cuando subamos a producion cambiamos a la linea de abajo
  #serve(app, host="0.0.0.0", port=8080)





