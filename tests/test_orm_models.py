def test_creating_init_sql(test_model):
    assert test_model.get_init_sql() == \
        "CREATE TABLE TESTMODEL ( _id INTEGER NOT NULL, name TEXT, second TEXT, last INTEGER NOT NULL, PRIMARY KEY (_id))"
