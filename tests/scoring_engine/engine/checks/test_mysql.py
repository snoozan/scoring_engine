from tests.scoring_engine.engine.checks.check_test import CheckTest


class TestMYSQLCheck(CheckTest):
    check_name = 'MYSQLCheck'
    properties = {
        'database': 'wordpressdb',
        'command': 'show tables'
    }
    accounts = {
        'pwnbus': 'pwnbuspass'
    }
    cmd = "mysql -h '127.0.0.1' -P 100 -u 'pwnbus' -p'pwnbuspass' 'wordpressdb' -e 'show tables'"
