'''
    created on 22 January 2020
    
    @author: Gergely
'''
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
'''


import threading
import time
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s', )


def consumer(cv):
    logging.debug('Consumer thread started ...')
    with cv:
        logging.debug('Consumer waiting ...')
        cv.wait()
        logging.debug('Consumer consumed the resource')


def producer(cv):
    logging.info('Producer thread started ...')
    with cv:
        logging.debug('Making resource available')
        logging.debug('Notifying to all consumers')
        cv.notifyAll()


class D:
    def __init__(self):
        print('triggered')
        self.a = [1, 2, 3]
        self.b = []

    def d(self):
        print('now called the d')
        self.b = self.a
        self.a = []


if __name__ == '__main__':
    condition = threading.Condition()
    cs1 = threading.Thread(name='consumer1', target=consumer, args=(condition,))
    cs2 = threading.Thread(name='consumer2', target=consumer, args=(condition,))
    pd = threading.Thread(name='producer', target=producer, args=(condition,))
    t = threading.Thread(name='maui', target=lambda: D().d())
    #d = D()
    #print(vars(d))
    #d.d()
    #print(vars(d))
    # cs1.start()
    time.sleep(2)
    t.start()
    # cs2.start()
    # time.sleep(2)
    # pd.start()