import sys
sys.path.append('/home/pqbas/miniconda3/envs/iot/lib/python3.8/site-packages')
from watchdog.events import EVENT_TYPE_OPENED
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)