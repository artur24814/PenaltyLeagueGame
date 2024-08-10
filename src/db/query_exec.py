from src.db.setup import create_connect


class QueryExecutor:
    def __init__(self, sql, values, many=False, return_id=False, class_name_of_new_obj=None, db_fields_to_lookup=None):
        self.cursor = None
        self.cnx = None
        self.sql = sql
        self.values = values
        self.many = many
        self.return_id = return_id
        self.class_name = class_name_of_new_obj
        self.fields_to_lookup = db_fields_to_lookup

    def execute(self, testing=False, *args, **kwargs):
        self.cursor, self.cnx = create_connect(testing=testing)
        self.cursor.execute(self.sql, tuple(self.values))
        result = True

        if self.many:
            result = self.get_many_result()
        elif not self.many and not self.return_id:
            result = self.get_one_result()
        elif self.return_id:
            self.cnx.commit()
            result = self.cursor.lastrowid
        self.cnx.close()
        return result

    def get_many_result(self):
        obj_list = list()
        for row in self.cursor.fetchall():
            result = row
            obj_list.append(self.get_new_obj(result))
        return obj_list

    def get_one_result(self):
        data = self.cursor.fetchone()
        if data:
            result = data
            return self.get_new_obj(result)
        else:
            return None

    def get_new_obj(self, result):
        new_obj = self.class_name(**{self.fields_to_lookup[index]: result[index] for index in range(1, len(result))})
        new_obj._id = result[0]
        return new_obj
