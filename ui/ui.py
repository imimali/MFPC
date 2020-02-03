'''
    created on 22 January 2020

    @author: Gergely
'''
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import *

from ui.widgets import MTableWidget, MFormWidget, TransactionUtilsWidget
from control.control import Controller

font = QFont('Verdana', 13)
font2 = QFont('Comic Sans MS', 12)


class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Movie Rental Management'
        self.controller = Controller()
        self.left = 200
        self.top = 200
        self.width = 800
        self.height = 800
        self.client_table = None
        self.product_table = None
        self.payments_table = None

        self.client_form = None
        self.product_form = None
        self.payment_form = None

        self.transaction_handle = None

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setFont(font2)
        main_layout = QVBoxLayout()

        # transaction
        client_table_metadata = {'db_name': 'MFPC0', 'table_name': 'client',
                                 'field_names': ['id', 'name', 'age', 'email']}
        product_table_metadata = {'db_name': 'MFPC0', 'table_name': 'product',
                                  'field_names': ['id', 'name', 'price']}
        payment_table_metadata = {'db_name': 'MPFC1', 'table_name': 'payments',
                                  'field_names': ['id', 'client', 'product', 'commission']}
        edits_layout = QHBoxLayout()
        edits_layout.setSpacing(24)
        client_form = MFormWidget(**client_table_metadata)
        rental_form = MFormWidget(**product_table_metadata)
        movie_form = MFormWidget(**payment_table_metadata)
        for widget in [client_form, rental_form, movie_form]:
            edits_layout.addWidget(widget)

        tables_layout = QHBoxLayout()
        tables_layout.setSpacing(16)
        client_table = MTableWidget(**client_table_metadata)
        rental_table = MTableWidget(**product_table_metadata)
        movie_table = MTableWidget(**payment_table_metadata)
        for widget in [client_table, rental_table, movie_table]:
            tables_layout.addWidget(widget)

        main_layout.addLayout(tables_layout)
        transaction_utils = TransactionUtilsWidget()
        main_layout.addWidget(transaction_utils)
        main_layout.addLayout(edits_layout)
        self.setLayout(main_layout)

        self.client_table = client_table
        self.product_table = rental_table
        self.payments_table = movie_table

        self.client_form = client_form
        self.product_form = rental_form
        self.payment_form = movie_form

        self.transaction_handle = transaction_utils
        self.connect_ui()
        self.show()

    def connect_form_buttons(self, form: MFormWidget):
        form.button_bar.connect_buttons({'Add': lambda: self.controller.create_insert_operation(
            db_name=form.db_name,
            table_name=form.table_name,
            params=form.get_values()),
                                         'Update': lambda: self.controller.create_update_operation(
                                             db_name=form.db_name,
                                             table_name=form.table_name,
                                             params=form.get_values()
                                         ),
                                         'Delete': lambda: self.controller.create_delete_operation(
                                             db_name=form.db_name,
                                             table_name=form.table_name,
                                             key=form.get_values()['id']
                                         )})
        form.button_bar.connect_buttons(
            {key: lambda: self.transaction_handle.fill_transactions(self.controller.operations_history)
             for key in ['Add', 'Update', 'Delete']}
        )

    def connect_ui(self):
        self.client_table.table.itemSelectionChanged.connect(
            lambda: self.client_form.fill_edits(self.client_table.get_selected_row_data()))

        self.payments_table.table.itemSelectionChanged.connect(
            lambda: self.payment_form.fill_edits(self.payments_table.get_selected_row_data()))

        self.product_table.table.itemSelectionChanged.connect(
            lambda: self.product_form.fill_edits(self.product_table.get_selected_row_data()))

        self.client_table.connect_fill_button(
            lambda x: self.controller.create_select_operation(db_name=self.client_table.db_name,
                                                              table_name=self.client_table.table_name,
                                                              params={}))
        self.payments_table.connect_fill_button(
            lambda x:
            self.controller.create_select_operation(db_name=self.payments_table.db_name,
                                                    table_name=self.payments_table.table_name,
                                                    params={}))
        self.product_table.connect_fill_button(
            lambda x:
            self.controller.create_select_operation(db_name=self.product_table.db_name,
                                                    table_name=self.product_table.table_name,
                                                    params={}))

        for form in [self.client_form, self.product_form, self.payment_form]:
            self.connect_form_buttons(form)

        self.transaction_handle.enough_button.clicked.connect(self.controller.create_transaction)
        self.transaction_handle.run_button.clicked.connect(self.controller.start_transactions)
