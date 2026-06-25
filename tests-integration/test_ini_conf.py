# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring,duplicate-code,too-many-locals
import os
import unittest
from cfgrw import CFGRW


class TestIniConf(unittest.TestCase):

    def test_read_with_conf_file_having_existing_props_values(self):
        cfgrw = CFGRW(conf_file="tests-integration/fixtures/cfgrw.ini")
        values = cfgrw.read(["handlers", "level", "extras"], {"section": "cfgrw"})
        self.assertEqual(values["handlers"], "stream,file")
        self.assertEqual(values["level"], "info")

    def test_read_with_conf_file_having_inexisting_props_values(self):
        cfgrw = CFGRW(conf_file="tests-integration/fixtures/cfgrw.ini")
        values = cfgrw.read(["xhandlers", "xlevel", "xextras"], {"section": "cfgrw"})
        self.assertTrue("xhandlers" not in values)
        self.assertTrue("xlevel" not in values)
        self.assertTrue("xextras" not in values)

    def test_read_with_conf_file_having_empty_config(self):
        cfgrw = CFGRW(conf_file="tests-integration/fixtures/cfgrw-empty.ini")
        values = cfgrw.read(["handlers", "level", "extras"], {"section": "cfgrw"})
        self.assertTrue("handlers" not in values)
        self.assertTrue("level" not in values)
        self.assertTrue("extras" not in values)


class TestIniConfWithEnvVarFallback(unittest.TestCase):

    def setUp(self):
        os.environ["CFGRW_XFORMAT"] = "some-xformat-value"

    def tearDown(self):
        os.unsetenv("CFGRW_XFORMAT")
        if "CFGRW_XFORMAT" in os.environ:
            os.environ.pop("CFGRW_XFORMAT")

    def test_read_with_conf_file_missing_prop_falls_back_to_envvar(self):
        cfgrw = CFGRW(conf_file="tests-integration/fixtures/cfgrw.ini")
        values = cfgrw.read(
            ["handlers", "level", "xformat"],
            {"section": "cfgrw", "prefix": "CFGRW_"},
        )
        self.assertEqual(values["handlers"], "stream,file")
        self.assertEqual(values["level"], "info")
        self.assertEqual(values["xformat"], "some-xformat-value")

    def test_read_with_conf_file_missing_prop_not_in_envvar_returns_prop_absent(self):
        cfgrw = CFGRW(conf_file="tests-integration/fixtures/cfgrw.ini")
        values = cfgrw.read(
            ["handlers", "level", "xmissing"],
            {"section": "cfgrw", "prefix": "CFGRW_"},
        )
        self.assertEqual(values["handlers"], "stream,file")
        self.assertEqual(values["level"], "info")
        self.assertTrue("xmissing" not in values)
