import os

def read_file_as_string(file_path):
    """
    Reads a text file and returns its content as a string.

    :param file_path: Path to the text file
    :return: Content of the file as a string
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()