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
    available    type                 users    running_since    pids
--  -----------  -------------------  -------  ---------------  ------
 0  [ ]          GeForce GTX 1070              None             
 1  [~]          GeForce GTX 1080 Ti  alice    2 days ago       19028
 2  [~]          GeForce GTX 1080 Ti  bob      13 hours ago     8479
 3  [~]          GeForce GTX 1070     bob      7 days ago       20883
 4  [~]          GeForce GTX 1070     bob      7 days ago       26228
 5  [~]          GeForce GTX 1080 Ti  ?        None             9305
 6  [ ]          GeForce GTX 1080 Ti           None
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

## Author

- Bohumír Zámečník, [Rossum, Ltd.](https://rossum.ai/)
- License: MIT

## TODO
- order GPUs by priority (decreasing power, decreasing free memory)
