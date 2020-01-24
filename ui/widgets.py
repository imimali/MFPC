'''
    created on 24 January 2020
    
    @author: Gergely
'''
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QTableWidget, QAbstractItemView, QVBoxLayout, QLabel, \
    QFormLayout, QLineEdit, QListWidget, QTableWidgetItem


class TransactionUtilsWidget(QWidget):
    def __init__(self):
        super().__init__()
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
        run_transaction_button.setFont(QFont('Verdana', 13))

        self.transaction_list = transaction_list
        self.start_new_transaction_button = start_new_transaction_button
        self.enough_button = enough_button
        self.run_button = run_transaction_button
        self.setLayout(run_transaction_layout)

    def connect(self):
        pass


class MFormWidget(QWidget):
    def __init__(self, title, row_names):
        super().__init__()
        edit_layout = QFormLayout()
        edit_layout.setSpacing(4)
        edit_layout.addWidget(QLabel(title))
        for row in row_names:
            value_edit = QLineEdit()
            value_edit.setFixedHeight(40)
            value_edit.setFixedWidth(120)
            edit_layout.addRow(row, value_edit)
        edit_layout.addRow(AUDButtonBar())
        self.setLayout(edit_layout)


class AUDButtonBar(QWidget):
    def __init__(self):
        super().__init__()
        button_bar = QHBoxLayout()
        self.buttons = {}
        for button_name in ['Add', 'Update', 'Delete']:
            button = QPushButton(button_name)
            button.setFixedWidth(100)
            button.setFixedHeight(40)
            button.setContentsMargins(20, 0, 20, 0)
            button_bar.addWidget(button)
            self.buttons[button_name] = button
        self.setLayout(button_bar)

    def connect_buttons(self, callback_map):
        for button_name in self.buttons:
            self.buttons[button_name].clicked.connect(callback_map[button_name])


class MTableWidget(QWidget):
    def __init__(self, columns_names, title):
        super().__init__()
        table = QTableWidget()
        table.setContentsMargins(10, 10, 10, 10)
        table.setColumnCount(len(columns_names))
        table.setRowCount(3)
        table.setHorizontalHeaderLabels(columns_names)
        table.resizeColumnsToContents()
        table.resizeRowsToContents()
        table.setSelectionBehavior(QAbstractItemView.SelectRows)

        wrapper = QVBoxLayout()

        wrapper.addWidget(QLabel(title))
        wrapper.addWidget(table)
        fill_button = QPushButton('Fill')
        fill_button.setFixedWidth(100)
        wrapper.addWidget(fill_button)

        self.table = table
        self.fill_button = fill_button
        self.setLayout(wrapper)

    def connect_fill_button(self, connect_callback):
        self.fill_button.clicked.connect(connect_callback)

    def fill(self, data):
        if len(data) == 0:
            return
        self.table.setRowCount(len(data))
        for i in range(len(data)):
            for j in range(len(data[0])):
                self.table.setItem(i, j, QTableWidgetItem(str(data[i][j])))
