from util.common import getContainer
from interact import interact
import ZODB, transaction
from BTrees.OOBTree import OOBTree

class Recorder:
    '''
    A class for managing simple records.
    The records stored in a flat fashion, that is, one key, one value
    '''
    def __init__(self, db_path):
        self.db_path = db_path
        self.db = None

    def opendb(self):
        if not self.db:
            connection = ZODB.connection(self.db_path)
            self.db    = getContainer(connection.root, 'main')

    def commit(self):
        transaction.commit()

    def save(self, key, ent):
        self.opendb()
        self.db[key] = ent
        self.commit()

    def dbinstance(self):
        '''
        open the database and return the container
        '''
        self.opendb()
        return self.db

    def add(self, key, ent):
        self.save(key, ent)

    def delete(self, key):
        self.opendb()
        del self.db[key]
        self.commit()

    def search(self, filter):
        # filter is a function takes two arguments, and returns Boolean
        # subclass must overload the __str__ method
        self.opendb()
        entries = ((k, v) for k,v in self.db.items() if filter(k, v))
        return entries

    def list(self):
        return Recorder.search(self, filter=(lambda k,v: True))

    def menu(self):
        choices = [
            ['add', self.add],
            ['list', self.list],
            ['search', self.search],
            ['edit', self.edit],
            ['delete', self.delete]
        ]
        i, junk = interact.printAndPick([x for x, y in choices], prompt='choice: ', lineMode=True)
        action = choices[i][-1]
        action()


class Logger(Recorder):
    def dellast(self):
        self.opendb()
        keys = [k for k in self.db]
        if not keys: return

        key = sorted(keys)[-1]
        log = self.db[key]
        i = interact.readstr('%s\nconfirm? [n] ' % log, default='n')
        if i not in ('y', 'Y'):
            return
        self.delete(key)


if __name__ == '__main__':
    logger = Logger('/tmp/testlog')
    #logger.add('sex', 'Male')
    #logger.add('age', 34)
    logger.list()
    logger.dellast()
