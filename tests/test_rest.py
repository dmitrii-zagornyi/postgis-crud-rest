import os
import signal
import subprocess
import time
import requests

import postgis_crud_rest


class test_rest():
    def setup(self):
        self.flaskServer = subprocess.Popen(['python', os.path.join(os.path.dirname(postgis_crud_rest.__file__), 'rest.py')])
        time.sleep(2)

    def teardown(self):
        os.kill(self.flaskServer.pid, signal.SIGTERM)
        
    def test_create_update_get_delete(self):
        r = requests.post("http://127.0.0.1:5000/api/create_polygon", data={'name': 'test', 'id': 1})
        assert r.status_code == 201, 'create_polygon'
        
        r = requests.post("http://127.0.0.1:5000/api/update_polygon", data={'name': 'main', 'id': 1})
        assert r.status_code == 201, 'update_polygon'
        
        r = requests.get("http://127.0.0.1:5000/api/get_polygons")
        assert r.status_code == 200, 'get_polygons'
        
        r = requests.delete("http://127.0.0.1:5000/api/delete_polygon/1")
        assert r.status_code == 200, 'delete_polygon'
