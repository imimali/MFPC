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
        self.transactions = []
        self.primary_db = 'MovieRental'

    def create_insert_operation(self, db_name, table_name, **params):
        logging.info(f'Creating insert operation, {db_name}, {table_name}, {params}')
        self.operations.append(InsertOperation(DbConnectionHelper(db_name), table_name, params,
                                               is_explicit=False))

    def create_delete_operation(self, db_name, table_name, key):
        logging.info(f'Creating delete operation, {db_name}, {table_name}, {key}')
        self.operations.append(DeleteOperation(DbConnectionHelper(db_name), table_name, params={'id': key}))

    def create_select_operation(self, db_name, table_name, params):
        logging.info(f'Creating select operation, {db_name}, {table_name}, {params}')
        self.operations.append(SelectOperation(DbConnectionHelper(db_name), table_name, params))

    def create_update_operation(self, db_name, table_name, params):
        logging.info(f'Creating update operation, {db_name}, {table_name}, {params}')
        self.operations.append(UpdateOperation(DbConnectionHelper(db_name), table_name, params))

    def create_transaction(self):
        logging.info(f'Creating Transaction')
        self.transactions.append(lambda: Thread(target=Transaction(operations=self.operations).execute()))
        self.operations = []

    def start_transactions(self):
        for transaction in self.transactions:
            transaction.start()
        for transaction in self.transactions:
            transaction.join()
