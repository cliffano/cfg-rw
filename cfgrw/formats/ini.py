"""INI file configuration reader.

Reference: https://en.wikipedia.org/wiki/INI_file
"""

import configparser


def read_values(
    conf_stream: object, props: list, opts: dict
) -> dict:  # pylint: disable=unused-argument
    """Read property values from an INI file.

    Only properties present under the specified section are included in the result.

    :param conf_stream: Readable stream of the INI file content.
    :type conf_stream: IO[str]
    :param props: Property names to read.
    :type props: list[str]
    :param opts: Reader options. Required key:

        - ``section`` *(str)* — INI section name to read properties from.
    :type opts: dict
    :returns: Mapping of property names to their values for all found properties.
    :rtype: dict
    """
    values = {}
    section = opts["section"]
    conf_ini = configparser.ConfigParser()
    conf_ini.read_file(conf_stream)
    for prop in props:
        if prop in conf_ini[section]:
            values[prop] = conf_ini[section][prop]
    return values
