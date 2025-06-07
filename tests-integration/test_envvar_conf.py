# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring,duplicate-code,too-many-locals
import unittest
import os
import os.path
from cfgrw import CFGRW


class TestEnvVarConf(unittest.TestCase):

    def setUp(self):
        os.environ["CFGRW_HANDLERS"] = "stream,file"
        os.environ["CFGRW_DATEFMT"] = "%Y"
        os.environ["CFGRW_FILENAME"] = "somecfgrw.log"
        os.environ["CFGRW_FILEMODE"] = "w"
        os.environ["CFGRW_FORMAT"] = "%(some_extra1)s Some Log %(asctime)s"
        os.environ["CFGRW_LEVEL"] = "info"
        os.environ["CFGRW_EXTRAS"] = "some_extra1=some_value1,some_extra2=some_value2"

    def tearDown(self):
        os.unsetenv("CFGRW_HANDLERS")
        if "CFGRW_HANDLERS" in os.environ:
            os.environ.pop("CFGRW_HANDLERS")
        os.unsetenv("CFGRW_DATEFMT")
        if "CFGRW_DATEFMT" in os.environ:
            os.environ.pop("CFGRW_DATEFMT")
        os.unsetenv("CFGRW_FORMAT")
        if "CFGRW_FORMAT" in os.environ:
            os.environ.pop("CFGRW_FORMAT")
        os.unsetenv("CFGRW_LEVEL")
        if "CFGRW_LEVEL" in os.environ:
            os.environ.pop("CFGRW_LEVEL")
        os.unsetenv("CFGRW_EXTRAS")
        if "CFGRW_EXTRAS" in os.environ:
            os.environ.pop("CFGRW_EXTRAS")

    def test_read_with_conf_file_having_existing_props_values(self):
        cfgrw = CFGRW()
        values = cfgrw.read(["handlers", "level", "extras"], {"prefix": "CFGRW_"})
        self.assertEqual(values["handlers"], "stream,file")
        self.assertEqual(values["level"], "info")

    def test_read_with_conf_file_having_inexisting_props_values(self):
        cfgrw = CFGRW()
        values = cfgrw.read(["xhandlers", "xlevel", "xextras"], {"prefix": "CFGRW_"})
        self.assertTrue("xhandlers" not in values)
        self.assertTrue("xlevel" not in values)
        self.assertTrue("xextras" not in values)
