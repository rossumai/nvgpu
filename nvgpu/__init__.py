import re
import six
import subprocess


def gpu_info():
    gpus = [line for line in _run_cmd(['nvidia-smi', '-L']) if line]
    gpu_infos = [re.match('GPU ([0-9]+): ([^(]+) \(UUID: ([^)]+)\)', gpu).groups() for gpu in gpus]
    gpu_infos = [dict(zip(['index', 'type', 'uuid'], info)) for info in gpu_infos]
    gpu_count = len(gpus)

    lines = _run_cmd(['nvidia-smi'])
    cuda_version = float(lines[2].split('CUDA Version: ')[1].split(' ')[0])
    if cuda_version < 11:
        line_distance = 3
        selected_lines = lines[7:7 + line_distance * gpu_count]
    else:
        line_distance = 4
        selected_lines = lines[8:8 + line_distance * gpu_count]
    for i in range(gpu_count):
        mem_used, mem_total = [int(m.strip().replace('MiB', '')) for m in
                               selected_lines[line_distance * i + 1].split('|')[2].strip().split('/')]
        gpu_infos[i]['mem_used'] = mem_used
        gpu_infos[i]['mem_total'] = mem_total
        gpu_infos[i]['mem_used_percent'] = 100. * mem_used / mem_total

    return gpu_infos


def _run_cmd(cmd):
    output = subprocess.check_output(cmd)
    if six.PY3:
        output = output.decode('UTF-8')
    return output.split('\n')

def available_gpus(max_used_percent=20.):
    return [gpu['index'] for gpu in gpu_info() if gpu['mem_used_percent'] <= max_used_percent]
