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
        self.person_table = None
        self.rental_table = None
        self.movie_table = None

        self.person_form = None
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

        edits_layout = QHBoxLayout()
        edits_layout.setSpacing(24)
        person_form = MFormWidget(title='Person', row_names=['id', 'name', 'age', 'email'])
        rental_form = MFormWidget(title='Rental', row_names=['id', 'person_id', 'movie_id'])
        movie_form = MFormWidget(title='Rental', row_names=['id', 'year', 'title', 'rating'])
        for widget in [person_form, rental_form, movie_form]:
            edits_layout.addWidget(widget)

        tables_layout = QHBoxLayout()
        tables_layout.setSpacing(16)
        person_table = MTableWidget(['id', 'name', 'age', 'email'], title='Person')
        rental_table = MTableWidget(['id', 'person_id', 'movie_id'], title='Rental')
        movie_table = MTableWidget(['id', 'year', 'title', 'rating'], title='Movie')
        for widget in [person_table, rental_table, movie_table]:
            tables_layout.addWidget(widget)

        main_layout.addLayout(tables_layout)
        transaction_utils = TransactionUtilsWidget()
        main_layout.addWidget(transaction_utils)
        main_layout.addLayout(edits_layout)
        self.setLayout(main_layout)

        self.person_table = person_table
        self.rental_table = rental_table
        self.movie_table = movie_table

        self.person_form = person_form
        self.rental_form = rental_form
        self.movie_form = movie_form

        self.transaction_handle = transaction_utils

        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
