'''
    created on 04 January 2020
    
    @author: Gergely
'''
from collections import namedtuple
from threading import Lock
from enum import Enum


class TransactionStatus(Enum):
    ACTIVE = 'active',
    ABORTED = 'aborted',
    COMMITTED = 'committed'


LockTableEntry = namedtuple('LockTableEntry',
                            'id '
                            'type '
                            'record_id '
                            'table '
                            'transaction')

TransactionTableEntry = namedtuple('TransactionTableEntry',
                                   'id '
                                   'timestamp '
                                   'status')

WaitForGraphEntry = namedtuple('WaitForGraphEntry',
                               'lock_type '
                               'locked_table '
                               'locked_object '
                               'trans_has_lock '
                               'trans_waits_lock')


class SynchronizedTable:
    def __init__(self):
        self.elems = []
        self.lock = Lock()

    @staticmethod
    def _check(op, params):
        return all([hasattr(op, arg) and getattr(op, arg, False) == params[arg] for arg in params])

    def append(self, elem):
        with self.lock:
            self.elems.append(elem)

    def get(self, **kwargs):
        with self.lock:
            return list(filter(lambda x: self._check(x, kwargs), self.elems))

    def contains(self, **kwargs):
        assert len(kwargs) > 0
        with self.lock:
            return len(list(filter(lambda x: self._check(x, kwargs), self.elems))) > 0

    def delete(self, **kwargs):
        assert len(kwargs) > 0
        with self.lock:
            self.elems = list(filter(lambda x: not self._check(x, kwargs), self.elems))


'''
t = SynchronizedTable()

t.append(TransactionTableEntry(id=0, status='active', timestamp=0))
t.append(TransactionTableEntry(id=1, status='active', timestamp=11))
t.append(TransactionTableEntry(id=2, status='active', timestamp=1))
t.append(TransactionTableEntry(id=3, status='committed', timestamp=0))
print(t.contains(id=3, status='active'))
print(t.delete(status='active'))
'''
