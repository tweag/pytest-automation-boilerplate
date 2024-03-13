import os
import re

from bp_core.utils.dataset_handler import DatasetHandler

def text_formatted(string_to_format: str):
    """text_formatted

    Arguments
    ---------
    `string_to_format: str`

    Returns
    -------
    Formatted `string_to_format` with environment variable / dataset
    """
    if string_to_format is not None:
        type_ = type(string_to_format)
        string_to_format = str(string_to_format)
        re_var = r"{%[0-9a-zA-Z_-]+%}"
        matches = re.findall(re_var, string_to_format)
        if len(matches) == 0:
            dataset = DatasetHandler()
            string_to_format = dataset.parse_and_get(string_to_format)
        else:
            for match in matches:
                match_ = match[2:-2]
                string_to_format = string_to_format.replace(match, os.environ.get(match_, ""))
        return type_(string_to_format)
    return string_to_format
