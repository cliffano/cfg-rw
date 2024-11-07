# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring,duplicate-code,too-many-locals
import unittest.mock
import unittest
import configparser
import io
from cfgrw.formats.ini import read_values
from . import TEST_PARAMS

INI_WITH_PARAMS = """[cfgrw]
datefmt: %%Y
filename: somecfgrw.log
filemode: w
format: %%(some_extra1)s Some Log %%(asctime)s
level: critical
extras: some_extra1=some_value1,some_extra2=some_value2
"""

INI_WITHOUT_PARAMS = """[cfgrw]
foo: bar
"""

INI_EMPTY = "[cfgrw]"

INI_INVALID = "def[ault]"


class TestIni(unittest.TestCase):

    def test_read_values_with_ini_having_params(self):
        values = read_values(
            io.StringIO(INI_WITH_PARAMS), TEST_PARAMS, {"section": "cfgrw"}
        )
        self.assertEqual(values["datefmt"], "%Y")
        self.assertEqual(values["filename"], "somecfgrw.log")
        self.assertEqual(values["filemode"], "w")
        self.assertEqual(values["format"], "%(some_extra1)s Some Log %(asctime)s")
        self.assertEqual(values["level"], "critical")
        self.assertEqual(
            values["extras"], "some_extra1=some_value1,some_extra2=some_value2"
        )

    def test_read_values_with_ini_not_having_params(self):
        values = read_values(
            io.StringIO(INI_WITHOUT_PARAMS), TEST_PARAMS, {"section": "cfgrw"}
        )
        self.assertFalse("datefmt" in values)
        self.assertFalse("filename" in values)
        self.assertFalse("filemode" in values)
        self.assertFalse("format" in values)
        self.assertFalse("level" in values)
        self.assertFalse("extras" in values)

    def test_read_values_with_empty_ini(self):
        values = read_values(io.StringIO(INI_EMPTY), TEST_PARAMS, {"section": "cfgrw"})
        self.assertFalse("datefmt" in values)
        self.assertFalse("filename" in values)
        self.assertFalse("filemode" in values)
        self.assertFalse("format" in values)
        self.assertFalse("level" in values)
        self.assertFalse("extras" in values)

    def test_read_values_with_invalid_ini(self):
        with self.assertRaises(configparser.MissingSectionHeaderError):
            read_values(io.StringIO(INI_INVALID), TEST_PARAMS, {"section": "cfgrw"})
