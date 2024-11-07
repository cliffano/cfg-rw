# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring,duplicate-code,too-many-locals
import unittest.mock
import unittest
import io
import xml
from cfgrw.formats.xml import read_values
from . import TEST_PARAMS

XML_WITH_PARAMS = """<?xml version="1.0" encoding="UTF-8"?>
<cfgrw>
  <datefmt>%Y</datefmt>
  <filename>somecfgrw.log</filename>
  <filemode>w</filemode>
  <format>%(some_extra1)s Some Log %(asctime)s</format>
  <level>critical</level>
  <extras>some_extra1=some_value1,some_extra2=some_value2</extras>
</cfgrw>
"""

XML_WITHOUT_PARAMS = """<?xml version="1.0" encoding="UTF-8"?>
<cfgrw>
  <foo>bar</foo>
</cfgrw>
"""

XML_EMPTY = '<?xml version="1.0" encoding="UTF-8"?><cfgrw></cfgrw>'

XML_INVALID = ">%%%{foobar}!!!<"


class TestXml(unittest.TestCase):

    def test_read_values_with_xml_having_params(self):
        values = read_values(io.StringIO(XML_WITH_PARAMS), TEST_PARAMS, {})
        self.assertEqual(values["datefmt"], "%Y")
        self.assertEqual(values["filename"], "somecfgrw.log")
        self.assertEqual(values["filemode"], "w")
        self.assertEqual(values["format"], "%(some_extra1)s Some Log %(asctime)s")
        self.assertEqual(values["level"], "critical")
        self.assertEqual(
            values["extras"], "some_extra1=some_value1,some_extra2=some_value2"
        )

    def test_read_values_with_xml_not_having_params(self):
        values = read_values(io.StringIO(XML_WITHOUT_PARAMS), TEST_PARAMS, {})
        self.assertFalse("datefmt" in values)
        self.assertFalse("filename" in values)
        self.assertFalse("filemode" in values)
        self.assertFalse("format" in values)
        self.assertFalse("level" in values)
        self.assertFalse("extras" in values)

    def test_read_values_with_empty_xml(self):
        values = read_values(io.StringIO(XML_EMPTY), TEST_PARAMS, {})
        self.assertFalse("datefmt" in values)
        self.assertFalse("filename" in values)
        self.assertFalse("filemode" in values)
        self.assertFalse("format" in values)
        self.assertFalse("level" in values)
        self.assertFalse("extras" in values)

    def test_read_values_with_invalid_xml(self):
        with self.assertRaises(xml.etree.ElementTree.ParseError):
            read_values(io.StringIO(XML_INVALID), TEST_PARAMS, {})
