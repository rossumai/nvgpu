from setuptools import setup


def read_file(path):
    with open(path, 'r') as f:
        return f.read()


setup(name='nvgpu',
    version='0.10.0',
    description='NVIDIA GPU tools',
    url='https://github.com/rossumai/nvgpu',
    author='Bohumir Zamecnik, Rossum',
    author_email='bohumir.zamecnik@rossum.ai',
    license='MIT',
    packages=['nvgpu'],
    zip_safe=False,
    install_requires=[
        'ansi2html',
        'arrow',
        'flask',
        'flask_restful',
        'nvidia-ml-py; python_version < "3"',
        'nvidia-ml-py3; python_version >= "3" and python_version < "3.6"',
        'pynvml; python_version >= "3.6"',
        'pandas',
        'psutil',
        'requests',
        'six',
        'termcolor',
        'tabulate',
    ],
    long_description=read_file('README.md'),
    long_description_content_type="text/markdown",
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',

        'Operating System :: POSIX :: Linux',
    ],
    entry_points={
        'console_scripts': [
            'nvgpu = nvgpu.__main__:main',
            'nvl = nvgpu.list_gpus:pretty_list_gpus'
        ]
    }, )
