import argparse
import json
import os

from util.loader import load_dataset

from structure.rawusecase import RawUseCase

from parsers.etoursparser import EtoursParser
from parsers.itrustparser import ItrustParser

from util.static import PATH_RAW_INPUT, PATH_RAW_OUTPUT, PATH_RAW_SUPPLEMENTARY

def store_dataset(parsed_use_cases: list[RawUseCase], dataset: str):
    """Store the parsed use cases as JSON files in the output path.
    
    Args:
        parsed_use_cases (list[RawUseCase]): The parsed use cases to store.
    """
    
    # ensure that the output directory exists
    output_path = os.path.join(PATH_RAW_OUTPUT, dataset)
    os.makedirs(output_path, exist_ok=True)

    for use_case in parsed_use_cases:
        output_file = os.path.join(output_path, f"{use_case.id}.json")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(use_case.to_dict(), f, ensure_ascii=False, indent=4)

def main(dataset: str):
    """Main function for parsing the use cases of a dataset.
    
    Args:
        dataset (str): The name of the dataset to parse.
    """
    # load the textual use cases
    raw_use_cases: dict[str, str] = load_dataset(data_path=PATH_RAW_INPUT, dataset_name=dataset)

    # parse the raw use cases into RawUseCase objects
    parsed_use_cases: list[RawUseCase] = []
    if dataset == 'etour':
        ucparser = EtoursParser()
        parsed_use_cases = [
            ucparser.parse(ucid, raw_use_cases[ucid]) for ucid in raw_use_cases]
    elif dataset == 'itrust':
        # parse the use case names which are contained in a supplementary file
        uc_names: dict[str, str] = None
        with open(os.path.join(PATH_RAW_SUPPLEMENTARY, 'itrust-uc-names.json'), 'r', encoding='utf-8') as f:
            uc_names = json.load(f)

        ucparser = ItrustParser()
        for ucid in raw_use_cases:
            uc = ucparser.parse(ucid, raw_use_cases[ucid], uc_names[ucid])
            parsed_use_cases.append(uc)

    # store the use cases as JSON files in the output path
    store_dataset(parsed_use_cases, dataset)

if __name__ == "__main__":
    # parse the arguments
    parser = argparse.ArgumentParser(description='Define the type of comparison.')
    parser.add_argument(
        '--dataset', 
        choices=['etour', 'itrust'], 
        required=True, 
        help='Name of the dataset to parse (which should also be the directory name)')
    args = parser.parse_args()

    # run the main function
    main(args.dataset)