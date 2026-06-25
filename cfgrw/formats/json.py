"""JSON file configuration reader.

Reference: https://www.json.org/
"""

import json


def read_values(
    conf_stream: object, props: list, opts: dict  # pylint: disable=unused-argument
) -> dict:
    """Read property values from a JSON file.

    Only top-level keys matching the requested property names are included in the result.

    :param conf_stream: Readable stream of the JSON file content.
    :type conf_stream: IO[str]
    :param props: Property names to read.
    :type props: list[str]
    :param opts: Reader options (unused for JSON).
    :type opts: dict
    :returns: Mapping of property names to their values for all found properties.
    :rtype: dict
    """
    values = {}
    conf_json = json.load(conf_stream)
    for prop in props:
        if prop in conf_json:
            values[prop] = conf_json[prop]
    return values
