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
