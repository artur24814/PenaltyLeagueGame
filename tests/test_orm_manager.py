from .testing_models import TestModel
from src.db.query_exec import QueryExecutor


def test_generated_table_name(test_model):
    assert test_model.query_creator.get_table_name() == "TESTMODEL"


def test_filter_queryset(test_model):
    executor = test_model.query_creator.filter(name='Harry', second="Potter")

    assert test_model.query_creator.sql == "SELECT * FROM TESTMODEL WHERE name=?, second=?"
    assert tuple(test_model.query_creator.values) == ("Harry", "Potter")
    assert isinstance(executor, QueryExecutor) is True


def test_all_queryset(test_model):
    executor = test_model.query_creator.all()

    assert test_model.query_creator.sql == "SELECT * FROM TESTMODEL"
    assert tuple(test_model.query_creator.values) == ()
    assert isinstance(executor, QueryExecutor) is True


def test_create_queryset(test_model):
    executor = test_model.save()

    assert test_model.query_creator.sql == "INSERT INTO TESTMODEL (name, second, last) VALUES (?,?,?)"
    assert tuple(test_model.query_creator.values) == ('Harry', 'Potter', 2)
    assert isinstance(executor, QueryExecutor) is True


def test_update_queryset_on_not_set_id(test_model):
    executor = test_model.save()

    assert test_model.query_creator.sql == "INSERT INTO TESTMODEL (name, second, last) VALUES (?,?,?)"
    assert tuple(test_model.query_creator.values) == ('Harry', 'Potter', 2)
    assert isinstance(executor, QueryExecutor) is True


def test_update_queryset_with_id(test_model):
    test_model._id = 5
    executor = test_model.save()

    assert test_model.query_creator.sql == "UPDATE TESTMODEL SET _id=?, name=?, second=?, last=? WHERE _id=5"
    assert tuple(test_model.query_creator.values) == (5, 'Harry', 'Potter', 2)
    assert isinstance(executor, QueryExecutor) is True


def test_delete_queryset_with_id(test_model):
    test_model._id = 5
    executor = test_model.delete()

    assert test_model.query_creator.sql == "DELETE FROM TESTMODEL WHERE _id=5"
    assert tuple(test_model.query_creator.values) == ()
    assert isinstance(executor, QueryExecutor) is True


def test_get_new_obj(test_model):
    result_tuple = (4, 'Simon', 'Kowalski', 4)
    executor = test_model.query_creator.all()
    new_obj = executor.get_new_obj(result_tuple)
    assert isinstance(new_obj, TestModel) is True
    assert new_obj.id == result_tuple[0]
    assert new_obj.name == result_tuple[1]
    assert new_obj.second == result_tuple[2]
    assert new_obj.last == result_tuple[3]
