import json
import os
from nose.tools import assert_equals, nottest
from shapely.geometry import Polygon as sgPolygon
from sqlalchemy.ext.declarative import declarative_base

from postgis_crud_rest.api import Api as BackendApi
from postgis_crud_rest.api import Singleton
from postgis_crud_rest.polygon import Polygon


connectionString = os.environ.get('postgresql')
if connectionString is None:
    connectionString = "postgresql://postgres:qazwsx@localhost:5432/postgres"


class test_api():
    sgPolygonPoints = [[0, 0], [0, 1], [1, 1], [1, 0], [0, 0]]

    def setup(self):
        backendApi = BackendApi(connectionString)
        backendApi.deleteAllPolygons()
        data = json.loads(backendApi.getPolygons())
        assert(len(data) == 0)

    def teardown(self):
        backendApi = BackendApi(connectionString)
        Polygon.__table__.drop(backendApi._engine)  # Need for reset id counter
        del backendApi
        Singleton._instances.clear()

    def test_backendapi_init(self):
        backendApi = BackendApi(connectionString)
        print(backendApi.getPolygons())

    def test_backendapi_createOnePolygon(self):
        backendApi = BackendApi(connectionString)
        backendApi.createOrUpdatePolygon(json.dumps({'name': 'test0'}))
        data = json.loads(backendApi.getPolygons())
        assert(len(data) == 1)
        assert(data[0]['name'] == 'test0')

    def test_backendapi_createTowPolygons(self):
        backendApi = BackendApi(connectionString)
        backendApi.createOrUpdatePolygon(json.dumps({'name': 'test0'}))
        data = json.loads(backendApi.getPolygons())
        assert(len(data) == 1)
        assert(data[0]['name'] == 'test0')
        backendApi.createOrUpdatePolygon(json.dumps({'name': 'test1'}))
        data = json.loads(backendApi.getPolygons())
        assert(len(data) == 2)
        assert(data[0]['name'] == 'test0')
        assert(data[1]['name'] == 'test1')

    def test_backendapi_UpdatePolygon(self):
        backendApi = BackendApi(connectionString)
        backendApi.createOrUpdatePolygon(json.dumps({'name': 'test0', 'id': 1}))
        data = json.loads(backendApi.getPolygons())
        assert(len(data) == 1)
        assert(data[0]['name'] == 'test0')
        backendApi.createOrUpdatePolygon(json.dumps({'name': 'test1', 'id': 1}))
        data = json.loads(backendApi.getPolygons())
        assert(len(data) == 1)
        assert(data[0]['name'] == 'test1')

    def test_BackendApi_CreatePolygonWithGeom(self):
        backendApi = BackendApi(connectionString)
        backendApi.createOrUpdatePolygon(json.dumps({'name': 'test0', 'geom': sgPolygon(self.sgPolygonPoints).wkt}))
        data = json.loads(backendApi.getPolygons())
        assert(len(data) == 1)
        assert(data[0]['name'] == 'test0')
        assert(data[0]['geom'] == sgPolygon(self.sgPolygonPoints).wkt)

    def test_BackendApi_updatePolygonWithGeom(self):
        backendApi = BackendApi(connectionString)
        backendApi.createOrUpdatePolygon(json.dumps({'name': 'test0'}))
        data = json.loads(backendApi.getPolygons())
        assert(len(data) == 1)
        assert(data[0]['name'] == 'test0')
        assert(data[0]['geom'] is None)
        backendApi.createOrUpdatePolygon(json.dumps({'name': 'test0', 'id': 1, 'geom': sgPolygon(self.sgPolygonPoints).wkt}))
        data = json.loads(backendApi.getPolygons())
        assert(len(data) == 1)
        assert(data[0]['name'] == 'test0')
        assert(data[0]['geom'] == sgPolygon(self.sgPolygonPoints).wkt)

    def test_BackendApi_deletePolygon(self):
        backendApi = BackendApi(connectionString)
        backendApi.createOrUpdatePolygon(json.dumps({'name': 'test0'}))
        data = json.loads(backendApi.getPolygons())
        print(data)
        assert(len(data) == 1)
        assert(data[0]['name'] == 'test0')
        assert(data[0]['id'] == 1)
        backendApi.deletePolygon(json.dumps({'id': 1}))
        data = json.loads(backendApi.getPolygons())
        assert(len(data) == 0)

    def test_BackendApi_getPolygons(self):
        backendApi = BackendApi(connectionString)
        backendApi.createOrUpdatePolygon(json.dumps({'name': 'test0'}))
        data = json.loads(backendApi.getPolygons())
        assert(len(data) == 1)
        assert(data[0]['name'] == 'test0')

    def test_BackendApi_deleteAllPolygons(self):
        backendApi = BackendApi(connectionString)
        backendApi.createOrUpdatePolygon(json.dumps({'name': 'test0'}))
        data = json.loads(backendApi.getPolygons())
        assert(len(data) == 1)
        backendApi.deleteAllPolygons()
        data = json.loads(backendApi.getPolygons())
        assert(len(data) == 0)

    def test_BackendApi_deleteAllPolygons_several(self):
        backendApi = BackendApi(connectionString)
        backendApi.createOrUpdatePolygon(json.dumps({'name': 'test0'}))
        backendApi.createOrUpdatePolygon(json.dumps({'name': 'test1'}))
        data = json.loads(backendApi.getPolygons())
        assert(len(data) == 2)
        backendApi.deleteAllPolygons()
        data = json.loads(backendApi.getPolygons())
        assert(len(data) == 0)
