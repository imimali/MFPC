'''
    created on 02 February 2020
    
    @author: Gergely
'''
import sys

from dao.db import DbConnectionHelper, SelectOperation
from dao.transaction import Transaction
from PyQt5.QtWidgets import QApplication

from ui.ui import App

if __name__ == '__main__':
    app = QApplication(sys.argv)
    connection = DbConnectionHelper('MFPC0')
    connection1 = DbConnectionHelper('MFPC1')
    clients = SelectOperation(connection, 'client').execute()
    products = SelectOperation(connection, 'product').execute()
    payments = SelectOperation(connection1, 'payments').execute()
    Transaction.deadlock_checker_daemon().start()
    ex = App()
    ex.client_table.fill(clients)
    ex.product_table.fill(products)
    ex.payments_table.fill(payments)
    sys.exit(app.exec_())
