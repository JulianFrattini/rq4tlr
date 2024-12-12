# Requirements Quality for Trace Link Recovery

This repository contains the replication package for the study on how requirements quality affects the performance of automatic trace link recovery tools.

## Structure of the Artifact

This repository consists of the following artifacts.

```
├── analysisautomatic/ : directory containing all data and source code for the automatic analysis
│   ├── data/ : input for and output of the analysis
│   │   ├── input/ : raw input data in the form of directories of use cases in text files
│   │   └── output/rq4tlr-automatic-variables.csv : automatic rating of variables 
│   ├── src/ : directory containing all source files, including the `main.py` which serves as the starting point
│   ├── README.md : separate readme file explaining how to understand, use, and extend the analysis
│   └── requirements.txt : specification of required libraries to run the analysis
├── analysismanual/ : directory containing all data and soure code produced during the manual analysis of the study
│    ├── data/rq4tlr-manual-variablex.xslx : Excel workbook containing the manual ratings of variable values
│    └── src/ : source code to process the manually generated data
│        ├── disagreements.py : utility script to detect all existing disagreements between two ratings
│        ├── ira.py : utility file implementing the calculation of percentage agreement and Bennett's S-score
│        ├── overlap-requirements.ipynb : inter-rater agreement calculation on the requirements-level
│        └── overlap-sentences.ipynb : inter-rater agreement calculation on the sentence-level
└── documentation/ : directory for all additional documentation
    └── figures/ : directory containing figures and graphs
        └── rq4tlr-study-overview.graphml : visualization of the study process
```    

The data used in this study stems from the repository [tobhey/**finegrained-traceability**](https://github.com/tobhey/finegrained-traceability). The data can be found in the *datasets* directory.

## System Requirements

The code in this repository uses Python 3.10.0. 
To execute the code locally, perform the following steps:

1. Ensure that [Python 3.10](https://www.python.org/downloads/release/python-3100/) is installed on your machine.
2. Install the [requirements](./requirements.txt) by executing `pip install -r requirements.txt`.

Then, you can run the Jupyter notebooks locally.

## Usage

To check the calculation of the inter-rater agreement, run the [overlap-requirements.ipynb](./analysismanual/src/overlap-requirements.ipynb) and the [overlap-sentences.ipynb](./analysismanual/src/overlap-sentences.ipynb) notebooks.

To determine disagreements between two manual ratings, use the [disagreements.py](./analysismanual/src/disagreements.py) script.
Ensure that `pandas` is installed and run (replace "sentences" with "requirements" for the requirements-level disagreements):

```
python disagreements.py --type sentences
```

## License

The code and content of this repository is available under the [MIT License](./LICENSE).
