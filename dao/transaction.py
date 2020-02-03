'''
    created on 04 January 2020
    
    @author: Gergely
'''
import json
import logging
import time

from dao.db import DeleteOperation, DbConnectionHelper, SelectOperation, InsertOperation
from dao.graph import without_cycles, table_to_graph
from tables.entry_types import TransactionTableEntry, WaitForGraphEntry, LockTableEntry, TransactionStatus
from tables.synced import SynchronizedTable
from threading import Condition, Thread

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
                                                             status=TransactionStatus.ACTIVE.value,
                                                             ref=self)
        self.TRANSACTIONS.append(self.transaction_table_entry)
        self.is_aborted = False

    def _save_backup_data(self):
        # save in a set every table name along with the db it belongs to
        working_tables = {(operation.connection_params.db_name, operation.table_name) for operation in self.operations
                          if not operation.is_select}
        # print(working_tables, self.operations)

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
                    params = {str(i): row[i] for i in range(0, len(row))}
                    op = InsertOperation(DbConnectionHelper(db_name),
                                         table_name,
                                         params=params,
                                         is_explicit=False)
                    op.execute()

    def abort(self):
        self.logger.warning('Aborting')
        self.is_aborted = True
        self.TRANSACTIONS.update(self.transaction_table_entry,
                                 self.transaction_table_entry._replace(status=TransactionStatus.ABORTED))
        self.LOCKS.delete(transaction=self.id)
        self.WAIT_FOR_GRAPH.delete(trans_waits_lock=self.id, trans_has_lock=self.id)

    def execute(self):
        # block all resources
        self.logger.info(f'Lock Table is{Transaction.LOCKS}')
        for operation in self.operations:
            op_key = operation.get_resource_id()
            lock_type = 'write' if not operation.is_select else 'read'
            locked_elem = self.LOCKS.get(record_id=op_key)
            is_mine = False if not locked_elem else locked_elem[0].transaction == self.id
            is_compatible = (False if lock_type == 'write' else
                             True if
                             lock_type == 'read' and locked_elem[0].type == 'read'
                             else False)
            if locked_elem and is_mine and is_compatible:
                trans_has_lock = locked_elem[0].transaction
                self.logger.warning(f'Waiting for transaction {trans_has_lock}')
                self.WAIT_FOR_GRAPH.append(
                    WaitForGraphEntry(lock_type=lock_type,
                                      locked_table=operation.table_name,
                                      locked_object=operation.key,
                                      trans_waits_lock=self.id,
                                      trans_has_lock=trans_has_lock))

                while self.LOCKS.contains(record_id=op_key):
                    with self.LOCKS.condition:
                        self.LOCKS.condition.wait()
                        if self.is_aborted:
                            return

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
            self.logger.info(f'Executing {operation}')
            operation.execute()
        self.LOCKS.delete(transaction=self.id)

        # commit
        commit_entry = self.transaction_table_entry._replace(status=TransactionStatus.COMMITTED)
        self.TRANSACTIONS.update(old_elem=self.transaction_table_entry,
                                 new_elem=commit_entry)
        logging.info(f'Transaction {self.id} committed')

    @staticmethod
    def deadlock_checker_daemon():
        def daemon_target():
            while True:
                time.sleep(13)
                logging.info('Checking for cycles')
                to_abort = without_cycles(table_to_graph(Transaction.WAIT_FOR_GRAPH))
                transactions = Transaction.TRANSACTIONS.get()
                if transactions is None:
                    continue
                for transaction in transactions:
                    if transaction.id in to_abort:
                        transaction.ref.abort()
                        transaction.ref.rollback()

        logging.info('Starting check for cycles')
        return Thread(name='cycle_checker', target=daemon_target)
