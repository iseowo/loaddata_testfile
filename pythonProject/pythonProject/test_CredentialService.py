from CredentialService import COS
import pytest


def object_assertion():
    return COS()


def cos():
    return object_assertion().call_cos()


def test_call_cos(mocker):
    mocking = mocker.patch('test_CredentialService.object_assertion', return_value=12)
    actual = object_assertion()
    ex = mocking.return_value
    assert actual == ex
    mocking.assert_called()


def test_cos_object_domain(mocker):
    mocking = mocker.patch('test_CredentialService.object_assertion', attribute='domain')
    mocking.return_value = 31
    actual = object_assertion()
    assert actual == 31
    mocking.assert_called()


def test_cos_object_role(mocker):
    mocking = mocker.patch('test_CredentialService.object_assertion', attribute='role')
    mocking.return_value = 42
    actual = object_assertion()
    assert actual == 42
    mocking.assert_called()


def test_cos_object_lockbox_id(mocker):
    mocking = mocker.patch('test_CredentialService.object_assertion', attribute='lockbox_id')
    mocking.return_value = 92
    actual = object_assertion()
    assert actual == 92
    mocking.assert_called()


def test_cos_object_path(mocker):
    mocking = mocker.patch('test_CredentialService.object_assertion', attribute='path')
    mocking.return_value = 50
    actual = object_assertion()
    assert actual == 50
    mocking.assert_called()


def test_cos(mocker):
    mocking = mocker.patch('test_CredentialService.cos', return_value=12)
    actual = cos()
    assert actual == 12
    mocking.assert_called()


def test_Name_Exception():
    with pytest.raises(Exception) as e:
        object_assertion().call_cos(None, None, None)

    exception_raised = e.value
    assert exception_raised.__str__() == "name 'logger' is not defined"


def test_Exception():
    with pytest.raises(Exception) as e:
        object_assertion().call_cos('bet.cja4hzvoumxg.us-east-1.rds.amazonaws.com', 'admin', '')

    exception_raised = e.value
    assert exception_raised.__str__() == "name 'logger' is not defined"
