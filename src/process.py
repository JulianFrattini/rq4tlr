import csv
import os, json
from collections import defaultdict

import pandas as pd

from structure.TLR_goldstandard import TLR_goldstandard
from util.static import PATH_RAW_GOLDSTANDARDS
from structure.rawusecase import RawUseCase
from structure.usecase import UseCase

from preprocessor.uc_preprocessor import UseCasePreprocessor 
from processor.processor import Processor

from util.static import PATH_OUTPUT, PATH_RAW_OUTPUT

def get_use_cases(dataset: str) -> list[RawUseCase]:
    """Read the use cases from the dataset folder and return them as a list of RawUseCase objects
    
    :param dataset: the dataset to get the use cases from
    :return: the list of use cases
    """
    path: str = os.path.join(PATH_RAW_OUTPUT, dataset)
    
    items: list[RawUseCase] = []
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        if os.path.isfile(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                obj = json.loads(file.read())
                raw_use_case = RawUseCase(**obj)
                items.append(raw_use_case)

    return items


def get_TLR_goldstandard(dataset) -> TLR_goldstandard:
    """Read the goldstandard from the dataset folder and return them as a list TLR_goldstandard object

       :param dataset: the dataset to get the goldstandard for
       :return: the goldstandard object
    """
    path: str = os.path.join(PATH_RAW_GOLDSTANDARDS, dataset)

    goldstandards: list[TLR_goldstandard] = []
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        if os.path.isfile(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                reader = csv.reader(file, delimiter=',')
                # Skip the header
                next(reader)

                links = defaultdict(list)
                # Populate the dictionary with lists of values
                for row in reader:
                    links[row[0]].append(row[1])

                tlr_goldstandard = TLR_goldstandard(dataset=dataset, links=links)

                goldstandards.append(tlr_goldstandard)

    if len(goldstandards) == 1:
        return goldstandards[0]
    elif len(goldstandards) == 0:
        raise ValueError('No TLR goldstandard found')
    else:
        raise ValueError('Multiple TLR goldstandards found')
    pass


def main():
    # STEP 1: parse the raw test files into RawUseCase objects
    raw_use_cases: list[RawUseCase] = []
    goldstandards = defaultdict(list)
    for dataset in ['etour', 'itrust']:
        parsed = get_use_cases(dataset)
        raw_use_cases = raw_use_cases + parsed
        goldstandards[dataset] = get_TLR_goldstandard(dataset)

    # STEP 2: preprocess the raw use case objects
    preprocessor = UseCasePreprocessor()
    use_cases: list[UseCase] = [
        preprocessor.preprocess_use_case(ruc, goldstandards, raw_use_cases) for ruc in raw_use_cases]

    # STEP 3: process the use case by running all processing steps to produce a table of data
    processor = Processor()
    results_uc: pd.DataFrame = processor.apply_uc_processors(ucs=use_cases)
    output_filename_ucs: str = os.path.join(PATH_OUTPUT, 'rq4tlr-automatic-uc.csv')
    results_uc.to_csv(output_filename_ucs, index=False)
    
    results_subflow: pd.DataFrame = processor.apply_subflow_processors(ucs=use_cases)
    output_filename_subflow: str = os.path.join(PATH_OUTPUT, 'rq4tlr-automatic-subflow.csv')
    results_subflow.to_csv(output_filename_subflow, index=False)
    
    results_sentence: pd.DataFrame = processor.apply_sentence_processors(ucs=use_cases)
    output_filename_sentence: str = os.path.join(PATH_OUTPUT, 'rq4tlr-automatic-sentence.csv')
    results_sentence.to_csv(output_filename_sentence, index=False)

if __name__ == "__main__":
    main()