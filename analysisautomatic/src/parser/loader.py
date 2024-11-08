import os

from util.uc import UseCase
from parser.usecaseparser import AbstractUseCaseParser

def read_file_as_string(file_path):
    """
    Reads a text file and returns its content as a string.

    :param file_path: Path to the text file
    :return: Content of the file as a string
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()
    
def parse_dataset(dataset_name: str, parser: AbstractUseCaseParser) -> list[UseCase]:
    """
    Parses a dataset containing use cases and returns a list of UseCase objects.

    :param dataset_name: Name of the dataset file
    :return: List of UseCase objects
    """
    dataset_path: str = f'./../data/{dataset_name}/'

    use_case_files = [f for f in os.listdir(dataset_path) if os.path.isfile(os.path.join(dataset_path, f))]

    for use_case_file in use_case_files[:1]:
        use_case_id: str = use_case_file.split('.')[0]
        use_case_text: str = read_file_as_string(os.path.join(dataset_path, use_case_file))

        uc: UseCase = parser.parse(ucid=use_case_id, uc_text=use_case_text)
        print(uc)
        