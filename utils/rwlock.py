'''
    created on 04 January 2020
    
    @author: Gergely
'''
from contextlib import contextmanager
from threading import Lock


# via https://gist.github.com/tylerneylon/a7ff6017b7a1f9a506cf75aa23eacfd6

class ReadWriteLock:
    def __init__(self):
        self.write_lock = Lock()
        self.read_lock = Lock()
        self.num_readers = 0

    def _read_acquire(self):
        self.read_lock.acquire()
        self.num_readers += 1
        if self.num_readers == 1:
            self.write_lock.acquire()
        self.read_lock.release()

    def _read_release(self):
        assert self.num_readers > 0
        self.read_lock.acquire()
        self.num_readers -= 1
        if self.num_readers == 0:
            self.write_lock.release()
        self.read_lock.release()

    @contextmanager
    def read_acquire(self):
        try:
            self._read_acquire()
            yield
        finally:
            self._read_release()

    @contextmanager
    def write_acquire(self):
        try:
            self.write_lock.acquire()
            yield
        finally:
            self.write_lock.release()
