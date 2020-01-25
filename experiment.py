'''
    created on 22 January 2020
    
    @author: Gergely
'''
from tables.tables import TransactionTableEntry, SynchronizedTable


class Person:
    def __init__(self):
        self.name = 'yup'
        self.age = 12


def f(**kwargs):
    print(kwargs)


e = TransactionTableEntry(id=1, timestamp=0, status='active')
e2 = TransactionTableEntry(id=1, timestamp=0, status='committed')
# f(**(e._asdict()))
t = SynchronizedTable()
t.append(e)
print(str(t))
t.update(old_elem=e, new_elem=e2)
p = Person()
print(str(t))
