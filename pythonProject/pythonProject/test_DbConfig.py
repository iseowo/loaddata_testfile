import DBConfig


def test_db_username():
    assert DBConfig.db_username == 'bet_test_dataloader'


def test_db_name():
    assert DBConfig.db_name == 'BET'


def test_db_endpoint():
    assert DBConfig.db_endpoint == 'bet.cja4hzvoumxg.us-east-1.rds.amazonaws.com'
