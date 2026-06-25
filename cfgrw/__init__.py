# pylint: disable=too-many-locals,too-few-public-methods
"""Python library for reading configuration properties from files and environment variables."""

import io
import os
from jinja2 import Environment, FileSystemLoader

from .formats.envvar import read_values as read_envvar_values
from .formats.ini import read_values as read_ini_values
from .formats.json import read_values as read_json_values
from .formats.xml import read_values as read_xml_values
from .formats.yaml import read_values as read_yaml_values

JINJA_EXT = ".j2"
"""str: File extension suffix that marks a Jinja2 template."""

CONF_FORMATS = {
    "ini": {"ext": [".ini"], "read_fn": read_ini_values},
    "json": {"ext": [".json"], "read_fn": read_json_values},
    "xml": {"ext": [".xml"], "read_fn": read_xml_values},
    "yaml": {"ext": [".yaml", ".yml"], "read_fn": read_yaml_values},
}
"""dict: Supported configuration formats mapped to their file extensions and reader functions."""


class CFGRW:
    """Reader for configuration properties from files and environment variables."""

    def __init__(self, conf_file=None) -> None:
        """Initialise CFGRW.

        :param conf_file: Path to the configuration file. When ``None``, all properties
            are read from environment variables.
        :type conf_file: str, optional
        """

        self.conf_file = conf_file
        self.conf_formats = CONF_FORMATS

    def read(  # pylint: disable=dangerous-default-value
        self, props: list, opts={}
    ) -> dict:
        """Read the values of a list of properties.

        When a configuration file is set, properties are read from it first. Any
        properties absent from the file are looked up as environment variables when
        ``prefix`` is provided in ``opts``. When no configuration file is set, all
        properties are read from environment variables.

        Properties not found in any source are silently omitted from the result.

        :param props: Property names to read.
        :type props: list[str]
        :param opts: Reader options. Recognised keys:

            - ``section`` *(str)* — section name, required for INI files.
            - ``prefix`` *(str)* — environment variable prefix, required for env var reads
              and env var fallback.
        :type opts: dict
        :returns: Mapping of property names to their values for all found properties.
        :rtype: dict
        """

        if self.conf_file:
            if self.conf_file.endswith(JINJA_EXT):
                j2_template_dir = os.path.dirname(self.conf_file)
                j2_template_file = os.path.basename(self.conf_file)
                j2_file_loader = FileSystemLoader(j2_template_dir)
                j2_env = Environment(loader=j2_file_loader)
                template = j2_env.get_template(j2_template_file)
                conf_string = template.render({"env": dict(os.environ)})
                conf_format = self._id_conf_format(
                    self.conf_file.replace(JINJA_EXT, "")
                )
                read_fn = conf_format["read_fn"]
                values = read_fn(io.StringIO(conf_string), props, opts)
            else:
                conf_format = self._id_conf_format(self.conf_file)
                read_fn = conf_format["read_fn"]
                with open(self.conf_file, "r", encoding="utf-8") as conf_stream:
                    values = read_fn(conf_stream, props, opts)
            missing_props = [p for p in props if p not in values]
            if missing_props and "prefix" in opts:
                values.update(read_envvar_values(missing_props, opts))
        else:
            values = read_envvar_values(props, opts)

        return values

    def _id_conf_format(self, conf_file: str) -> dict:
        """Identify the configuration format settings for a given file path.

        :param conf_file: Path to the configuration file.
        :type conf_file: str
        :returns: Format settings dict with ``ext`` and ``read_fn`` keys,
            or ``None`` if no supported format matches.
        :rtype: dict or None
        """

        for (
            conf_format,  # pylint: disable=unused-variable
            settings,
        ) in CONF_FORMATS.items():
            if conf_file.endswith(tuple(settings["ext"])):
                return settings

        return None
