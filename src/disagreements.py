import pandas as pd
import argparse

file_name: str = '../data/labeling/rq4tlr-manual-variables.xlsx'

factors_requirement: list[str] = ['Functional Duplication', 
                      'Use Case Naming Problems', 
                      'Inappropriate Scope', 
                      'Incoherent Text Order', 
                      'Inconsistent Level of Abstraction', 
                      'Inputs or Outputs not quantified', 
                      'Contains NFRs', 
                      'Contains Actor-Actor Interaction',
                      'Contains justifications']

factors_sentence: list[str] = ['Coordination Ambiguity', 
                               'Contains UI Design Details']

def compare(rating1: pd.DataFrame, rating2: pd.DataFrame, factors: list[str], compose_id: callable):
    # drop rows with missing values
    rating1 = rating1.dropna(subset=['Rater'])
    rating2 = rating2.dropna(subset=['Rater'])

    # convert factors to boolean and comments to string
    for factor in factors:
        rating1[factor] = rating1[factor].astype(bool)
        rating2[factor] = rating2[factor].astype(bool)
    rating1["Comment"] = rating1["Comment"].astype(str)
    rating2["Comment"] = rating2["Comment"].astype(str)

    rating1['ID'] = rating1.apply(compose_id, axis=1)
    rating2['ID'] = rating2.apply(compose_id, axis=1)

    # determine differences
    for factor in factors:
        for rid in rating1['ID']:
            if rid in rating2['ID'].values:
                value1 = rating1.loc[rating1['ID'] == rid, factor].values[0]
                value2 = rating2.loc[rating2['ID'] == rid, factor].values[0]

                rater1 = rating1.loc[rating1['ID'] == rid, "Rater"].values[0]
                rater2 = rating2.loc[rating2['ID'] == rid, "Rater"].values[0]
                if value1 != value2:
                    print(f'[{rid}] {factor}: {value1} ({rater1}) vs {value2} ({rater2})')
                    print(f'  - {rater1}: {rating1.loc[rating1["ID"] == rid, "Comment"].values[0]}')
                    print(f'  - {rater2}: {rating2.loc[rating2["ID"] == rid, "Comment"].values[0]}')

if __name__ == "__main__":
    # parse the arguments
    parser = argparse.ArgumentParser(description='Define the level of comparison.')
    parser.add_argument(
        '--level', 
        choices=['requirements', 'sentences'], 
        required=True, 
        help='Whether to run the comparison on "requirements" or "sentence" level')
    args = parser.parse_args()

    if args.level == 'requirements':
        rating1 = pd.read_excel(file_name, sheet_name='Requirements')
        rating2 = pd.read_excel(file_name, sheet_name='Requirements Overlap')
        compose_id = lambda row: f'{row["Dataset"]}-{row["File"]}'
        compare(rating1, rating2, factors_requirement, compose_id)
    elif args.level == 'sentences':
        rating1 = pd.read_excel(file_name, sheet_name='Sentence')
        rating2 = pd.read_excel(file_name, sheet_name='Sentence Overlap')
        compose_id = lambda row: f'{row["Dataset"]}-{row["File"]}-{row["Line"]}'
        compare(rating1, rating2, factors_sentence, compose_id)