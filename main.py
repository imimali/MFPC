'''
    created on 02 February 2020
    
    @author: Gergely
'''
import sys
from dao.transaction import Transaction
from PyQt5.QtWidgets import QApplication

from ui.ui import App

# TODO use other tables
# TODO actually fill tables

if __name__ == '__main__':
    app = QApplication(sys.argv)
    Transaction.launch_deadlock_checker_daemon()
    ex = App()
    sys.exit(app.exec_())
