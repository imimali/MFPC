'''
    created on 22 January 2020

    @author: Gergely
'''
import sys

from PyQt5 import QtCore, QtWidgets
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
        self.height = 800
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setFont(font)
        main_layout = QVBoxLayout()

        # transaction
        run_transaction_layout = QVBoxLayout()
        run_transaction_layout.setContentsMargins(200, 0, 200, 0)
        transaction_list = QListWidget()
        run_transaction_layout.addWidget(transaction_list)

        manage_buttons_layout = QHBoxLayout()
        enough_button = QPushButton('Enough')
        start_new_transaction_button = QPushButton('New Transaction')
        manage_buttons_layout.addWidget(start_new_transaction_button)
        manage_buttons_layout.addWidget(enough_button)
        run_transaction_button = QPushButton('Run Transaction')
        run_transaction_layout.addLayout(manage_buttons_layout)
        run_transaction_layout.addWidget(run_transaction_button)
        run_transaction_button.setFont(font)

        edits_layout = QHBoxLayout()
        edits_layout.setSpacing(24)
        edits_layout.addLayout(self.build_form(title='Person', row_names=['id', 'name', 'age', 'email']))
        edits_layout.addLayout(self.build_form(title='Rental', row_names=['id', 'person_id', 'movie_id']))
        edits_layout.addLayout(self.build_form(title='Rental', row_names=['id', 'year', 'title', 'rating']))

        tables_layout = QHBoxLayout()
        tables_layout.setSpacing(16)
        tables_layout.addLayout(App.build_table(['id', 'name', 'age', 'email'], title='Person'))
        tables_layout.addLayout(App.build_table(['id', 'person_id', 'movie_id'], title='Rental'))
        tables_layout.addLayout(App.build_table(['id', 'year', 'title', 'rating'], title='Movie'))

        main_layout.addLayout(tables_layout)
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

    @staticmethod
    def build_table(columns_names, rows=0, title=''):
        table = QTableWidget()
        table.setContentsMargins(10, 10, 10, 10)
        table.setColumnCount(len(columns_names))
        table.setRowCount(3)
        table.setHorizontalHeaderLabels(columns_names)
        table.resizeColumnsToContents()
        table.resizeRowsToContents()
        table.setSelectionBehavior(QAbstractItemView.SelectRows)
        for i in range(rows):
            for j in range(len(columns_names)):
                # item = QTableWidgetItem('asd')
                table.setItem(i, j, QTableWidgetItem(f'iiiiiiiiiiiiiiiii={i};j={j}'))

        wrapper = QVBoxLayout()

        wrapper.addWidget(QLabel(title))
        wrapper.addWidget(table)
        fill_button = QPushButton('Fill')
        fill_button.setFixedWidth(100)
        wrapper.addWidget(fill_button)

        return wrapper


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
