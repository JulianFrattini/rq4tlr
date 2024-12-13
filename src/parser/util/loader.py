import os

def read_file_as_string(file_path):
    """
    Reads a text file and returns its content as a string.

    :param file_path: Path to the text file
    :return: Content of the file as a string
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()
    
def load_dataset(data_path: str, dataset_name: str) -> dict[str, str]:
    """
    Loads a set of raw use cases contained in text files

    :param dataset_path: Path to the directory containing the use case files
    :return: List of raw use cases as strings
    """
    # get a list of all use case files in the dataset directory
    dataset_path = os.path.join(data_path, dataset_name)
    use_case_files = [f for f in os.listdir(dataset_path) if os.path.isfile(os.path.join(dataset_path, f))]

    # prepare an empty list for the parsed use cases
    raw_use_cases: dict[str, str] = {}

    for use_case_file in use_case_files:
        # determine the id and text of the use case
        use_case_id: str = f'{dataset_name}-{use_case_file.split(".")[0]}'
        use_case_text: str = read_file_as_string(os.path.join(dataset_path, use_case_file))
        raw_use_cases[use_case_id] = use_case_text

    return raw_use_cases
        