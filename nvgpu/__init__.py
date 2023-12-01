# nvgpu __init__.py

import re
import subprocess
# import six  # Unused import?


def gpu_info():
    """Parse `nvidia-smi` CLI output to collect Nvidia GPU information."""
    # Ensure that `nvidia-smi` is available and finds GPUs before proceeding.
    try:
        gpus = [line.strip() for line in _run_cmd(["nvidia_smi", "-L"]) if line]
    except (FileNotFoundError, subprocess.CalledProcessError):
        return []

    # Manage output according to whether Nvidia MIG devices are enabled or not
    mig_mode = _run_cmd(
        ["nvidia-smi", "--query-gpu=mig.mode.current", "--format=csv,noheader"]
        )[0]
    if mig_mode == "Enabled":
        re_gpu = "(.+?)\s{1,}Device\s{1,}([0-9]+): \(UUID: ([^)]+)\)"  # Match strings like 'MIG 1g.5gb Device 0: (UUID: MIG-GPU-6482a92e-d06b-dc68-c272-e3d8f7ecabbf/7/0)'
        re_match_order = ("type", "index", "uuid")
        gpus = [
            line for line in gpus if not line.startswith("GPU")
        ]  # Update to avoid physical GPUs (only count virtual MIG devices)
    else:
        re_gpu = "GPU ([0-9]+): (.+?) \(UUID: ([^)]+)\)"  # Match strings like 'GPU 0: NVIDIA A100 80GB PCIe (UUID: GPU-84ccface-663f-f5fd-8e8e-109d0f78bd2f)'
        re_match_order = ("index", "type", "uuid")

    gpu_infos = [re.match(re_gpu, gpu) for gpu in gpus]
    gpu_infos = [info.groups() for info in gpu_infos if info is not None]
    gpu_infos = [dict(zip(re_match_order, info)) for info in gpu_infos]
    gpu_count = len(gpus)

    lines = _run_cmd(["nvidia-smi"])
    cuda_version = float(lines[2].split("CUDA Version: ")[1].split(" ")[0])

    if cuda_version < 11:
        line_distance = 3
        selected_lines = lines[7 : 7 + line_distance * gpu_count]
    else:
        if mig_mode == "Enabled":
            line_distance = 2
            selected_lines = lines[19 : 19 + line_distance * gpu_count]
        else:
            line_distance = 4
            selected_lines = lines[8 : 8 + line_distance * gpu_count]

    for i in range(gpu_count):
        mem_used, mem_total = [
            int(m.strip().replace("MiB", ""))
            for m in selected_lines[line_distance * i + 1]
            .split("|")[2]
            .strip()
            .split("/")
        ]
        gpu_infos[i]["mem_used"] = mem_used
        gpu_infos[i]["mem_total"] = mem_total
        gpu_infos[i]["mem_used_percent"] = 100.0 * mem_used / mem_total

    return gpu_infos


def _run_cmd(cmd):
    output = subprocess.check_output(cmd)
    if isinstance(output, bytes):
        output = output.decode("UTF-8")
    return output.split("\n")


def available_gpus(max_used_percent=20.0):
    gpus = gpu_info()
    if gpus:
        return [gpu["index"] for gpu in gpus if gpu["mem_used_percent"] <= max_used_percent]
    return []
