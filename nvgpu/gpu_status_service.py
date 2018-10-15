# Gathers GPU utilization status via 'nvl' command from multiple hosts
# and publishes in via a web app.
#
# FLASK_APP=gpu_status_service.py flask run --host 0.0.0.0 --port 1080

from subprocess import check_output, CalledProcessError

from ansi2html import Ansi2HTMLConverter
from flask import Flask

app = Flask(__name__)

hosts = ['localhost', ] # ...


def gpu_status(host=None):
    if host is not None and host != 'localhost':
        command = ['ssh', host, 'nvl']
        try:
            output = '%s\n%s' % (host, check_output(command))
        except CalledProcessError:
            output = '%s\n\nHost not reachable!' % host
    else:
        output = check_output('hostname') + check_output('nvl')

    # text with ANSI colors
    return output


def gpu_status_all(hosts):
    statuses = []
    for host in hosts:
        statuses.append(gpu_status(host))
    return '\n\n'.join(statuses)


@app.route('/')
def index():
    status = gpu_status_all(hosts)
    conv = Ansi2HTMLConverter(scheme='osx', dark_bg=False)
    html = conv.convert(status)
    html = html.replace(
        '.body_background { background-color: #AAAAAA; }',
        '.body_background { background-color: #FFFFFF; }')
    return html
