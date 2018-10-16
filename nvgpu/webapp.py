"""
Gathers GPU utilization status via 'nvgpu' library from multiple hosts
and publishes in via a web app.

This web app can act either as an agent (just publishing status of GPUs on one
machine in JSON via REST API) or master (in addition aggregating statuses from
all machines in a cluster and showing them on a HTML page). Master instance can
also act as an agent.

Master:
NVGPU_CLUSTER_CFG=$(pwd)/nvgpu_master.cfg FLASK_APP=nvgpu.webapp flask run --host 0.0.0.0 --port 1080

Agent:
FLASK_APP=nvgpu.webapp flask run --host 0.0.0.0 --port 1080
"""

from ansi2html import Ansi2HTMLConverter
from flask import Flask
from flask import Response
from flask_restful import Resource, Api

from nvgpu.agent import machine_status
from nvgpu.master import gather_reports, format_reports_to_ansi

app = Flask(__name__)
api = Api(app)

app.config.from_envvar('NVGPU_CLUSTER_CFG', silent=True)

# agent is either a URL to another machine or 'self' for direct access
# if no agents specified it will only report its own status
agents = app.config.get('AGENTS', ['self'])


class GpuStatus(Resource):
    def get(self):
        return machine_status()


class GpuClusterStatus(Resource):
    def get(self):
        return gather_reports(agents)


class GpuClusterStatusHTML(Resource):
    def get(self):
        reports = gather_reports(agents)
        ansi_text = format_reports_to_ansi(agents, reports)
        html = ansi_text_to_html(ansi_text)
        return Response(html, mimetype='text/html')


def ansi_text_to_html(text):
    conv = Ansi2HTMLConverter(scheme='osx', dark_bg=False)
    html = conv.convert(text)
    html = html.replace(
        '.body_background { background-color: #AAAAAA; }',
        '.body_background { background-color: #FFFFFF; }')
    return html


# Possibly publish this only if NVML is available on this host.
api.add_resource(GpuStatus, '/gpu_status')
api.add_resource(GpuClusterStatusHTML, '/')
api.add_resource(GpuClusterStatus, '/cluster_status')

if __name__ == '__main__':
    app.run(debug=True, port=1080)
