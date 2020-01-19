'''
    created on 04 January 2020
    
    @author: Gergely
'''
from tables.tables import SynchronizedTable, TransactionTableEntry, WaitForGraphEntry, LockTableEntry
from dao.repo import DbOperation, DeleteOperation, DbConnectionHelper, SelectOperation, UpdateOperation, InsertOperation
import json

import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Transaction:
    TRANSACTIONS = SynchronizedTable()
    LOCKS = SynchronizedTable()
    WAIT_FOR_GRAPH = SynchronizedTable()
    ID = 0

    def __init__(self, operations):
        self.operations = operations
        self.id = Transaction.ID
        Transaction.ID += 1
        self.nuke_operations = []
        self.backup_log_file = f'backup_trw_{self.id}.json'
        self._save_backup_data()

    def _save_backup_data(self):
        # save in a set every table name along with the db it belongs to
        working_tables = {(operation.connection_params.db_name, operation.table_name) for operation in self.operations}

        # prepare afferent select operations to save the data
        backup_operations = [SelectOperation(DbConnectionHelper(db_name=pair[0]), table_name=pair[1])
                             for pair in working_tables]

        self.nuke_operations = [DeleteOperation(DbConnectionHelper(db_name=pair[0]), table_name=pair[1])
                                for pair in working_tables]

        backup_data = {operation.get_resource_id(): operation.execute() for operation in backup_operations}

        with open(self.backup_log_file, 'w+') as f:
            json.dump(backup_data, f)

    def rollback(self):
        for op in self.nuke_operations:
            op.execute()
        logger.warning(f'Rolling back Transaction {self.id}')
        with open(self.backup_log_file, 'r') as f:
            data = json.load(f)
            for entry in data:
                db_name, table_name = entry.split('$')
                for row in data[entry]:
                    params = {str(i): row[i] for i in range(1, len(row))}
                    op = InsertOperation(DbConnectionHelper(db_name),
                                         table_name,
                                         params=params,
                                         key=row[0],
                                         is_explicit=False)
                    op.execute()
                    print(op._build_sql())

    def execute(self):
        for operation in self.operations:
            op_key = operation.key
            lock_type = 'write' if not operation.is_select else 'read'
            if op_key in self.LOCKS:
                self.WAIT_FOR_GRAPH[op_key] = WaitForGraphEntry(lock_type=lock_type,
                                                                locked_table=operation.table_name,
                                                                locked_object=operation.key,
                                                                trans_has_lock=self.LOCKS[op_key].transaction)


connection = DbConnectionHelper('MovieRental')
connection_aop = DbConnectionHelper('aop')

update_op = UpdateOperation(connection, 'client', key=12, params={'email': 'ahoy@mail'})
insert_op = InsertOperation(connection, 'client', key=12,
                            params={'name': 'once again', 'email': 'hot@mail', 'age': 22}, is_explicit=False)
delete_op = DeleteOperation(connection_aop, 'my_entity')
select_op = SelectOperation(connection_aop, 'candidates')

transaction = Transaction([update_op, insert_op, delete_op, select_op])
#transaction.rollback()
# print(transaction.rollback())
# print(insert_op._build_sql())
# print(delete_op.execute())
