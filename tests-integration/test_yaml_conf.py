# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring,duplicate-code,too-many-locals
import unittest
from cfgrw import CFGRW


class TestYamlConf(unittest.TestCase):

    def test_read_with_conf_file_having_existing_props_values(self):
        cfgrw = CFGRW(conf_file="tests-integration/fixtures/cfgrw.yaml")
        values = cfgrw.read(["handlers", "level", "extras"])
        self.assertEqual(values["handlers"], "stream,file")
        self.assertEqual(values["level"], "info")
        self.assertEqual(values["extras"]["env"], "someenv")

    def test_read_with_conf_file_having_inexisting_props_values(self):
        cfgrw = CFGRW(conf_file="tests-integration/fixtures/cfgrw.yaml")
        values = cfgrw.read(["xhandlers", "xlevel", "xextras"])
        self.assertTrue("xhandlers" not in values)
        self.assertTrue("xlevel" not in values)
        self.assertTrue("xextras" not in values)

    def test_read_with_conf_file_having_empty_config(self):
        cfgrw = CFGRW(conf_file="tests-integration/fixtures/cfgrw-empty.yaml")
        values = cfgrw.read(["handlers", "level", "extras"])
        self.assertTrue("handlers" not in values)
        self.assertTrue("level" not in values)
        self.assertTrue("extras" not in values)
