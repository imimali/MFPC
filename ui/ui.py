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
        self.rental_table = None
        self.movie_table = None

        self.client_form = None
        self.rental_form = None
        self.movie_form = None

        self.transaction_handle = None

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setFont(font2)
        main_layout = QVBoxLayout()

        # transaction
        client_table_metadata = {'title': 'client', 'field_names': ['id', 'name', 'age', 'email']}
        rental_table_metadata = {'title': 'rental', 'field_names': ['id', 'client_id', 'movie_id']}
        movie_table_metadata = {'title': 'movie', 'field_names': ['id', 'title', 'genre', 'rating']}
        edits_layout = QHBoxLayout()
        edits_layout.setSpacing(24)
        client_form = MFormWidget(**client_table_metadata)
        rental_form = MFormWidget(**rental_table_metadata)
        movie_form = MFormWidget(**movie_table_metadata)
        for widget in [client_form, rental_form, movie_form]:
            edits_layout.addWidget(widget)

        tables_layout = QHBoxLayout()
        tables_layout.setSpacing(16)
        client_table = MTableWidget(**client_table_metadata)
        rental_table = MTableWidget(**rental_table_metadata)
        movie_table = MTableWidget(**movie_table_metadata)
        for widget in [client_table, rental_table, movie_table]:
            tables_layout.addWidget(widget)

        main_layout.addLayout(tables_layout)
        transaction_utils = TransactionUtilsWidget()
        main_layout.addWidget(transaction_utils)
        main_layout.addLayout(edits_layout)
        self.setLayout(main_layout)

        self.client_table = client_table
        self.rental_table = rental_table
        self.movie_table = movie_table

        self.client_form = client_form
        self.rental_form = rental_form
        self.movie_form = movie_form

        self.transaction_handle = transaction_utils
        self.connect_ui()
        self.show()

    def connect_form_buttons(self, form: MFormWidget):
        form.button_bar.connect_buttons({'Add': lambda: self.controller.create_insert_operation(
            db_name=None,
            table_name=form.title,
            params=form.get_values()),
                                         'Update': lambda: self.controller.create_update_operation(
                                             db_name=None,
                                             table_name=form.title,
                                             params=form.get_values()
                                         ),
                                         'Delete': lambda: self.controller.create_delete_operation(
                                             db_name=None,
                                             table_name=form.title,
                                             key=form.get_values()['id']
                                         )})
        form.button_bar.connect_buttons(
            {key: lambda: self.transaction_handle.fill_transactions(self.controller.operations_history)
             for key in ['Add', 'Update', 'Delete']}
        )

    def connect_ui(self):
        self.client_table.table.itemSelectionChanged.connect(
            lambda: self.client_form.fill_edits(self.client_table.get_selected_row_data()))

        self.movie_table.table.itemSelectionChanged.connect(
            lambda: self.movie_form.fill_edits(self.movie_table.get_selected_row_data()))

        self.rental_table.table.itemSelectionChanged.connect(
            lambda: self.rental_form.fill_edits(self.rental_table.get_selected_row_data()))

        self.client_table.connect_fill_button(
            lambda x: self.controller.create_select_operation('MovieRental',
                                                              table_name=self.client_table.title,
                                                              params={}))
        self.movie_table.connect_fill_button(
            lambda x:
            self.controller.create_select_operation('MovieRental',
                                                    table_name=self.movie_table.title,
                                                    params={}))
        self.rental_table.connect_fill_button(
            lambda x:
            self.controller.create_select_operation('MovieRental',
                                                    table_name=self.rental_table.title,
                                                    params={}))

        for form in [self.client_form, self.rental_form, self.movie_form]:
            self.connect_form_buttons(form)

        self.transaction_handle.enough_button.clicked.connect(self.controller.create_transaction)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
