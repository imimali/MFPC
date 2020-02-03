'''
    created on 26 January 2020
    
    @author: Gergely
'''
import logging
from threading import Thread

from dao.db import InsertOperation, DeleteOperation, SelectOperation, UpdateOperation, DbConnectionHelper
from dao.transaction import Transaction

logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-9s) %(message)s')


class Controller:

    def __init__(self):
        self.operations = []
        self.operations_history = ['']
        self.transactions = []
        self.primary_db = 'MovieRental'

    def create_insert_operation(self, db_name, table_name, params):
        logging.info(f'Creating insert operation, {db_name}, {table_name}, {params}')
        self.operations.append(InsertOperation(DbConnectionHelper(db_name), table_name, params,
                                               is_explicit=False))
        self.operations_history[-1] += self.operations[-1].to_fancy() + '; '

    def create_delete_operation(self, db_name, table_name, key):
        logging.info(f'Creating delete operation, {db_name}, {table_name}, {key}')
        self.operations.append(DeleteOperation(DbConnectionHelper(db_name), table_name, params={'id': key}))
        self.operations_history[-1] += self.operations[-1].to_fancy() + '; '

    def create_select_operation(self, db_name, table_name, params):

        logging.info(f'Creating select operation, {db_name}, {table_name}, {params}')
        self.operations.append(SelectOperation(DbConnectionHelper(db_name), table_name, params))
        self.operations_history[-1] += self.operations[-1].to_fancy() + '; '

    def create_update_operation(self, db_name, table_name, params):
        logging.info(f'Creating update operation, {db_name}, {table_name}, {params}')
        self.operations.append(UpdateOperation(DbConnectionHelper(db_name), table_name, params))
        self.operations_history[-1] += self.operations[-1].to_fancy() + '; '

    def create_transaction(self):
        logging.info(f'Creating Transaction with ops {self.operations}')

        def create(ops):
            transaction = Transaction(operations=ops)
            try:
                transaction.execute()
            except Exception as e:
                logging.error(f'Error occurred {e}')
                transaction.abort()
                transaction.rollback()

        if self.operations:
            operations = self.operations[:]
            self.transactions.append(
                Thread(target=create, args=(operations,)))
            self.operations_history.append('')
            self.operations = []
        else:
            logging.warning('No operations added. Transaction not created')

    def start_transactions(self):
        self.operations_history.clear()
        for transaction in self.transactions:
            transaction.start()
        for transaction in self.transactions:
            transaction.join()

    def clear(self):
        self.transactions.clear()
        self.operations.clear()
        self.operations_history = ['']
