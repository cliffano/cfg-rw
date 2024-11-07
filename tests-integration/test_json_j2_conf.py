# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring,duplicate-code,too-many-locals
import unittest
import os
from cfgrw import CFGRW

class TestJsonJ2Conf(unittest.TestCase):

    def test_read_with_conf_file_having_prop_value_from_envvars(self):
        os.environ['CFGRW_HANDLERS'] = 'stream'
        os.environ['CFGRW_LEVEL'] = 'critical'
        cfgrw = CFGRW(conf_file='tests-integration/fixtures/cfgrw.json.j2')
        values = cfgrw.read(['handlers', 'level', 'extras'])
        self.assertEqual(values['handlers'], 'stream')
        self.assertEqual(values['level'], 'critical')
