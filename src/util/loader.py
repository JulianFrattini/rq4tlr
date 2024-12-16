import os
from util.readfile import read_file_as_string
import re

def get_unique_uc_ids(use_case_file_names: list[str]) -> list[int]:
    """
    The text files containing use cases follow a naming convention that always starts with the use case id (e.g., UC1) but may be followd by a suffix that identifies it as a subflow (e.g., UC1E1). This function extracts the unique use case ids from the file names."""

    unique_ids = set()
    for file_name in use_case_file_names:
        match = re.match(r'UC(\d+)', file_name)
        if match:
            unique_ids.add(int(match.group(1)))
    return list(unique_ids)
    
def load_dataset(data_path: str, dataset_name: str) -> dict[str, dict]:
    """
    Loads a set of raw use cases contained in text files

    :param dataset_path: Path to the directory containing the use case files
    :return: dictionary associating the use case id with a dictonary associating a file name with its textual content
    """
    # get a list of all use case files in the dataset directory
    dataset_path: str = os.path.join(data_path, dataset_name)
    use_case_files = [
        f for f in os.listdir(dataset_path) 
        if os.path.isfile(os.path.join(dataset_path, f))]

    # determine the unique use case IDs
    unique_ids = get_unique_uc_ids(use_case_files)

    # prepare an empty list for the parsed use cases
    raw_use_cases: dict[str, dict] = {}
    for uid in unique_ids:
        # determine all file names relevant to this use case (i.e., all files labeled UC{uid}, UC{uid}E, or UC{uid}S)
        relevant_files: list[str] = [
            filename for filename in use_case_files 
            if (f'UC{uid}.txt' in filename) or (f'UC{uid}E' in filename) or (f'UC{uid}S' in filename)]
            
        # parse these files and associate the filename with the textual content
        files: dict[str, str] = {}
        for filename in relevant_files:
            files[filename] = read_file_as_string(os.path.join(dataset_path, filename))

        # associate the use case id with the files
        raw_use_cases[f'UC{uid}'] = files

    return raw_use_cases
        