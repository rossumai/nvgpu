from contextlib import contextmanager

from pynvml import nvmlInit, nvmlShutdown

@contextmanager
def nvml_context():
    nvmlInit()
    yield
    nvmlShutdown()
