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
                                   'status '
                                   'ref')

WaitForGraphEntry = namedtuple('WaitForGraphEntry',
                               'lock_type '
                               'locked_table '
                               'locked_object '
                               'trans_has_lock '
                               'trans_waits_lock')
