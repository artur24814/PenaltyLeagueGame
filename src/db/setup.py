import sqlite3


def create_connect(testing):
    if testing:
        return _create_temp_db()
    return _create_prod_db()


def _create_prod_db():
    cnx = sqlite3.connect('db.db')
    cursor = cnx.cursor()
    return cursor, cnx


def _create_temp_db():
    cnx = sqlite3.connect('test-db.db')
    cursor = cnx.cursor()
    return cursor, cnx
