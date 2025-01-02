# Requirements Quality for Trace Link Recovery

This repository contains the replication package for the study on how requirements quality affects the performance of automatic trace link recovery tools.

## Structure of the Artifact

This repository consists of the following files.

```
├── data : directory containing all data collected for and produced during the study
│   ├── input : data sets composed from a series of use cases from different domains
│   │   ├── raw : original data as obtained from previous studies (see below)
│   │   └── preprocessed : processed data put into a common json format
│   ├── labeling/rq4tlr-manual-variables.xlsx : labels assigned manually for complex independent variables
│   └── output/rq4tlr-automatic-variables.csv : labels assigned automatically for simpler independent variables
├── documentation : directory for all additional documentation
│   └── figures : directory containing figures and graphs
│       └── rq4tlr-study-overview.graphml : visualization of the study process
├── src : directory containing all source code
└── requirements.txt : specification of required libraries to run the analysis
```

The src subdirectory contains its own [README.md](./src/README.md) with more detailed descriptions.
The data used in this study stems from the repository [tobhey/**finegrained-traceability**](https://github.com/tobhey/finegrained-traceability). 

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
