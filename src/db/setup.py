import sqlite3
import tempfile


def create_connect(testing):
    if testing:
        return _create_temp_db()
    return _create_prod_db()


def _create_prod_db():
    cnx = sqlite3.connect('database.db')
    cursor = cnx.cursor()
    return cursor, cnx


def _create_temp_db():
    _, db_path = tempfile.mkstemp()
    cnx = sqlite3.connect(db_path)
    cursor = cnx.cursor()
    # cursor.execute(CREATE_TABLE)
    cnx.commit()
    return cnx, cursor
