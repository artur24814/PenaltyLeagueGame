from .orm_fields import IntergerField, RealField, TextField


class BaseManager:
    def __init__(self, object, cursor=None):
        self.object = object
        self.class_name = self.object.__class__
        self.cursor = cursor
        self.sql = ''
        self.many = False
        self.values = None
        self.return_obj = False

    def get_attrs_values_tuple(self):
        attrs = tuple(self.object.db_fields_to_lookup)
        values = [getattr(self.object, attr) for attr in self.object.db_fields_to_lookup]
        return attrs, values

    def execute(self, *args, **kwargs):
        self.cursor.execute(self.sql, tuple(self.values()))
        if self.many:
            return self.get_many_result()
        elif not self.many and not self.return_obj:
            return self.get_one_result()
        elif self.return_obj:
            self.object._id = self.cursor.lastrowid
            return self.object
        return True

    def get_many_result(self):
        obj_list = list()
        for row in self.cursor.fetchall():
            result = row
            obj_list.append(self.get_new_obj(result))
        return obj_list

    def get_one_result(self):
        data = self.fetchone()
        if data:
            result = data
            return self.get_new_obj(result)
        else:
            return None

    def get_new_obj(self, result):
        new_obj = self.class_name(**{self.object.db_fields_to_lookup[index]: result[index] for index in range(1, len(result))})
        new_obj._id = result[0]
        return new_obj

    def get_table_name(self):
        return str(self.object.__class__.__name__).upper()

    def filter(self, **kwargs):
        attrs_str = ", ".join([attr + '=?' for attr in kwargs.keys()])
        self.sql = f'SELECT * FROM {self.get_table_name()} WHERE {attrs_str}'
        self.values = kwargs.values()
        self.many = True
        self.return_obj = False

    def get_one(self, **kwargs):
        self.filter(**kwargs)
        self.many = False

    def all(self):
        self.sql = f'SELECT * FROM {self.get_table_name()}'
        self.values = []
        self.many = True
        self.return_obj = False

    def create(self, *args, **kwargs):
        attrs, values = self.get_attrs_values_tuple()
        self.sql = f'INSERT INTO {self.get_table_name()} ({", ".join(attrs)}) VALUES ({"?," * len(values)})'
        self.values = values
        self.many = False
        self.return_obj = True

    def update(self, *args, **kwargs):
        if self.object._id == -1:
            return self.create(self, *args, **kwargs)

        attrs, _ = self.get_attrs_values_tuple()
        attrs_str = ", ".join([attr + '=?' for attr in attrs])

        self.sql = f"UPDATE {self.object.__class__.__name__} SET {attrs_str} WHERE _id={self.object._id}"
        self.values = []
        self.many = False
        self.return_obj = True

    def delete(self, *args, **kwargs):
        self.sql = f"DELETE FROM {self.__class__.__name__} WHERE _id={self.object._id}"
        self.values = []
        self.many = False
        self.return_obj = False


class Model:
    fields_to_db_ignore = ['manager']

    def __init__(self):
        self._id = -1
        self.manager = BaseManager(self)

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def db_fields_to_lookup(self):
        return [attr for attr in self.__dict__.keys() if attr not in self.fields_to_db_ignore]

    def get_init_sql(self):
        fields_sql = ''
        for field in self.db_fields_to_lookup:
            if field == '_id':
                continue
            value = getattr(self, field)
            if isinstance(value, int):
                fields_sql += IntergerField(name=field, null=False).get_sql() + ', '
            elif isinstance(value, float):
                fields_sql += RealField(name=field, null=False).get_sql() + ', '
            else:
                fields_sql += TextField(name=field).get_sql() + ', '

        return f"CREATE TABLE {self.manager.get_table_name()} ( _id INTEGER NOT NULL, " + fields_sql + "PRIMARY KEY (_id))"
