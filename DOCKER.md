## Installation and running via Docker

<dev>For easier deployment of the agent apps we can use Docker.</del>

> `psutils` cannot see process details (user, creation time, command) on the host
OS - by definition os container this is separated. This is a design fault of the
dockerized solution and I'm not sure if it can work at all.
See https://github.com/rossumai/nvgpu/issues/2.

It needs [nvidia-docker](https://github.com/NVIDIA/nvidia-docker) installed.

```bash
# build the image
docker build -t nvgpu .

# run CLI
nvidia-docker run --rm nvgpu nvl

# run agent
nvidia-docker run --rm -p 1080:80 nvgpu

# run the master with agents specified in ~/nvgpu_master.cfg
nvidia-docker run --rm -p 1080:80 -v $(pwd)/nvgpu_master.cfg:/etc/nvgpu.cfg nvgpu

open http://localhost:1080
```

You can set the containers for automatic startup with `--restart always` option.

Note: Docker containers have some hash as hostname (it's not the host machine hostname).
