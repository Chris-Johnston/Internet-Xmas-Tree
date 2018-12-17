#!/usr/bin/env python3.6

import json
import webcolors #hex_to_rgb
from flask import Flask, request, render_template
from flask_cors import CORS

# file to write to
FILE_PATH = 'data.json'

APP = Flask(__name__,static_url_path='/static',
            template_folder='templates')
CORS(APP)

@APP.route('/', methods=['GET', 'POST'])
def root():
    return render_template('index.html')
    #return APP.send_static_file('index.html')

# writes the data to the output file
def write(data):
    d = json.dumps(data)
    file = open(FILE_PATH, 'w')
    file.write(d)
    file.close()

# reads the form data, assumes that it's all good
# returns back the data that was sent
@APP.route('/set', methods=['GET', 'POST'])
def set_data():
    # set data, replacement of that PHP script
    data = {}
    data['color1'] = webcolors.hex_to_rgb('#' + request.args['color1'])
    data['color2'] = webcolors.hex_to_rgb('#' + request.args['color2'])
    #data['color1'] = request.args['color1']
    #data['color2'] = request.args['color2']
    data['random1'] = request.args['random1'] == 'true  '
    data['random2'] = request.args['random2'] == 'true'
    data['pattern'] = int(request.args['pattern'])
    data['length'] = int(request.args['length'])
    data['delay'] = int(request.args['delay'])
    # convert the colors from hex strings to
    # RGB values
    write(data)
    return json.dumps(data)

if __name__ == '__main__':
    APP.run(debug=True, host='0.0.0.0')
