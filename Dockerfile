# TODO: We need only NVML, not whole CUDA.
FROM nvidia/cuda:9.0-base

MAINTAINER Bohumir Zamecnik (bohumir.zamecnik@rossum.ai)

# TODO: Use a separate build image and don't put GCC into the final image.
RUN apt update && apt install -y python-pip python-setuptools python-dev gcc

RUN pip install wheel

# install the app from sources
WORKDIR /root/nvgpu
COPY . ./
RUN pip install --no-cache-dir .

ENV FLASK_APP nvgpu.webapp
ENV NVGPU_CLUSTER_CFG /etc/nvgpu.cfg
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "80"]
