import os, argparse, json

import pandas as pd

from structure.rawusecase import RawUseCase

from util.static import PATH_RAW_OUTPUT, PATH_RAW_SUPPLEMENTARY
import re

def get_items(dataset: str) -> list[RawUseCase]:
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

def get_subflow_id(subflowid: str) -> (int, int):
    subflowtype = 0 if ('S' in subflowid) else 1

    subflow_number = 0
    if 'S' in subflowid or 'E' in subflowid:
        # extract the id of the subflow from subflowid by obtaining the number after the 'S' or 'E'
        subflow_number = int(re.search(r'[SE](\d+)', subflowid).group(1))

    return (subflowtype, subflow_number)

def get_item_list(dataset: list[RawUseCase], level: str) -> pd.DataFrame:
    item_list: pd.DataFrame = None
    if level == 'requirement':
        item_list = pd.DataFrame(columns=['UC', 'Subflowtype', 'Subflow', 'File'])
    elif level == 'sentence':
        item_list = pd.DataFrame(columns=['UC', 'Subflowtype', 'Subflow', 'File', 'Line'])

    for entry in dataset:
        # extract the number of the use case from the entry.id
        uc_number = re.search(r'UC(\d+)', entry.id).group(1)

        # create a new dictionary that contains the key-value pairs of both entry.main and entry.alternative
        all_subflows = {**entry.main, **entry.alternative}
        for subflowid in all_subflows:
            subflowtype, subflow_number = get_subflow_id(subflowid)

            if level == 'requirement':
                item_list = item_list.append({
                    'UC': uc_number,
                    'Subflowtype': subflowtype,
                    'Subflow': subflow_number,
                    'File': subflowid
                    }, ignore_index=True)
            elif level == 'sentence':
                for sentenceid, sentence in enumerate(all_subflows[subflowid]):
                    item_list = item_list.append({
                        'UC': uc_number,
                        'Subflowtype': subflowtype,
                        'Subflow': subflow_number,
                        'File': subflowid,
                        'Line': sentenceid+1
                        }, ignore_index=True)

    # cast the UC and subflow column to integer and sort the DataFrame
    item_list['UC'] = item_list['UC'].astype(int)
    item_list['Subflow'] = item_list['Subflow'].astype(int)
    # sort the dataframe by the UC and subflow number
    item_list = item_list.sort_values(['UC', 'Subflowtype', 'Subflow'])

    return item_list

if __name__ == "__main__":
    # parse the arguments
    parser = argparse.ArgumentParser(description='Define the type of comparison.')
    parser.add_argument(
        '-d', '--dataset', choices=['etour', 'itrust'], required=True, 
        help='Name of the dataset to parse (which should also be the directory name)')
    parser.add_argument(
        '-l', '--level', choices=['requirement', 'sentence'], required=True, 
        help='Level of granularity to obtain the item list')
    args = parser.parse_args()

    items = get_items(args.dataset)

    item_list = get_item_list(items, args.level)

    # store the item_list as a xlsx file
    output_path = os.path.join(PATH_RAW_SUPPLEMENTARY, f'{args.dataset}-{args.level}.xlsx')
    item_list.to_excel(output_path, sheet_name='Indices', index=False)
