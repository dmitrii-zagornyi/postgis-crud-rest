import os
import signal
import subprocess
import time


class test_rest():
    def setup(self):
        self.flaskServer = subprocess.Popen(['python', 'rest.py'])
        time.sleep(2)

    def teardown(self):
        os.kill(self.flaskServer.pid, signal.SIGTERM)
        
    def test_smole(self):
        os.system('curl http://127.0.0.1:5000/api/get_polygons')
