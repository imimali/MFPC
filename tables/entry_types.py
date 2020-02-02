'''
    created on 04 January 2020
    
    @author: Gergely
'''
from collections import namedtuple
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

'''
t = SynchronizedTable()

t.append(TransactionTableEntry(id=0, status='active', timestamp=0))
t.append(TransactionTableEntry(id=1, status='active', timestamp=11))
t.append(TransactionTableEntry(id=2, status='active', timestamp=1))
t.append(TransactionTableEntry(id=3, status='committed', timestamp=0))
print(t.contains(id=3, status='active'))
print(t.delete(status='active'))
'''
