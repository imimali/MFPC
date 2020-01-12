'''
    created on 04 January 2020
    
    @author: Gergely
'''
from collections import namedtuple
from threading import Lock

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
        self.elems = {}
        self.lock = Lock()

    def __getitem__(self, item):
        with self.lock:
            return self.elems[item]

    def __setitem__(self, key, value):
        with self.lock:
            self.elems[key] = value

    def __contains__(self, item):
        with self.lock:
            return item in self.elems
