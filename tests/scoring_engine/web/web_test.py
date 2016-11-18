import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../../'))

from scoring_engine.web import app
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../'))
from unit_test import UnitTest


class WebTest(UnitTest):

    def setup(self):
        super(WebTest, self).setup()
        self.app = app
        self.client = self.app.test_client()

    def verify_auth_required(self, path):
        resp = self.client.get(path)
        assert resp.status_code == 302
        assert '/login?' in resp.location

    def verify_auth_required_post(self, path):
        resp = self.client.post(path)
        assert resp.status_code == 302
        assert '/login?' in resp.location

    def test_debug(self):
        assert self.app.debug is True
