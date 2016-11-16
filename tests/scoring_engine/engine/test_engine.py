import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../../'))

from scoring_engine.engine.engine import Engine
from scoring_engine.db import DB

from scoring_engine.models.team import Team
from scoring_engine.models.service import Service
from scoring_engine.models.property import Property
from scoring_engine.models.check import Check


class TestEngine():

    def setup(self):
        self.db = DB()
        self.db.connect()
        self.db.setup()

    def teardown(self):
        self.db.destroy()

    def test_init(self):
        engine = Engine()
        from ipv4.ssh import SSHCheck
        from ipv4.icmp import ICMPCheck
        expected_checks = [ICMPCheck, SSHCheck]
        assert engine.checks == expected_checks

    def test_current_round_init(self):
        engine = Engine(current_round=100)
        assert engine.current_round == 100

    def test_total_rounds_init(self):
        engine = Engine(total_rounds=100)
        assert engine.total_rounds == 100

    def test_shutdown(self):
        engine = Engine()
        assert engine.last_round is False
        engine.shutdown()
        assert engine.last_round is True

    def test_run_one_round(self):
        engine = Engine(current_round=1, total_rounds=1)
        assert engine.rounds_run == 0
        assert engine.current_round == 1
        engine.run()
        assert engine.rounds_run == 1
        assert engine.current_round == 2

    def test_run_ten_rounds(self):
        engine = Engine(total_rounds=10)
        assert engine.current_round == 1
        assert engine.rounds_run == 0
        engine.run()
        assert engine.rounds_run == 10
        assert engine.current_round == 11

    def test_run_hundred_rounds(self):
        engine = Engine(current_round=50, total_rounds=100)
        assert engine.current_round == 50
        assert engine.rounds_run == 0
        engine.run()
        assert engine.rounds_run == 100
        assert engine.current_round == 150

    def test_check_name_to_obj_positive(self):
        engine = Engine()
        check_obj = engine.check_name_to_obj("ICMP IPv4 Check")
        from ipv4.icmp import ICMPCheck
        check_obj == ICMPCheck

    def test_check_name_to_obj_negative(self):
        engine = Engine()
        check_obj = engine.check_name_to_obj("Garbage Check")
        assert check_obj is None

    def test_with_one_team(self):
        team = Team(name="Team1", color="Blue")
        self.db.save(team)
        service = Service(name="Example Service 2", team=team, check_name="ICMP IPv4 Check")
        self.db.save(service)

        engine = Engine(current_round=50, total_rounds=100)
        engine.run()