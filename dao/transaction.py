'''
    created on 04 January 2020
    
    @author: Gergely
'''
import json
import logging
import time

from dao.db import DeleteOperation, DbConnectionHelper, SelectOperation, InsertOperation
from tables.entry_types import TransactionTableEntry, WaitForGraphEntry, LockTableEntry, TransactionStatus
from tables.synced import SynchronizedTable
from threading import Condition

logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-9s) %(message)s')


class Transaction:
    TRANSACTIONS = SynchronizedTable()
    LOCKS = SynchronizedTable(Condition())
    WAIT_FOR_GRAPH = SynchronizedTable()
    ID = 0

    def __init__(self, operations):
        self.operations = operations
        self.id = Transaction.ID
        Transaction.ID += 1

        self.logger = logging.getLogger(f'.transaction[{self.id}]')
        self.logger.setLevel(logging.DEBUG)

        self.nuke_operations = []
        self.backup_log_file = f'backup_tr_{self.id}.json'
        self._save_backup_data()
        self.transaction_table_entry = TransactionTableEntry(id=self.id,
                                                             timestamp=time.time(),
                                                             status=TransactionStatus.ACTIVE.value)
        self.TRANSACTIONS.append(self.transaction_table_entry)

    def _save_backup_data(self):
        # save in a set every table name along with the db it belongs to
        working_tables = {(operation.connection_params.db_name, operation.table_name) for operation in self.operations
                          if not operation.is_select}

        # prepare afferent select operations to save the data
        backup_operations = [SelectOperation(DbConnectionHelper(db_name=pair[0]), table_name=pair[1])
                             for pair in working_tables]

        self.nuke_operations = [DeleteOperation(DbConnectionHelper(db_name=pair[0]), table_name=pair[1])
                                for pair in working_tables]

        backup_data = {operation.get_resource_id(): operation.execute() for operation in backup_operations}
        self.logger.info(f'Backup Data {backup_data}')

        with open(self.backup_log_file, 'w+') as f:
            json.dump(backup_data, f)

    def rollback(self):
        for op in self.nuke_operations:
            op.execute()
        self.logger.warning(f'Rolling Back {self.id}')
        with open(self.backup_log_file, 'r') as f:
            data = json.load(f)
            for entry in data:
                db_name, table_name = entry.split('$')
                for row in data[entry]:
                    params = {str(i): row[i] for i in range(1, len(row))}
                    op = InsertOperation(DbConnectionHelper(db_name),
                                         table_name,
                                         params=params,
                                         is_explicit=False)
                    op.execute()

    def abort(self):
        self.LOCKS.delete(transaction=self.id)
        self.WAIT_FOR_GRAPH.delete(trans_waits_lock=self.id, trans_has_lock=self.id)
        self.TRANSACTIONS.update(self.transaction_table_entry,
                                 self.transaction_table_entry._replace(status=TransactionStatus.ABORTED))

    def execute(self):
        # block all resources
        for operation in self.operations:
            op_key = operation.get_resource_id()
            lock_type = 'write' if not operation.is_select else 'read'
            locked_elem = self.LOCKS.get(locked_object=op_key)
            # TODO implement lock compatibility check
            if locked_elem:
                trans_has_lock = locked_elem[0].transaction
                self.logger.warning(f'Waiting for transaction {trans_has_lock}')
                self.WAIT_FOR_GRAPH.append(
                    WaitForGraphEntry(lock_type=lock_type,
                                      locked_table=operation.table_name,
                                      locked_object=operation.key,
                                      trans_waits_lock=self.id,
                                      trans_has_lock=trans_has_lock))

            while self.LOCKS.contains(locked_object=op_key):
                self.LOCKS.condition.wait()

            self.LOCKS.append(LockTableEntry(id=0,
                                             type=lock_type,
                                             record_id=op_key,
                                             transaction=self.id,
                                             table=operation.table_name))

            # if the lock was acquired, we no longer wait for anyone
            self.WAIT_FOR_GRAPH.delete(lock_type=lock_type,
                                       locked_table=operation.table_name,
                                       locked_object=operation.key,
                                       trans_waits_lock=self.id)

        for operation in self.operations:
            operation.execute()
        # TODO unlock in reverse order
        self.LOCKS.delete(transaction=self.id)

        # commit
        commit_entry = self.transaction_table_entry._replace(status=TransactionStatus.COMMITTED)
        self.TRANSACTIONS.update(old_elem=self.transaction_table_entry,
                                 new_elem=commit_entry)
        logging.info(f'Transaction {self.id} committed')


'''
connection = DbConnectionHelper('MovieRental')
connection_aop = DbConnectionHelper('aop')

update_op = UpdateOperation(connection, 'client', key=12, params={'email': 'ahoy@mail'})
insert_op = InsertOperation(connection, 'client', key=12,
            params={'name': 'once again', 'email': 'hot@mail', 'age': 22},
            is_explicit=False)
delete_op = DeleteOperation(connection_aop, 'my_entity')
select_op = SelectOperation(connection_aop, 'candidates')

transaction = Transaction([update_op, insert_op, delete_op, select_op])
# transaction.rollback()
# print(transaction.rollback())
# print(insert_op._build_sql())
# print(delete_op.execute())
'''
