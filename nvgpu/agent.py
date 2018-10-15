import socket

from nvgpu.list_gpus import device_statuses

hostname = socket.gethostname()


def machine_status():
    return {
        'hostname': hostname,
        'gpus': device_statuses()
    }
