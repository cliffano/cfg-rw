# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring,duplicate-code,too-many-locals
from unittest.mock import patch
import unittest.mock
import unittest
import os
from cfgrw.formats.envvar import read_values
from . import TEST_PARAMS

ENVVAR_WITH_PARAMS = {
    "CFGRW_DATEFMT": "%Y",
    "CFGRW_FILENAME": "somecfgrw.log",
    "CFGRW_FILEMODE": "w",
    "CFGRW_FORMAT": "%(some_extra1)s Some Log %(asctime)s",
    "CFGRW_LEVEL": "critical",
    "CFGRW_EXTRAS": "some_extra1=some_value1,some_extra2=some_value2",
}

ENVVAR_WITHOUT_PARAMS = {"CFGRW_FOO": "bar"}

ENVVAR_EMPTY = {}


class TestEnvVar(unittest.TestCase):

    @patch.dict(os.environ, ENVVAR_WITH_PARAMS, clear=True)
    def test_read_values_with_environ_having_params(self):
        values = read_values(TEST_PARAMS, {"prefix": "CFGRW_"})
        self.assertEqual(values["datefmt"], "%Y")
        self.assertEqual(values["filename"], "somecfgrw.log")
        self.assertEqual(values["filemode"], "w")
        self.assertEqual(values["format"], "%(some_extra1)s Some Log %(asctime)s")
        self.assertEqual(values["level"], "critical")
        self.assertEqual(
            values["extras"], "some_extra1=some_value1,some_extra2=some_value2"
        )

    @patch.dict(os.environ, ENVVAR_WITHOUT_PARAMS, clear=True)
    def test_read_values_with_environ_not_having_params(self):
        values = read_values(TEST_PARAMS, {"prefix": "CFGRW_"})
        self.assertFalse("datefmt" in values)
        self.assertFalse("filename" in values)
        self.assertFalse("filemode" in values)
        self.assertFalse("format" in values)
        self.assertFalse("level" in values)
        self.assertFalse("extras" in values)

    @patch.dict(os.environ, ENVVAR_EMPTY, clear=True)
    def test_read_values_with_empty_environ(self):
        values = read_values(TEST_PARAMS, {"prefix": "CFGRW_"})
        self.assertFalse("datefmt" in values)
        self.assertFalse("filename" in values)
        self.assertFalse("filemode" in values)
        self.assertFalse("format" in values)
        self.assertFalse("level" in values)
        self.assertFalse("extras" in values)
