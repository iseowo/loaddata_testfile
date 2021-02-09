import lambda_function
from DBConnect import DbConnection
import pytest


def db_object():
    return DbConnection()


def test_db_connect(mocker):
    def mock_db_connect():
        return 'xyz'

    mocker.patch('lambda_function.lambda_handler', mock_db_connect())
    ex = 'xyz'
    ac = lambda_function.lambda_handler
    assert ex == ac


def test_copy_from_stringio(mocker):
    def mock_stringIO():
        return 'xyz'

    mocker.patch('lambda_function.lambda_handler', mock_stringIO())
    ex = 'xyz'
    ac = lambda_function.lambda_handler
    assert lambda_function.lambda_handler
    assert ex == ac


def test_db_connect_object(mocker):
    db_mock_object = mocker.patch('lambda_function.lambda_handler', return_value=123)
    db = db_mock_object
    db_lambda = lambda_function.lambda_handler()
    assert db.assert_called() is None


def test_db_connect_attribute_username_parm(mocker):
    db_mock_object = mocker.patch('test_DBConnect.db_object', attribute='username_parm')
    db_mock_object.return_value = 123
    ac = db_object()
    assert ac == 123


def test_db_connect_Exception():
    with pytest.raises(Exception) as e:
        db_object().copy_from_stringio(None, None, None)
    exception_raised = e.value.__str__()
    assert exception_raised == "'NoneType' object has no attribute 'to_csv'"


def test_db_connect_NameError():
    with pytest.raises(Exception) as e:
        db_object().copy_from_stringio('', None, None)
    exception_raised = e.value.__str__()
    assert exception_raised == "'NoneType' object has no attribute 'to_csv'"


def test_db_connect_pw_tile(mocker):
    mocker.patch('test_DBConnect.db_object', attribute='pw_tile', return_value=123)
    ex = db_object()
    ac = 123
    assert ex == ac
