from setuptools import setup

setup(name='nvgpu',
    version='0.7.0',
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
        # works only in Python 2
        'nvidia-ml-py',
        'pandas',
        'psutil',
        'requests',
        'termcolor',
        'tabulate',
    ],
    setup_requires=['setuptools-markdown'],
    long_description_markdown_filename='README.md',
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

        'Operating System :: POSIX :: Linux',
    ],
    entry_points={
        'console_scripts': [
            'nvgpu = nvgpu.__main__:main',
            'nvl = nvgpu.list_gpus:pretty_list_gpus'
        ]
    }, )
