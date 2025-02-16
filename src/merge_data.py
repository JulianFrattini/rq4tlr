import os, json
import pandas as pd

from util.static import PATH_OUTPUT, PATH_LABELING

def load_manual_data() -> pd.DataFrame:
    """Load the manually annotated data from the CSV file."""
    # determine the file name of the manually labeled data set
    data_manual_filename: str = os.path.join(PATH_LABELING, 'rq4tlr-manual-variables.xlsx')

    # load the manually labeled data sets on both the requirements (req) and sentences (sen) level
    dfm_req = pd.read_excel(data_manual_filename, sheet_name='Requirements R2')
    dfm_sen = pd.read_excel(data_manual_filename, sheet_name='Sentences R2')

    # drop the "Comment" column from both data frames
    dfm_req.drop(columns=['Comment', 'Inconsistent Level of Abstraction', 'Contains clarification'], inplace=True)
    dfm_sen.drop(columns=['Comment'], inplace=True)

    # specify the sentence-level variables that need to be aggregated
    manual_sentence_variables: list[str] = [
        "Coordination Ambiguity", 
        "Contains UI Design Details", 
        "Contains Alternative", 
        "Inconsistent Level of Abstraction", 
        "Contains Clarification"]

    # aggregate the rows of dfm_sen per Dataset and File column
    dfm_sen_aggregated = dfm_sen.groupby(['Dataset', 'File'])[manual_sentence_variables].mean()
    # reset the index of the aggregated data frame
    dfm_sen_aggregated = dfm_sen_aggregated.reset_index()

    # join the dfm_req and dfm_sen_aggregated data frames on the Dataset and File columns
    dfm = dfm_req.merge(dfm_sen_aggregated, on=['Dataset', 'File'], how='left')

    # make all strings in the dataset column lowercase
    dfm['Dataset'] = dfm['Dataset'].str.lower()

    return dfm

def load_automatic_data() -> pd.DataFrame:
    # determine the file name of the automatically labeled data set
    data_automatic_filename: str = os.path.join(PATH_OUTPUT, 'rq4tlr-automatic-aggregated.csv')

    # load the data set
    dfa: pd.DataFrame = pd.read_csv(data_automatic_filename)

    # rename the dataset and file columns to match the manual data set
    dfa.rename(columns={'dataset': 'Dataset', 'file': 'File'}, inplace=True)

    return dfa

def determine_nfr_variable(df: pd.DataFrame) -> pd.DataFrame:
    # determine the relevant NFR variable from the two existing ones
    df['Mislocated Functional Requirements'] = df.apply(
        lambda row: row['nfrs'] and not row['Contains NFRs'], 
        axis=1)

    # drop the original NFR variables
    df.drop(columns=['nfrs', 'Contains NFRs'], inplace=True)

def rename_columns(df: pd.DataFrame) -> pd.DataFrame:
    # read the variables.json file in the output folder
    variables_filename: str = os.path.join(PATH_OUTPUT, 'variables.json')
    with open(variables_filename, 'r', encoding='utf-8') as f:
        variables = json.load(f)

        name_to_label = {variable['name']: variable['label'] for variable in variables}
        # replace every column name that corresponds to a key in name_to_label with its corresponding value
        df.rename(columns=name_to_label, inplace=True)

        templabel_to_label = {variable['temp_label']: variable['label'] for variable in variables if 'temp_label' in variable}
        df.rename(columns=templabel_to_label, inplace=True)


if __name__ == "__main__":
    # load the manually annotated data
    dfm: pd.DataFrame = load_manual_data()

    # load the automatically annotated data
    dfa: pd.DataFrame = load_automatic_data()

    # merge the manual and automatic data sets on the Dataset and File columns
    df = dfm.merge(dfa, on=['Dataset', 'File'], how='left')
    # drop all unnecessary columns
    df.drop(columns=['Done', 'Rater', 'UC', 'uc'], inplace=True)

    # finalize the data set by applying the remaining, relevant operations
    determine_nfr_variable(df)

    # rename the columns of the data set
    rename_columns(df)
    
    # save the merged data set
    data_merged_filename: str = os.path.join(PATH_OUTPUT, 'rq4tlr-merged.csv')
    df.to_csv(data_merged_filename, index=False)