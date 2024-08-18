from .orm_fields import IntergerField, RealField, TextField
from src.db.query_exec import QueryExecutor


class BaseManager:
    def __init__(self, model):
        self.model = model
        self.sql = ''
        self.many = False

    def get_table_name(self):
        return self.get_class_name().__name__.upper()

    def get_class_name(self):
        if isinstance(self.model, type):
            return self.model
        return self.model.__class__

    def filter(self, **kwargs):
        attrs_str = " AND ".join([attr + '=?' for attr in kwargs.keys()])
        self.sql = f'SELECT * FROM {self.get_table_name()} WHERE {attrs_str}'
        self.values = kwargs.values()
        self.many = True
        self.return_obj = False
        return QueryExecutor(
            self.sql, self.values, many=True,
            db_fields_to_lookup=self.model.db_fields_to_lookup,
            class_name_of_new_obj=self.get_class_name()
        )

    def get_one(self, **kwargs):
        executor = self.filter(**kwargs)
        executor.many = False
        return executor

    def all(self):
        self.sql = f'SELECT * FROM {self.get_table_name()}'
        self.values = []
        self.many = True
        self.return_obj = False
        return QueryExecutor(
            self.sql, self.values, many=True,
            db_fields_to_lookup=self.model.db_fields_to_lookup,
            class_name_of_new_obj=self.get_class_name()
        )


class ModelMeta(type):
    def __new__(cls, name, bases, attrs):
        new_cls = super().__new__(cls, name, bases, attrs)
        new_cls.query_creator = BaseManager(new_cls)
        return new_cls


class Model(metaclass=ModelMeta):
    db_fields_to_lookup = ['_id']

    def __init__(self):
        self._id = -1
        self.query_creator = BaseManager(self)

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    def get_attrs_values_tuple(self):
        attrs = self.db_fields_to_lookup
        values = [getattr(self, attr) for attr in self.db_fields_to_lookup]
        return attrs, values

    def save(self, *args, **kwargs):
        attrs, values = self.get_attrs_values_tuple()
        if self._id == -1:
            self.query_creator.sql = f'INSERT INTO {self.query_creator.get_table_name()} ({", ".join(attrs[1:])}) VALUES ({str("?," * len(values[1:]))[:-1]})'
            self.query_creator.values = values[1:]
        else:
            attrs_str = ", ".join([attr + '=?' for attr in attrs])
            self.query_creator.sql = f"UPDATE {self.query_creator.get_table_name()} SET {attrs_str} WHERE _id={self._id}"
            self.query_creator.values = values

        return QueryExecutor(self.query_creator.sql, self.query_creator.values, return_id=True)

    def delete(self, *args, **kwargs):
        self.query_creator.sql = f"DELETE FROM {self.query_creator.get_table_name()} WHERE _id={self._id}"
        self.query_creator.values = []
        return QueryExecutor(self.query_creator.sql, self.query_creator.values, return_id=True)

    def get_init_sql(self):
        fields_sql = ''
        for field in self.db_fields_to_lookup:
            if field == '_id':
                continue
            value = getattr(self, field)
            if isinstance(value, int):
                fields_sql += IntergerField(name=field, null=False).get_sql() + ', '
            elif isinstance(value, bool):
                fields_sql += IntergerField(name=field, null=False).get_sql() + ', '
            elif isinstance(value, float):
                fields_sql += RealField(name=field, null=False).get_sql() + ', '
            else:
                fields_sql += TextField(name=field).get_sql() + ', '

        return f"CREATE TABLE {self.query_creator.get_table_name()} ( _id INTEGER NOT NULL, " + fields_sql + "PRIMARY KEY (_id))"
