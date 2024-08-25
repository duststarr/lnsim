from flask import Flask, jsonify, abort, make_response, request,send_from_directory
from sgp4.api import Satrec
from sgp4.api import jday
import numpy as np
from flask_cors import CORS

from coordinator import Coordinator

app = Flask(__name__)
CORS(app)

coo = Coordinator()


@app.route('/leo/api/v1.0/test', methods=['GET'])
def leotest():
    return jsonify({'id':'hello world'})

@app.route('/leo/testczml', methods=['GET'])
def testczml():
    return send_from_directory('static', 'test.czml', mimetype='javascript/json')

@app.route('/leo/build', methods=['GET'])
def build():
    p = request.args.get('p')
    n = request.args.get('n')
    i = request.args.get('i')
    h = request.args.get('h')
    return jsonify(coo.build(p, n, i , h))

@app.route('/leo/update', methods=['GET'])
def update():
    t = request.args.get('time')
    return jsonify(coo.update(t))


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(debug=True)
