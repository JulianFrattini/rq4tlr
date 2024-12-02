import os

from util.uc import RawUseCase
from parser.usecaseparser import AbstractUseCaseParser

def read_file_as_string(file_path):
    """
    Reads a text file and returns its content as a string.

    :param file_path: Path to the text file
    :return: Content of the file as a string
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()
    
def parse_dataset(dataset_name: str, parser: AbstractUseCaseParser) -> list[RawUseCase]:
    """
    Parses a dataset containing use cases and returns a list of UseCase objects.

    :param dataset_name: Name of the dataset file
    :return: List of UseCase objects
    """
    # get a list of all use case files in the dataset directory
    dataset_path: str = f'./../data/input/{dataset_name}/'
    use_case_files = [f for f in os.listdir(dataset_path) if os.path.isfile(os.path.join(dataset_path, f))]

    # prepare an empty list for the parsed use cases
    use_cases: list[RawUseCase] = []

    for use_case_file in use_case_files:
        # determine the id and text of the use case
        use_case_id: str = f'{dataset_name}-{use_case_file.split(".")[0]}'
        use_case_text: str = read_file_as_string(os.path.join(dataset_path, use_case_file))

        # parse the use case with the provided parser
        uc: RawUseCase = parser.parse(ucid=use_case_id, uc_text=use_case_text)
        use_cases.append(uc)

    return use_cases
        