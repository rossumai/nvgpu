import re
import subprocess


def gpu_info():
    gpus = [line for line in subprocess.check_output(['nvidia-smi', '-L']).split('\n') if line]
    gpu_infos = [re.match('GPU ([0-9]+): ([^(]+) \(UUID: ([^)]+)\)', gpu).groups() for gpu in gpus]
    gpu_infos = [dict(zip(['index', 'type', 'uuid'], info)) for info in gpu_infos]
    gpu_count = len(gpus)

    lines = subprocess.check_output(['nvidia-smi']).split('\n')
    selected_lines = lines[7:7 + 3 * gpu_count]
    for i in range(gpu_count):
        mem_used, mem_total = [int(m.strip().replace('MiB', '')) for m in
                               selected_lines[3 * i + 1].split('|')[2].strip().split('/')]
        gpu_infos[i]['mem_used'] = mem_used
        gpu_infos[i]['mem_total'] = mem_total
        gpu_infos[i]['mem_used_percent'] = 100. * mem_used / mem_total

    return gpu_infos


def available_gpus(max_used_percent=20.):
    return [gpu['index'] for gpu in gpu_info() if gpu['mem_used_percent'] <= max_used_percent]
