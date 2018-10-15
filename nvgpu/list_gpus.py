from __future__ import print_function

import arrow
import pandas as pd
import psutil
import pynvml as nv
from tabulate import tabulate
from termcolor import colored

from nvgpu.nvml import nvml_context


def device_status(device_index):
    handle = nv.nvmlDeviceGetHandleByIndex(device_index)
    device_name = nv.nvmlDeviceGetName(handle)
    nv_procs = nv.nvmlDeviceGetComputeRunningProcesses(handle)
    utilization = nv.nvmlDeviceGetUtilizationRates(handle).gpu
    clock_mhz = nv.nvmlDeviceGetClock(handle, nv.NVML_CLOCK_SM, 0)
    temperature = nv.nvmlDeviceGetTemperature(handle, nv.NVML_TEMPERATURE_GPU)
    pids = []
    users = []
    dates = []
    cmd = None
    for nv_proc in nv_procs:
        pid = nv_proc.pid
        pids.append(pid)
        try:
            proc = psutil.Process(pid)
            users.append(proc.username())
            dates.append(proc.create_time())
            if cmd is None:
                cmd = parse_cmd_roughly(proc.cmdline())
        except psutil.NoSuchProcess:
            users.append('?')
    return {
        'type': device_name,
        'is_available': len(pids) == 0,
        'pids': ','.join([str(pid) for pid in pids]),
        'users': ','.join(users),
        'running_since': arrow.get(min(dates)).humanize() if len(dates) > 0 else None,
        'utilization': utilization,
        'clock_mhz': clock_mhz,
        'temperature': temperature,
        'cmd': cmd,
        }

def parse_cmd_roughly(args):
    cmdline = ' '.join(args)
    if 'python -m ipykernel_launcher' in cmdline:
        return 'jupyter'
    python_script = [arg for arg in args if arg.endswith('.py')]
    if len(python_script) > 0:
        return python_script[0]
    else:
        return cmdline if len(cmdline) <= 25 else cmdline[:25] + '...'

def device_statuses():
    with nvml_context():
        device_count = nv.nvmlDeviceGetCount()
        return [device_status(device_index) for device_index in range(device_count)]

def device_table(rows):
    df = pd.DataFrame(rows, columns=[
        'is_available', 'type', 'utilization', 'clock_mhz', 'temperature', 'users', 'running_since', 'pids', 'cmd'
    ])
    return df

def format_table(df):
    def make_status(row):
        if row['users'] == '?':
            return '[!]'
        elif row['is_available']:
            return '[ ]'
        else:
            return '[~]'
    def color_by_status(status):
        if status == '[ ]':
            return 'green'
        elif status == '[~]':
            return 'blue'
        elif status == '[!]':
            return 'red'
        else:
            raise ValueError(status)
    df['status'] = df.apply(make_status, axis=1)
    df['color'] = df['status'].apply(color_by_status)
    df['util.'] = df['utilization'].apply(lambda u: '%03s %%' % u)
    df['MHz'] = df['clock_mhz']
    df['temp.'] = df['temperature']
    df['since'] = df['running_since']
    for col in ['since', 'cmd']:
        df[col] = df[col].apply(lambda v: v if v is not None else '')
    cols = ['status', 'type', 'util.', 'temp.', 'MHz', 'users', 'since', 'pids', 'cmd']
    for col in cols:
        df[col] = [colored(row[col], row['color']) for i, row in df.iterrows()]
    df = df[[col for col in cols if col not in ['color']]]
    return tabulate(df, headers='keys')

def pretty_list_gpus():
    rows = device_statuses()
    df = device_table(rows)
    print(format_table(df))


if __name__ == '__main__':
    pretty_list_gpus()
