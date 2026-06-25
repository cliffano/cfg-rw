"""XML file configuration reader.

Reference: https://www.w3.org/XML/
"""

import xml.etree.ElementTree as ET


def read_values(
    conf_stream: object, props: list, opts: dict  # pylint: disable=unused-argument
) -> dict:
    """Read property values from an XML file.

    Each property name is matched against direct child elements of the root node.
    Only elements that exist are included in the result.

    :param conf_stream: Readable stream of the XML file content.
    :type conf_stream: IO[str]
    :param props: Property names to read.
    :type props: list[str]
    :param opts: Reader options (unused for XML).
    :type opts: dict
    :returns: Mapping of property names to their element text values for all found properties.
    :rtype: dict
    """
    values = {}
    xml_tree = ET.ElementTree(ET.fromstring(conf_stream.read()))
    conf_xml = xml_tree.getroot()
    for prop in props:
        xml_elem = conf_xml.find(prop)
        if xml_elem is not None:
            values[prop] = xml_elem.text
    return values
