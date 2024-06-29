import re


def check_string_format(input_string, expected_pattern):
    match = re.fullmatch(expected_pattern, input_string)
    if match is not None:
        print("******")
        print(input_string)
        print(expected_pattern)
    return match is not None
