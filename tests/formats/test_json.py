# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring,duplicate-code,too-many-locals
import unittest.mock
import unittest
import io
import json
from cfgrw.formats.json import read_values
from . import TEST_PARAMS

JSON_WITH_PARAMS = """{
    "datefmt": "%Y",
    "filename": "somecfgrw.log",
    "filemode": "w",
    "format": "%(some_extra1)s Some Log %(asctime)s",
    "level": "critical",
    "extras": {
        "some_extra1": "some_value1",
        "some_extra2": "some_value2"
    }
}"""

JSON_WITHOUT_PARAMS = """{
    "foo": "bar"
}"""

JSON_EMPTY = "{}"

JSON_INVALID = "---\nhello"


class TestJson(unittest.TestCase):

    def test_read_values_with_json_having_props(self):
        values = read_values(io.StringIO(JSON_WITH_PARAMS), TEST_PARAMS, {})
        self.assertEqual(values["datefmt"], "%Y")
        self.assertEqual(values["filename"], "somecfgrw.log")
        self.assertEqual(values["filemode"], "w")
        self.assertEqual(values["format"], "%(some_extra1)s Some Log %(asctime)s")
        self.assertEqual(values["level"], "critical")
        extras = values["extras"]
        self.assertEqual(len(extras.keys()), 2)
        self.assertEqual(extras["some_extra1"], "some_value1")
        self.assertEqual(extras["some_extra2"], "some_value2")

    def test_read_values_with_json_not_having_props(self):
        values = read_values(io.StringIO(JSON_WITHOUT_PARAMS), TEST_PARAMS, {})
        self.assertFalse("datefmt" in values)
        self.assertFalse("filename" in values)
        self.assertFalse("filemode" in values)
        self.assertFalse("format" in values)
        self.assertFalse("level" in values)
        self.assertFalse("extras" in values)

    def test_read_values_with_empty_json(self):
        values = read_values(io.StringIO(JSON_EMPTY), TEST_PARAMS, {})
        self.assertFalse("datefmt" in values)
        self.assertFalse("filename" in values)
        self.assertFalse("filemode" in values)
        self.assertFalse("format" in values)
        self.assertFalse("level" in values)
        self.assertFalse("extras" in values)

    def test_read_values_with_invalid_json(self):
        with self.assertRaises(json.decoder.JSONDecodeError):
            read_values(io.StringIO(JSON_INVALID), TEST_PARAMS, {})
