from flask import Flask
from flask import jsonify, make_response, request
from flask_restful import Resource, Api
import json

from backend.api import Api as BackendApi
from backend.api import connectionString as ConnectionString


app = Flask(__name__)
api = Api(app)


@app.route('/api/create_polygon', methods=['POST'])
def createPolygon():
    if request.form:
        try:
            backendApi = BackendApi(ConnectionString)
            backendApi.createPolygon(json.dumps(request.form))
            response = make_response(jsonify({'status': 'Created'}), 201)
        except Exception as e:
            response = make_response(jsonify({'error': 'Internal Server Error'}), 500)
    else:
        response = make_response(jsonify({'error': 'Bad Request'}), 400)
    return response


@app.route('/api/delete_polygon/<int:id>', methods=['DELETE'])
def deletePolygon(id):
    try:
        backendApi = BackendApi(ConnectionString)
        backendApi.deletePolygon(json.dumps({'id': id}))
        response = make_response(jsonify({'status': 'Deleted'}), 200)
    except Exception as e:
        response = make_response(jsonify({'error': 'Internal Server Error'}), 500)
    return response


@app.route('/api/update_polygon', methods=['POST'])
def updatePolygon():
    if request.form:
        try:
            backendApi = BackendApi(ConnectionString)
            backendApi.updatePolygon(json.dumps(request.form))
            response = make_response(jsonify({'status': 'Updated'}), 201)
        except Exception as e:
            response = make_response(jsonify({'error': 'Internal Server Error'}), 500)
    else:
        response = make_response(jsonify({'error': 'Bad Request'}), 400)
    return response


@app.route('/api/get_polygons', methods=['GET'])
def getPolygons():
    try:
        backendApi = BackendApi(ConnectionString)
        responseData = backendApi.getPolygons()
        response = make_response(responseData, 200)
    except Exception as e:
        response = make_response(jsonify({'error': 'Internal Server Error'}), 500)
    return response


if __name__ == '__main__':
    app.run(debug=True)
