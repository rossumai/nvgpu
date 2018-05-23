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
    pids = []
    users = []
    dates = []
    for nv_proc in nv_procs:
        pid = nv_proc.pid
        pids.append(pid)
        try:
            proc = psutil.Process(pid)
            users.append(proc.username())
            dates.append(proc.create_time())
        except psutil._exceptions.NoSuchProcess:
            users.append('?')
    return {
        'type': device_name,
        'is_available': len(pids) == 0,
        'pids': ','.join([str(pid) for pid in pids]),
        'users': ','.join(users),
        'running_since': arrow.get(min(dates)).humanize() if len(dates) > 0 else None,
        'utilization': utilization
    }

def device_table():
    with nvml_context():
        device_count = nv.nvmlDeviceGetCount()
        rows = [device_status(device_index) for device_index in range(device_count)]
        df = pd.DataFrame(rows, columns=['is_available', 'type', 'utilization', 'users', 'running_since', 'pids'])
        return df

def pretty_list_gpus():
    df = device_table()
    df['status'] = df['is_available'].apply(lambda a: '[ ]' if a else '[~]')
    df['util.'] = df['utilization'].apply(lambda u: '%02s %%' % u)
    for col in ['status', 'type', 'util.', 'users', 'running_since', 'pids']:
        df[col] = [colored(row[col], 'green') if row['is_available'] else colored(row[col], 'red') for i, row in df.iterrows()]
    df = df[['status', 'type', 'util.', 'users', 'running_since', 'pids']]
    print(tabulate(df, headers='keys'))

if __name__ == '__main__':
    pretty_list_gpus()
