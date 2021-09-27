from flask import Flask
from flask import jsonify, make_response, request
from flask_restful import Resource, Api
import json
import sys

from postgis_crud_rest.api import Api as BackendApi
from postgis_crud_rest.api import Status


app = Flask(__name__)
api = Api(app)


@app.route('/api/create_polygon', methods=['POST'])
def createPolygon():
    if request.form:
        try:
            status = backendApi.createOrUpdatePolygon(json.dumps(request.form))
            if status == Status.Created:
                response = make_response(jsonify({'status': 'Created'}), 201)
            else:
                response = make_response(jsonify({'error': 'Bad Request'}), 400)
        except Exception as e:
            response = make_response(jsonify({'error': 'Internal Server Error'}), 500)
    else:
        response = make_response(jsonify({'error': 'Bad Request'}), 400)
    return response


@app.route('/api/delete_polygon/<int:id>', methods=['DELETE'])
def deletePolygon(id):
    try:
        backendApi.deletePolygon(json.dumps({'id': id}))
        response = make_response(jsonify({'status': 'Deleted'}), 200)
    except Exception as e:
        response = make_response(jsonify({'error': 'Internal Server Error'}), 500)
    return response


@app.route('/api/delete_polygons', methods=['DELETE'])
def deletePolygons():
    try:
        status = backendApi.deleteAllPolygons()
        if status == Status.Deleted:
            response = make_response(jsonify({'status': 'Deleted'}), 200)
        else:
            response = make_response(jsonify({'error': 'Internal Server Error'}), 500)
    except Exception as e:
        response = make_response(jsonify({'error': 'Internal Server Error'}), 500)
    return response


@app.route('/api/update_polygon', methods=['POST'])
def updatePolygon():
    if request.form:
        try:
            status = backendApi.createOrUpdatePolygon(json.dumps(request.form))
            if status == Status.Updated:
                response = make_response(jsonify({'status': 'Updated'}), 201)
            else:
                response = make_response(jsonify({'error': 'Bad Request'}), 400)
        except Exception as e:
            response = make_response(jsonify({'error': 'Internal Server Error'}), 500)
    else:
        response = make_response(jsonify({'error': 'Bad Request'}), 400)
    return response


@app.route('/api/get_polygons', methods=['GET'])
def getPolygons():
    try:
        responseData = backendApi.getPolygons()
        response = make_response(responseData, 200)
    except Exception as e:
        response = make_response(jsonify({'error': 'Internal Server Error'}), 500)
    return response


if __name__ == '__main__':
    connectionString = sys.argv[1]
    assert connectionString is not None

    backendApi = BackendApi(connectionString)
    app.run(debug=True)
