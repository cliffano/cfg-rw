# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring,duplicate-code,too-many-locals
from unittest.mock import patch, mock_open
import unittest
from cfgrw import CFGRW

INI_STRING = """[cfgrw]
datefmt: %%Y
"""


class TestCFGRW(unittest.TestCase):

    def test_cfgrw(self):  # pylint: disable=too-many-arguments

        cfgrw = CFGRW(conf_file="somefile.ini")
        assert cfgrw.conf_file == "somefile.ini"

    @patch("builtins.open", new_callable=mock_open, read_data=INI_STRING)
    @patch("cfgrw.read_ini_values")
    def test_read_with_conf_file_and_opt(
        self, func_read_ini_values, func_open  # pylint: disable=unused-argument
    ):

        mock_values = {"handlers": "somehandler"}
        func_read_ini_values.return_value = mock_values

        with open("somefile.ini", "r", encoding="utf8") as file_handle:
            assert file_handle.read() == INI_STRING

        cfgrw = CFGRW(conf_file="somefile.ini")

        # Need to overwrite CONF_FORMATS despite using a patched cfgrw.read_ini_values
        # because the CONF_FORMATS already point to the unpatched cfgrw.read_ini_values
        # when CFGRW is initialised
        cfgrw.conf_formats["ini"]["read_fn"] = func_read_ini_values

        values = cfgrw.read(["handlers"], {"section": "cfgrw"})
        assert values == mock_values

    @patch("builtins.open", new_callable=mock_open, read_data=INI_STRING)
    @patch("cfgrw.read_envvar_values")
    @patch("cfgrw.read_ini_values")
    def test_read_with_conf_file_missing_prop_falls_back_to_envvar(
        self,
        func_read_ini_values,
        func_read_envvar_values,
        func_open,  # pylint: disable=unused-argument
    ):

        func_read_ini_values.return_value = {"handlers": "somehandler"}
        func_read_envvar_values.return_value = {"level": "DEBUG"}

        cfgrw = CFGRW(conf_file="somefile.ini")
        cfgrw.conf_formats["ini"]["read_fn"] = func_read_ini_values

        values = cfgrw.read(
            ["handlers", "level"], {"section": "cfgrw", "prefix": "APP_"}
        )

        assert values == {"handlers": "somehandler", "level": "DEBUG"}
        func_read_envvar_values.assert_called_once_with(
            ["level"], {"section": "cfgrw", "prefix": "APP_"}
        )

    @patch("builtins.open", new_callable=mock_open, read_data=INI_STRING)
    @patch("cfgrw.read_envvar_values")
    @patch("cfgrw.read_ini_values")
    def test_read_with_conf_file_all_props_missing_falls_back_to_envvar(
        self,
        func_read_ini_values,
        func_read_envvar_values,
        func_open,  # pylint: disable=unused-argument
    ):

        func_read_ini_values.return_value = {}
        func_read_envvar_values.return_value = {
            "handlers": "somehandler",
            "level": "DEBUG",
        }

        cfgrw = CFGRW(conf_file="somefile.ini")
        cfgrw.conf_formats["ini"]["read_fn"] = func_read_ini_values

        values = cfgrw.read(
            ["handlers", "level"], {"section": "cfgrw", "prefix": "APP_"}
        )

        assert values == {"handlers": "somehandler", "level": "DEBUG"}
        func_read_envvar_values.assert_called_once_with(
            ["handlers", "level"], {"section": "cfgrw", "prefix": "APP_"}
        )

    @patch("builtins.open", new_callable=mock_open, read_data=INI_STRING)
    @patch("cfgrw.read_envvar_values")
    @patch("cfgrw.read_ini_values")
    def test_read_with_conf_file_missing_prop_not_in_envvar_returns_prop_absent(
        self,
        func_read_ini_values,
        func_read_envvar_values,
        func_open,  # pylint: disable=unused-argument
    ):

        func_read_ini_values.return_value = {"handlers": "somehandler"}
        func_read_envvar_values.return_value = {}

        cfgrw = CFGRW(conf_file="somefile.ini")
        cfgrw.conf_formats["ini"]["read_fn"] = func_read_ini_values

        values = cfgrw.read(
            ["handlers", "level"], {"section": "cfgrw", "prefix": "APP_"}
        )

        assert values == {"handlers": "somehandler"}
        assert "level" not in values
        func_read_envvar_values.assert_called_once_with(
            ["level"], {"section": "cfgrw", "prefix": "APP_"}
        )
