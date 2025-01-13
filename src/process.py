import os, json
import pandas as pd

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

def main():
    # STEP 1: parse the raw test files into RawUseCase objects
    raw_use_cases: list[RawUseCase] = []
    for dataset in ['etour', 'itrust']:
        parsed = get_use_cases(dataset)
        raw_use_cases = raw_use_cases + parsed

    # STEP 2: preprocess the raw use case objects
    preprocessor = UseCasePreprocessor()
    use_cases: list[UseCase] = [
        preprocessor.preprocess_use_case(ruc) for ruc in raw_use_cases]

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