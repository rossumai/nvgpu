from ansi2html import Ansi2HTMLConverter
from flask import Flask
from flask import Response
from flask_restful import Resource, Api

from nvgpu.master import gather_reports, format_reports_to_ansi

app = Flask(__name__)
api = Api(app)

agents = ['http://127.0.0.1:1070']


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

api.add_resource(GpuClusterStatusHTML, '/')
api.add_resource(GpuClusterStatus, '/cluster_status')

if __name__ == '__main__':
    app.run(debug=True, port=1080)
