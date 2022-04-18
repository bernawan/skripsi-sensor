import json
import random
import time
import requests
from datetime import datetime
from flask import Flask, Response, render_template, stream_with_context


application = Flask(__name__)

random.seed()  # Initialize the random number generato

@application.route('/')

def index():
    return render_template('index.html')





@application.route('/chart-data')
def chart_data():
    def ambil_data_suhu():
        while True:
            response = requests.get('http://192.168.48.90:5000/suhu')
            suhu = json.loads(response.content)
            response.close()
            json_data = json.dumps(
                {'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'value_suhu': suhu['suhu'], 'value_kelembapan': suhu['kelembapan']})
            yield f"data:{json_data}\n\n"
            time.sleep(1)



    response = Response(stream_with_context(ambil_data_suhu()), mimetype="text/event-stream")
    response.headers["Cache-Control"] = "no-cache"
    response.headers["X-Accel-Buffering"] = "no"
    return response





if __name__ == '__main__':
    application.run(host='0.0.0.0', debug=True, threaded=True)

