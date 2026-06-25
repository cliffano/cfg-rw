"""Environment variable configuration reader.

Reference: https://en.wikipedia.org/wiki/Environment_variable
"""

import os


def read_values(props: list, opts: dict) -> dict:  # pylint: disable=unused-argument
    """Read property values from environment variables.

    Each property name is upper-cased and prepended with ``opts["prefix"]`` to form
    the environment variable name, e.g. property ``level`` with prefix ``APP_``
    resolves to ``APP_LEVEL``. Properties whose environment variable is not set are
    omitted from the result.

    :param props: Property names to read.
    :type props: list[str]
    :param opts: Reader options. Required key:

        - ``prefix`` *(str)* — prefix prepended to each upper-cased property name.
    :type opts: dict
    :returns: Mapping of property names to their environment variable values for all
        found properties.
    :rtype: dict
    """
    values = {}
    prefix = opts["prefix"]
    for prop in props:
        env_var = prefix + prop.upper()
        if env_var in os.environ:
            values[prop] = os.environ[env_var]
    return values
