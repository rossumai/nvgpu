test:
	nosetests

install:
	pip install nvgpu

install_dev:
	pip install -e .

uninstall:
	pip uninstall nvgpu

clean:
	rm -r build/ dist/ nvgpu.egg-info/

# twine - a tool for uploading packages to PyPI
install_twine:
	pip install twine

build:
	python setup.py sdist
	python setup.py bdist_wheel --universal

# PyPI production

publish:
	twine upload dist/*

docker_build:
	docker build -t nvgpu .

docker_run_nvl:
	nvidia-docker run --rm nvgpu nvl
#
#docker_run_agent:
#	nvidia-docker run --rm -p 1080:80 nvgpu
#
#docker_run_master:
#	nvidia-docker run --rm -p 1080:80 -v $(pwd)/nvgpu_master.cfg:/etc/nvgpu.cfg nvgpu
