import argparse
import json
import os

from util.loader import load_dataset

from util.uc import RawUseCase
from datasetparsers.etoursparser import EtoursParser

PATH_INPUT: str = '../../data/input/raw/'
PATH_OUTPUT: str = '../../data/input/preprocessed/'

if __name__ == "__main__":
    # parse the arguments
    parser = argparse.ArgumentParser(description='Define the type of comparison.')
    parser.add_argument(
        '--dataset', 
        choices=['etours', 'itrust'], 
        required=True, 
        help='Name of the dataset to parse (which should also be the directory name)')
    args = parser.parse_args()

    raw_use_cases: list[str] = []
    use_cases: list[RawUseCase] = []

    if args.dataset == 'etours':
        raw_use_cases = load_dataset(data_path=PATH_INPUT, dataset_name='eTour')
        ucparser = EtoursParser()
        # parse the raw use cases into RawUseCase objects
        parsed_use_cases = [
            ucparser.parse(ucid, raw_use_cases[ucid]) for ucid in raw_use_cases]

    os.makedirs(PATH_OUTPUT, exist_ok=True)

    for use_case in parsed_use_cases:
        output_file = os.path.join(PATH_OUTPUT, f"{use_case.id}.json")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(use_case.to_dict(), f, ensure_ascii=False, indent=4)