#!/usr/bin/env python3.6

import json
# import webcolors
import re
from flask import Flask, request, render_template
from flask_cors import CORS

# file to write to
FILE_PATH = 'data.json'

# regex to match that colors are hexadecimal values
regex_color = '^#[A-Fa-f0-9]{6}$'

APP = Flask(__name__,static_url_path='/static',
            template_folder='templates')
# allow cross origin requests, we need this because of jscolor
CORS(APP)


@APP.route('/', methods=['GET'])
def index():
    return render_template('index.html')


# writes the data to the output file
def write(data):
    d = json.dumps(data)
    with open(FILE_PATH, 'w') as f:
        f.write(d)
        f.close()


@APP.route('/state', methods=['GET'])
def get_state():
    """
    GET /state

    Returns the current state of the lights.
    This will just return the current state of the data file, without checking that it is valid json.
    Not sure if there is any point in converting from json back into json again.
    """
    with open(FILE_PATH, 'r') as f:
        return f.readlines()


def validate_state(data: dict):
    """
    Checks that the provied object contains valid data

    Throws an assertionerror if invalid
    """
    assert isinstance(data, dict)

    # validate colors
    assert data['color1'] is not None
    assert re.match(regex_color, data['color1'])
    assert data['color2'] is not None
    assert re.match(regex_color, data['color2'])

    # validate types for the values that we cast
    # this check is redundant when getting values from the form
    # but is not when we just get json from the user
    assert isinstance(data['random1'], bool)
    assert isinstance(data['random2'], bool)
    assert isinstance(data['pattern'], int)
    assert isinstance(data['length'], int)
    assert isinstance(data['delay'], int)

    # check the bounds for some of the parameters
    assert data['length'] > 0
    assert data['delay'] >= 0
    assert data['pattern'] > 0

@APP.route('/form', methods=['POST'])
def form_state():
    """
    POST /form
    Request body are url encoded form params

    Updates the state using the form parameters.
    """
    data = {}
    # get the state from request args
    # these can be part of the query string, but we don't really care if it's one or the other
    try:
        data['color1'] = webcolors.hex_to_rgb('#' + request.args['color1'])
        data['color2'] = webcolors.hex_to_rgb('#' + request.args['color2'])
        data['random1'] = bool(request.args['random1'])
        data['random2'] = bool(request.args['random2'])
        data['pattern'] = int(request.args['pattern'])
        data['length'] = int(request.args['length'])
        data['delay'] = int(request.args['delay'])
        validate_state(data)
    except Exception:
        # if we caught something, probably invalid request data
        return 'Bad!', 400
    write(data)
    return data, 200


@APP.route('/state', methods=['POST'])
def post_state():
    """
    POST /state

    Expects the following json from the request body

    {
    "color1": "#00f00f",
    "color2": "#00f00f",
    "random2": true,
    "random1": true,
    "length": 1,
    "delay": 1,
    "pattern": 1
    }

    Updates the current state from the json provided in the request body.
    """
    # from the request body, load some json
    try:
        data = json.loads(request.data)
        validate_state(data)
    except Exception:
        # todo make this exception handling more specific
        # just return bad request, something was likely invalid
        return 'Bad!', 400
    # write this data to the state file if valid
    write(data)
    return json.dumps(data), 200


if __name__ == '__main__':
    # host the server on port 80
    # while we shouldn't require using the builtin server in production environment
    # I think that this is just fine for the use case that I require
    # we can just turn off debug mode in production
    APP.run(debug=True, host='0.0.0.0', port=80)
