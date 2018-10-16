# `nvgpu` - NVIDIA GPU tools

It provides information about GPUs and their availability for computation.

Often we want to train a ML model on one of GPUs installed on a multi-GPU
machine. Since TensorFlow allocates all memory, only one such process can
use the GPU at a time. Unfortunately `nvidia-smi` provides only a text
interface with information about GPUs. This packages wraps it with an
easier to use CLI and Python interface.

It's a quick and dirty solution calling `nvidia-smi` and parsing its output.
We can take one or more GPUs availabile for computation based on relative
memory usage, ie. it is OK with Xorg taking a few MB.

In addition we have a fancy table of GPU with more information taken by
python binding to NVML.

For easier monitoring of multiple machines it's possible to deploy agents (that
provide the GPU information in JSON over a REST API) and show the aggregated
status in a web application.

## Installing

```
pip install nvgpu
```

## Usage examples

Command-line interface:

```
# grab all available GPUs
CUDA_VISIBLE_DEVICES=$(nvgpu available)

# grab at most available GPU
CUDA_VISIBLE_DEVICES=$(nvgpu available -l 1)
```

Print pretty colored table of devices, availability, users, processes:

```
$ nvgpu list
    status    type                 util.      temp.    MHz  users    since    pids    cmd
--  --------  -------------------  -------  -------  -----  -------  ---------------  ------  --------
 0  [ ]       GeForce GTX 1070      0 %          44    139                          
 1  [~]       GeForce GTX 1080 Ti   0 %          44    139  alice    2 days ago       19028   jupyter
 2  [~]       GeForce GTX 1080 Ti   0 %          44    139  bob      14 hours ago     8479    jupyter
 3  [~]       GeForce GTX 1070     46 %          54   1506  bob      7 days ago       20883   train.py
 4  [~]       GeForce GTX 1070     35 %          64   1480  bob      7 days ago       26228   evaluate.py
 5  [!]       GeForce GTX 1080 Ti   0 %          44    139  ?                         9305
 6  [ ]       GeForce GTX 1080 Ti   0 %          44    139
```

Or shortcut:

```
$ nvl
```

Python API:

```
import nvgpu

nvgpu.available_gpus()
# ['0', '2']

nvgpu.gpu_info()
[{'index': '0',
  'mem_total': 8119,
  'mem_used': 7881,
  'mem_used_percent': 97.06860450794433,
  'type': 'GeForce GTX 1070',
  'uuid': 'GPU-3aa99ee6-4a9f-470e-3798-70aaed942689'},
 {'index': '1',
  'mem_total': 11178,
  'mem_used': 10795,
  'mem_used_percent': 96.57362676686348,
  'type': 'GeForce GTX 1080 Ti',
  'uuid': 'GPU-60410ded-5218-7b06-9c7a-124b77a22447'},
 {'index': '2',
  'mem_total': 11178,
  'mem_used': 10789,
  'mem_used_percent': 96.51994990159241,
  'type': 'GeForce GTX 1080 Ti',
  'uuid': 'GPU-d0a77bd4-cc70-ca82-54d6-4e2018cfdca6'},
  ...
]
```

## Web application with agents

There are multiple nodes. Agents take info from GPU and provide it in JSON via
REST API. Master gathers info from other nodes and displays it in a HTML page.
Agents can also display their status by default.

### Agent

```
FLASK_APP=nvgpu.webapp flask run --host 0.0.0.0 --port 1080
```

### Master

Set agents into a config file. Agent is specified either via a URL to a remote
machine or `'self'` for direct access to local machine. Remove `'self'` if the
machine itself does not have any GPU. Default is `AGENTS = ['self']`, so that
agents also display their own status. Set `AGENTS = []` to avoid this.

```
# nvgpu_master.cfg
AGENTS = [
         'self', # node01 - master - direct access without using HTTP
         'http://node02:1080',
         'http://node03:1080',
         'http://node04:1080',
]
```

```
NVGPU_CLUSTER_CFG=/path/to/nvgpu_master.cfg FLASK_APP=nvgpu.webapp flask run --host 0.0.0.0 --port 1080
```

Open the master in the web browser: http://node01:1080.

## Author

- Bohumír Zámečník, [Rossum, Ltd.](https://rossum.ai/)
- License: MIT

## TODO

- dockerize the master/agent webapp for easier deployment
- order GPUs by priority (decreasing power, decreasing free memory)
