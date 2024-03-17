import re
from collections import deque

from bp_core.utils.exceptions import DatasetHandlerException
from bp_core.utils.singleton import SingletonMeta


class DatasetHandler(metaclass=SingletonMeta):
    def __init__(
        self,
        dataset = None
    ) -> None:
        self.dataset = dataset

    def parse_and_get(self, string_to_format: str):
        match = re.findall("{(.*?)}", str(string_to_format))
        if len(match) > 0:
            if self.dataset._dataset_prefix == '':
                raise DatasetHandlerException(
                    "Please provide the environment of the files using '--dataset-prefix [value]' within CLI arguments")
            file_name = string_to_format[1:string_to_format.index(":") + 1]
            string_to_format = string_to_format.replace(file_name, '')
            file_name = re.findall('[0-9a-zA-Z_-]+', file_name)
            match = re.findall("{(.*?)}", str(string_to_format))
            keys = deque(match[0].split("~"))
            data = self.dataset[f"{self.dataset._dataset_prefix}{file_name[0]}"]
            value = data.get(keys.popleft().strip())
            while keys:
                try:
                    value = value.get(keys.popleft().strip())
                except AttributeError:
                    raise DatasetHandlerException("The provided path is not present in the specified file")
            # the returned value is the value present in the file having the file name and path provided as arguments
            return value
        # return the initial value
        return string_to_format
