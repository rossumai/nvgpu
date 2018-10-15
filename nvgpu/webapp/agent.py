from flask import Flask
from flask_restful import Resource, Api
import socket

from nvgpu.list_gpus import device_statuses

app = Flask(__name__)
api = Api(app)

hostname = socket.gethostname()

class GpuStatus(Resource):
    def get(self):
        return {
            'hostname': hostname,
            'gpus': device_statuses()
        }


api.add_resource(GpuStatus, '/gpu_status')

if __name__ == '__main__':
    app.run(debug=True, port=1070)
