'''
    created on 22 January 2020

    @author: Gergely
'''
import sys

from PyQt5.QtCore import pyqtSlot, QRect
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import *

font = QFont('Verdana', 13)
font2 = QFont('Comic Sans MS', 12)


class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Movie Rental Management'
        self.left = 200
        self.top = 200
        self.width = 800
        self.height = 500
        self.run_transaction_button = None
        self._plainTextEdit = None
        self._cipherTextEdit = None
        self._encryptButton = None
        self._decryptButton = None
        self._encryptionKeyInfoLabel = None
        self._decryptionKeyInfoLabel = None
        self._key = None
        # self.initUI()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setFont(font)
        main_layout = QVBoxLayout()

        # run transaction button
        run_transaction_layout = QHBoxLayout()
        run_transaction_layout.setContentsMargins(200, 0, 200, 0)
        run_transaction_button = QPushButton('Run Transaction')
        run_transaction_layout.addWidget(run_transaction_button)
        run_transaction_button.setFont(font)

        edits_layout = QHBoxLayout()
        edits_layout.setSpacing(24)
        edits_layout.addLayout(self.build_form(title='Person', row_names=['id', 'name', 'age', 'email']))
        edits_layout.addLayout(self.build_form(title='Rental', row_names=['id', 'person_id', 'movie_id']))
        edits_layout.addLayout(self.build_form(title='Rental', row_names=['id', 'year', 'title', 'rating']))
        main_layout.addLayout(run_transaction_layout)
        main_layout.addLayout(edits_layout)
        self.setLayout(main_layout)
        self.show()

    @staticmethod
    def build_form(title, row_names):
        edit_layout = QFormLayout()
        edit_layout.setSpacing(4)
        edit_layout.addWidget(QLabel(title))
        for row in row_names:
            edit_layout.addRow(row, App.build_form_row())
        edit_layout.addRow(App.build_button_bar())
        return edit_layout

    @staticmethod
    def build_button_bar():
        button_bar = QHBoxLayout()
        for button_name in ['Add', 'Update', 'Delete']:
            button = QPushButton(button_name)
            button.setFixedWidth(100)
            button.setFixedHeight(40)
            button.setContentsMargins(20, 0, 20, 0)
            button_bar.addWidget(button)
        return button_bar

    @staticmethod
    def build_form_row():
        value_edit = QTextEdit()
        value_edit.setFixedHeight(40)
        value_edit.setFixedWidth(120)
        return value_edit


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
