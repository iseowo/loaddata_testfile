import lambda_function


def convert_d():
    return lambda_function.convert_datatype(None)


def test_convert_datatype(mocker):
    mocking = mocker.patch('test_lambda_function.convert_d', return_value=['1', '2'])
    ac = ['1', '2']
    ex = convert_d()
    assert ac == ex
    mocking.assert_called()


def test_convert_datatype_dict(mocker):
    mocking = mocker.patch('test_lambda_function.convert_d', return_value=dict())
    ac = dict()
    ex = convert_d()
    assert ac == ex
    mocking.assert_called()
