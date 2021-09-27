import json
import os
import signal
import subprocess
import time
import requests

import postgis_crud_rest


dbConnectionString = os.environ.get('postgresql')
if dbConnectionString is None:
    dbConnectionString = "postgresql://postgres:qazwsx@localhost:5432/postgres"

siteConnectionString = "http://127.0.0.1:5000"


class test_rest():
    @classmethod
    def setup_class(cls):
        cls.flaskServer = subprocess.Popen([
            'python',
            os.path.join(os.path.dirname(postgis_crud_rest.__file__), 'rest.py'),
            f'{dbConnectionString}'])
        time.sleep(1)
        return

    @classmethod
    def teardown_class(cls):
        os.kill(cls.flaskServer.pid, signal.SIGTERM)
        return

    def _check_single_polygon(self, testData):
        response = requests.get(f'{siteConnectionString}/api/get_polygons')
        assert response.status_code == 200, f'get_polygons: {response.status_code}'
        responseData = json.loads(response.text)
        assert len(responseData) == 1
        print(testData)
        print(responseData)
        for key, value in testData.items():
            assert key in responseData[0], f'{key} not exists in response'
            assert responseData[0][key] == value, f'{responseData[key]} != {value}'
        return

    def setup(self):
        response = requests.delete(f'{siteConnectionString}/api/delete_polygons', data={'name': 'test', 'id': 1})
        assert response.status_code == 200, f'delete_polygons: {response.status_code}'
        return

    def test_rest_delete_all(self):
        response = requests.delete(f'{siteConnectionString}/api/delete_polygons', data={'name': 'test', 'id': 1})
        assert response.status_code == 200, f'delete_polygons: {response.status_code}'
        return

    def test_create(self):
        testData = {'name': 'test0'}
        response = requests.post(f'{siteConnectionString}/api/create_polygon', data=testData)
        assert response.status_code == 201, f'create_polygon: {response.status_code}'
        self._check_single_polygon(testData)
        return

    def test_update(self):
        testData = {'name': 'test0', 'id': 1}
        response = requests.post(f'{siteConnectionString}/api/create_polygon', data=testData)
        assert response.status_code == 201, f'create_polygon: {response.status_code}'
        self._check_single_polygon(testData)

        testData['name'] = 'test1'
        response = requests.post(f'{siteConnectionString}/api/update_polygon', data=testData)
        assert response.status_code == 201, f'update_polygon: {response.status_code}'
        self._check_single_polygon(testData)
        return

    def test_get_polygon(self):
        response = requests.get(f'{siteConnectionString}/api/get_polygons')
        assert response.status_code == 200, f'get_polygons: {response.status_code}'
        responseData = json.loads(response.text)
        assert len(responseData) == 0
        return

    def test_delete_polygon(self):
        testId = 1
        testData = {'name': 'test0', 'id': testId}
        response = requests.post(f'{siteConnectionString}/api/create_polygon', data=testData)
        assert response.status_code == 201, f'create_polygon: {response.status_code}'
        self._check_single_polygon(testData)

        response = requests.delete(f'{siteConnectionString}/api/delete_polygon/{str(testData["id"])}')
        assert response.status_code == 200, f'delete_polygon: {response.status_code}'

        response = requests.get(f'{siteConnectionString}/api/get_polygons')
        assert response.status_code == 200, f'get_polygons: {response.status_code}'
        responseData = json.loads(response.text)
        assert len(responseData) == 0
        return
