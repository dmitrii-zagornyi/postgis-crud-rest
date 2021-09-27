import json
import os
from nose.tools import assert_equals, nottest
from shapely.geometry import Polygon as sgPolygon
from sqlalchemy.ext.declarative import declarative_base

from postgis_crud_rest.api import Api as BackendApi
from postgis_crud_rest.api import Singleton
from postgis_crud_rest.api import Status
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
        assert len(data) == 0
        return

    def teardown(self):
        backendApi = BackendApi(connectionString)
        Polygon.__table__.drop(backendApi._engine)  # Need for reset id counter
        del backendApi
        Singleton._instances.clear()
        return

    def test_api_init(self):
        backendApi = BackendApi(connectionString)
        print(backendApi.getPolygons())
        return

    def test_api_create_one_polygon(self):
        backendApi = BackendApi(connectionString)
        status = backendApi.createOrUpdatePolygon(json.dumps({'name': 'test0'}))
        assert status == Status.Created, f'Status: {status}'
        data = json.loads(backendApi.getPolygons())
        assert len(data) == 1
        assert data[0]['name'] == 'test0'
        return

    def test_api_create_two_polygons(self):
        backendApi = BackendApi(connectionString)
        status = backendApi.createOrUpdatePolygon(json.dumps({'name': 'test0'}))
        assert status == Status.Created, f'Status: {status}'
        data = json.loads(backendApi.getPolygons())
        assert len(data) == 1
        assert data[0]['name'] == 'test0'
        status = backendApi.createOrUpdatePolygon(json.dumps({'name': 'test1'}))
        assert status == Status.Created, f'Status: {status}'
        data = json.loads(backendApi.getPolygons())
        assert len(data) == 2
        assert data[0]['name'] == 'test0'
        assert data[1]['name'] == 'test1'
        return

    def test_api_update_polygon(self):
        backendApi = BackendApi(connectionString)
        status = backendApi.createOrUpdatePolygon(json.dumps({'name': 'test0', 'id': 1}))
        assert status == Status.Created, f'Status: {status}'
        data = json.loads(backendApi.getPolygons())
        assert len(data) == 1
        assert data[0]['name'] == 'test0'
        status = backendApi.createOrUpdatePolygon(json.dumps({'name': 'test1', 'id': 1}))
        assert status == Status.Updated, f'Status: {status}'
        data = json.loads(backendApi.getPolygons())
        assert len(data) == 1
        assert data[0]['name'] == 'test1'
        return

    def test_api_create_polygon_with_geom(self):
        backendApi = BackendApi(connectionString)
        backendApi.createOrUpdatePolygon(json.dumps({'name': 'test0', 'geom': sgPolygon(self.sgPolygonPoints).wkt}))
        data = json.loads(backendApi.getPolygons())
        assert len(data) == 1
        assert data[0]['name'] == 'test0'
        assert data[0]['geom'] == sgPolygon(self.sgPolygonPoints).wkt
        return

    def test_api_update_polygon_with_geom(self):
        backendApi = BackendApi(connectionString)
        backendApi.createOrUpdatePolygon(json.dumps({'name': 'test0'}))
        data = json.loads(backendApi.getPolygons())
        assert len(data) == 1
        assert data[0]['name'] == 'test0'
        assert data[0]['geom'] is None
        backendApi.createOrUpdatePolygon(json.dumps({
            'name': 'test0',
            'id': 1,
            'geom': sgPolygon(self.sgPolygonPoints).wkt}))
        data = json.loads(backendApi.getPolygons())
        assert len(data) == 1
        assert data[0]['name'] == 'test0'
        assert data[0]['geom'] == sgPolygon(self.sgPolygonPoints).wkt
        return

    def test_api_delete_polygon(self):
        backendApi = BackendApi(connectionString)
        status = backendApi.createOrUpdatePolygon(json.dumps({'name': 'test0'}))
        assert status == Status.Created, f'Status: {status}'
        data = json.loads(backendApi.getPolygons())
        assert len(data) == 1
        assert data[0]['name'] == 'test0'
        assert data[0]['id'] == 1
        status = backendApi.deletePolygon(json.dumps({'id': 1}))
        assert status == Status.Deleted, f'Status: {status}'
        data = json.loads(backendApi.getPolygons())
        assert len(data) == 0
        return

    def test_api_get_polygons(self):
        backendApi = BackendApi(connectionString)
        backendApi.createOrUpdatePolygon(json.dumps({'name': 'test0'}))
        data = json.loads(backendApi.getPolygons())
        assert len(data) == 1
        assert data[0]['name'] == 'test0'
        return

    def test_api_get_polygons_srid(self):
        # ToDo: need more clear understanding difference between srid's for better coverage
        backendApi = BackendApi(connectionString)
        backendApi.createOrUpdatePolygon(json.dumps({'name': 'test0', 'geom': sgPolygon(self.sgPolygonPoints).wkt}))
        data = json.loads(backendApi.getPolygons(json.dumps({'srid': 32644})))
        assert len(data) == 1
        assert data[0]['name'] == 'test0'
        return

    def test_api_delete_all_polygons_one(self):
        backendApi = BackendApi(connectionString)
        status = backendApi.createOrUpdatePolygon(json.dumps({'name': 'test0'}))
        assert status == Status.Created, f'Status: {status}'
        data = json.loads(backendApi.getPolygons())
        assert len(data) == 1
        status = backendApi.deleteAllPolygons()
        assert status == Status.Deleted, f'Status: {status}'
        data = json.loads(backendApi.getPolygons())
        assert len(data) == 0
        return

    def test_api_delete_all_polygons_several(self):
        backendApi = BackendApi(connectionString)
        backendApi.createOrUpdatePolygon(json.dumps({'name': 'test0'}))
        backendApi.createOrUpdatePolygon(json.dumps({'name': 'test1'}))
        data = json.loads(backendApi.getPolygons())
        assert len(data) == 2
        status = backendApi.deleteAllPolygons()
        assert status == Status.Deleted
        data = json.loads(backendApi.getPolygons())
        assert len(data) == 0
        return
