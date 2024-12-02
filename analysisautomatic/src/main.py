from util.uc import RawUseCase, UseCase

import pandas as pd

from parser.loader import parse_dataset
from parser.etoursparser import EtoursParser

from preprocessor.uc_preprocessor import UseCasePreprocessor 
from processor.processor import Processor

def main():
    # STEP 1: parse the raw test files into RawUseCase objects
    raw_use_cases: list[RawUseCase] = []
    parsers = [('eTour', EtoursParser())]
    for dataset, parser in parsers:
        parsed = parse_dataset(dataset, parser)
        raw_use_cases = raw_use_cases + parsed
    #TODO: parse the iTrust files as well

    # STEP 2: preprocess the raw use case objects
    preprocessor = UseCasePreprocessor()
    use_cases: list[UseCase] = [preprocessor.preprocess_use_case(ruc) for ruc in raw_use_cases]

    # STEP 3: process the use case by running all processing steps to produce a table of data
    processor = Processor()
    results: pd.DataFrame = processor.apply_processors(ucs=use_cases)

    # STEP 4: save the processed data to a file
    results.to_csv('../data/output/rq4tlr-automatic-variables.csv', index=False)

if __name__ == "__main__":
    main()