import json
import os
from nose.tools import assert_equals, nottest
from shapely.geometry import Polygon as sgPolygon
from sqlalchemy.ext.declarative import declarative_base

from backend.api import Api as BackendApi
from backend.api import Singleton
from backend.polygon import Polygon


connectionString = os.environ.get('postgresql')
if connectionString is None:
    connectionString = "postgresql://postgres:qazwsx@localhost:5432/postgres"


class test_api():
    sgPolygonPoints = [[0, 0], [0, 1], [1, 1], [1, 0], [0, 0]]

    def setup(self):
        pass

    def teardown(self):
        backendApi = BackendApi(connectionString)
        Polygon.__table__.drop(backendApi._engine)
        del backendApi
        Singleton._instances.clear()

    def test_backendapi_init(self):
        backendApi = BackendApi(connectionString)
        print(backendApi.getPolygons())

    def test_backendapi_createpolygon(self):
        backendApi = BackendApi(connectionString)
        backendApi.createPolygon(json.dumps({'name': 'test'}))

    def test_BackendApi_updatePolygon(self):
        backendApi = BackendApi(connectionString)
        backendApi.createPolygon(json.dumps({'name': 'test'}))
        backendApi.updatePolygon(json.dumps({'name': 'test', 'id': 1, 'geom': sgPolygon(self.sgPolygonPoints).wkt}))

    def test_BackendApi_deletePolygon(self):
        backendApi = BackendApi(connectionString)
        backendApi.createPolygon(json.dumps({'name': 'test'}))
        backendApi.deletePolygon(json.dumps({'id': 1}))

    def test_BackendApi_getPolygons(self):
        backendApi = BackendApi(connectionString)
        backendApi.createPolygon(json.dumps({'name': 'test'}))
        backendApi.getPolygons()
