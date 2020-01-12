'''
    created on 04 January 2020
    
    @author: Gergely
'''
from tables.tables import SynchronizedTable, TransactionTableEntry, WaitForGraphEntry, LockTableEntry
from dao.repo import DbOperation, DeleteOperation, DbConnectionHelper
from itertools import product


class Transaction:
    TRANSACTIONS = SynchronizedTable()
    LOCKS = SynchronizedTable()
    WAIT_FOR_GRAPH = SynchronizedTable()

    def __init__(self, operations, id):
        self.operations = operations
        self.id = id

        db_names = {operation.db_name for operation in operations}
        table_names = {operation.table_name for operation in operations}
        data_backup_keys = product(db_names, table_names)
        delete_operations = [DeleteOperation(DbConnectionHelper(tup[0]), tup[1])
                             for tup in data_backup_keys]
        insert_operations = []

    def rollback(self):
        pass

    def execute(self):
        for operation in self.operations:
            op_key = operation.key
            lock_type = 'write' if not operation.is_select else 'read'
            if op_key in self.LOCKS:
                self.WAIT_FOR_GRAPH[op_key] = WaitForGraphEntry(lock_type=lock_type,
                                                                locked_table=operation.table_name,
                                                                locked_object=operation.key,
                                                                trans_has_lock=self.LOCKS[op_key].transaction)
