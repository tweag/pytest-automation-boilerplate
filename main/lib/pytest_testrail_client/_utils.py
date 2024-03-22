from os import listdir, path
from os.path import abspath

from gherkin.parser import Parser
from gherkin.token_scanner import TokenScanner


def _get_feature(file_path: str):
    """Read and parse given feature file"""
    print("Reading feature file ", file_path)
    file_obj = open(file_path, "r")
    steam = file_obj.read()
    parser = Parser()
    return parser.parse(TokenScanner(steam))


def _write_feature(file_path: str, line, column, value):
    ln, cn = line - 1, column - 1  # offset from human index to Python index
    count = 0  # initial count of characters
    with open(file_path, "r+") as f:  # open file for reading an writing
        for idx, line in enumerate(f):  # for all line in the file
            if idx < ln:  # before the given line
                count += len(line)  # read and count characters
            elif idx == ln:  # once at the line
                f.seek(count + cn)  # place cursor at the correct character location
                remainder = f.read()  # store all character afterwards
                f.seek(count + cn)  # move cursor back to the correct character location
                f.write(
                    value + remainder.strip()
                )  # insert text and rewrite the remainder
                return  # You're finished!


def _get_list_of_files(absolute_path):
    # create a list of file and sub directories
    # names in the given directory
    if path.isdir(absolute_path):
        list_of_file = listdir(absolute_path)
    else:
        list_of_file = [absolute_path]
    all_files = list()
    # Iterate over all the entries
    for entry in list_of_file:
        # Create full path
        full_path = path.join(absolute_path, entry)
        # If entry is a directory then get the list of files in this directory
        if path.isdir(full_path):
            all_files = all_files + _get_list_of_files(full_path)
        else:
            all_files.append(full_path)
    return all_files
