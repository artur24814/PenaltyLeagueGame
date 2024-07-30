def test_integer_field_sql(integer_field):
    assert integer_field.get_sql() == 'test_integer INTEGER NOT NULL'


def test_integer_field_primary_sql(integer_field):
    integer_field.primary = True
    assert integer_field.get_sql() == 'test_integer INTEGER NOT NULL\nPRIMARY KEY (test_integer)'


def test_text_field_sql(text_field):
    assert text_field.get_sql() == 'test_text TEXT NOT NULL'


def test_real_field_sql(real_field):
    assert real_field.get_sql() == 'test_real REAL NOT NULL'
