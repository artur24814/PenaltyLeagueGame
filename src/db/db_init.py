"""
===================================
run > python -m src.db.db_init.py
===================================
"""
import os

from src.settings import BASE_DIR
from src.db.helpers import execute_get_init_sql_on_subclasses
from src.db.setup import create_connect


def run_init_queryes(file_path):
    results = execute_get_init_sql_on_subclasses(file_path)
    cursor, cnx = create_connect()
    for class_name, sql in results.items():
        try:
            cursor.execute(sql)
            print(f'From {class_name} Table created!')
        except Exception:
            print(f'From {class_name} table already exists')
    cnx.commit()
    cnx.close()


if __name__ == "__main__":
    file_path = os.path.join(BASE_DIR, 'models', 'game_models.py')
    run_init_queryes(file_path)
