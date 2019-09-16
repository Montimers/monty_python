def add_to_hex_string_length(hex_string, desired_hex_string_length, character_to_add):
    """
    Adds leading values to a hex string to increase it's length
    :param hex_string: hex string to add leading characters to
    :param desired_hex_string_length: length for hex string to be
    :param character_to_add: which hex character to add (usually "0")
    :return:
    """

    while len(hex_string) < desired_hex_string_length:
        hex_string = character_to_add + hex_string
    return hex_string


def convert_int_to_hex_string(int_value):
    """
    Converts an int to a hex string (which is like turning the int 15 to the string "F"
    This is surpisingly not as easy to do as it should be but thankfully Python3.7 has f strings which are wonderful
    :param int_value: int to convert to a hex string
    :return: hex string representation of int_value
    """
    return f'{int_value:X}'
