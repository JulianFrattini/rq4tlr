import csv
import os, json
import argparse
from collections import defaultdict
import re

from util.static import LEVELS

import pandas as pd

from structure.TLR_goldstandard import TLR_goldstandard
from util.static import PATH_RAW_GOLDSTANDARDS
from structure.rawusecase import RawUseCase
from structure.usecase import UseCase

from preprocessor.uc_preprocessor import UseCasePreprocessor 
from processor.processor import Processor

from util.static import PATH_OUTPUT, PATH_RAW_OUTPUT


def formatted_uc_sort_key(filename: str) -> tuple[int, str]:
    match = re.match(r'UC(\d+)\.json$', filename)
    if not match:
        return (10**9, filename)
    return (int(match.group(1)), filename)

def get_use_cases(dataset: str) -> list[RawUseCase]:
    """Read the use cases from the dataset folder and return them as a list of RawUseCase objects
    
    :param dataset: the dataset to get the use cases from
    :return: the list of use cases
    """
    path: str = os.path.join(PATH_RAW_OUTPUT, dataset)
    
    items: list[RawUseCase] = []
    for filename in sorted(os.listdir(path), key=formatted_uc_sort_key):
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
    for filename in sorted(os.listdir(path)):
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


def main(selected_level: str):
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
    level_results = {}
    for level in LEVELS:
        if selected_level == level or selected_level == 'all':
            results: pd.DataFrame = processor.apply_processors(level=level, ucs=use_cases)
            output_filename: str = os.path.join(PATH_OUTPUT, f'rq4tlr-automatic-{level}.csv')
            results.to_csv(output_filename, index=False)
            level_results[level] = results

    # STEP 4: aggregate to goldstandard level
    final_df = aggregate_dataframes(level_results)
    if final_df is not None:
        output_filename: str = os.path.join(PATH_OUTPUT, f'rq4tlr-automatic-aggregated.csv')
        final_df.to_csv(output_filename, index=False)


def aggregate_dataframes(level_results):
    if 'sentence' not in level_results:
        return None

    # First merge subflow and sentence
    # Identify key columns
    key_columns = ["dataset", "uc", "file"]
    # Define aggregation dynamically
    bool_columns = level_results["sentence"].select_dtypes(include=bool).columns
    agg_funcs = {col: "mean" for col in bool_columns}  # Compute ratio of `True` values
    agg_funcs.update({col: "max" for col in level_results["sentence"].select_dtypes(include="number").columns if
                      col not in key_columns})  # Apply `.max()` to numeric columns except keys
    # Group by key columns and apply aggregation
    aggregated_df = level_results["sentence"].groupby(key_columns, as_index=False).agg(agg_funcs)
    aggregated_df = aggregated_df.drop(columns=["line"],
                                       errors="ignore")  # Using errors='ignore' to prevent errors if "line" column is not found
    # Rename columns for clarity
    aggregated_df = aggregated_df.rename(columns={col: f'ratio_of_{col}' for col in bool_columns})
    aggregated_df = aggregated_df.rename(columns={col: f'max_{col}' for col in aggregated_df.columns if
                                                  col not in key_columns and 'max' in agg_funcs.get(col, '')})

    if 'subflow' not in level_results:
        return aggregated_df

    merged_df = pd.merge(level_results["subflow"], aggregated_df, on=["dataset", "uc", "file"], how="inner")


    # Second merge use case results with dataframe
    # Rename `id` to `uc` for merging
    if 'usecase' not in level_results:
        return merged_df

    extra_df = level_results["usecase"].rename(columns={"id": "uc"})
    # Merge DataFrames
    final_df = pd.merge(extra_df, merged_df, on=["dataset", "uc"], how="right")

    # Columns you want to move to the front
    columns_to_move = ["dataset", "uc", "file"]

    # Get the remaining columns that are not in the 'columns_to_move' list
    remaining_columns = [col for col in final_df.columns if col not in columns_to_move]

    # Create the new column order by putting 'columns_to_move' first
    new_column_order = columns_to_move + remaining_columns

    # Reorder the DataFrame
    final_df = final_df[new_column_order]

    return final_df


if __name__ == "__main__":
    # parse the arguments
    parser = argparse.ArgumentParser(description='Specify the processing configuration')
    parser.add_argument(
        '-l', '--level', 
        choices=LEVELS + ['all'], 
        required=True, 
        help='Level on which to perform the processing')
    args = parser.parse_args()

    main(selected_level=args.level)