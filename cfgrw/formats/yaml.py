"""YAML file configuration reader.

Reference: https://yaml.org/
"""

import yaml


def read_values(
    conf_stream: object, props: list, opts: dict  # pylint: disable=unused-argument
) -> dict:
    """Read property values from a YAML file.

    Only top-level keys matching the requested property names are included in the result.
    An empty YAML document returns an empty dict without error.

    :param conf_stream: Readable stream of the YAML file content.
    :type conf_stream: IO[str]
    :param props: Property names to read.
    :type props: list[str]
    :param opts: Reader options (unused for YAML).
    :type opts: dict
    :returns: Mapping of property names to their values for all found properties.
    :rtype: dict
    """
    values = {}
    conf_yaml = yaml.safe_load(conf_stream)
    if conf_yaml is not None:
        for prop in props:
            if prop in conf_yaml:
                values[prop] = conf_yaml[prop]
    return values
