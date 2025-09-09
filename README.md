# Requirements Quality for Trace Link Recovery

This repository contains the replication package for the study on how requirements quality affects the performance of automatic trace link recovery tools.
In the scope of this study, we address the question "Which factors of requirements quality impact the performance of automatic traceability like recovery?"
We implement both an observational and an experimental study to answer this research question.

![Overview of the study method](./figures/graphs/rq4tlr-study-overview.png)

## Structure of the Artifact

This repository consists of the following files.

```
├── analysis : directory containing all files for the final data analysis
│   ├── data : directory for data directly for the analysis 
│   │   ├── estimates : directory of outputs produced during the data analysis
│   │   └── rq4tlr.csv : data parsed into a format usable for the final data analysis
│   ├── experimental/experimental-analysis.Rmd : multivariate regression analysis on the experimental data
│   ├── html : directory containing all pre-compiled data analysis notebooks
│   ├── observational : directory containing all regression analysis on the observational data
│   │   ├── observational-analysis-x.Rmd : observational analysis of all variables per outcome
│   │   └── interaction-approach-x.Rmd : interaction analysis between approach and variable x
│   └── util : directory for utility scripts
│       ├── dag.Rmd : specification of the causal assumptions
│       └── data-preparation.Rmd : compilation and casting of final data set
├── data : directory containing all data collected for and produced during the study
│   ├── input : data sets composed from a series of use cases from different domains
│   │   ├── raw : original data as obtained from previous studies (see below)
│   │   └── preprocessed : processed data put into a common json format
│   ├── labeling/rq4tlr-manual-variables.xlsx : labels assigned manually for complex independent variables
│   ├── output/ : labels assigned automatically for simpler independent variables
│   │   ├── rq4tlr-automatic-aggregated.csv : automatically labeled variables aggregated to file-level
│   │   ├── rq4tlr-automatic-sentence.csv : automatically labeled variables on sentence-level
│   │   ├── rq4tlr-automatic-subflow.csv : automatically labeled variables on subflow-level
│   │   ├── rq4tlr-automatic-usecase.csv : automatically labeled variables on usecase-level
│   │   ├── rq4tlr-merged.csv : merged data from automatically and manually labeled variables
│   │   └── variables.json : specification of variable names
│   └── TLR_results/FTLR : results from the FTLR tool performing TLR on the data set
├── figures : directory for all additional documentation
│   ├── distributions : visualization of the distribution of factors in the data
│   ├── graphs/rq4tlr-study-overview.graphml : visualization of the study process
│   └── results/coefficients : visualization of coefficient CIs from posterior distributions
├── src : directory containing all source code
└── requirements.txt : specification of required libraries to run the analysis
```

The src subdirectory contains its own [README.md](./src/README.md) with more detailed descriptions.
The data used in this study stems from the repository [tobhey/**finegrained-traceability**](https://github.com/tobhey/finegrained-traceability). 

## System Requirements

To run the processing steps implemented using Python, consider the [README file in the src directory](./src/README.md) which contains both system requirements and usage instructions.
To run the data analysis scripts implemented in R, ensure that you have [R](https://ftp.acc.umu.se/mirror/CRAN/) (version > 4.0) and an IDE like [RStudio](https://posit.co/download/rstudio-desktop/#download) installed on your machine. 
Then, execute the following steps:

1. Install the C toolchain by following the instructions for [Windows](https://github.com/stan-dev/rstan/wiki/Configuring-C---Toolchain-for-Windows#r40), [Mac OS](https://github.com/stan-dev/rstan/wiki/Configuring-C---Toolchain-for-Mac), or [Linux](https://github.com/stan-dev/rstan/wiki/Configuring-C-Toolchain-for-Linux) respectively.
2. Restart RStudio and follow the instructions starting with the [Installation of RStan](https://github.com/stan-dev/rstan/wiki/RStan-Getting-Started#installation-of-rstan).
3. Install the latest version of `stan` by running the following commands
```
    install.packages("devtools")
    devtools::install_github("stan-dev/cmdstanr")
    cmdstanr::install_cmdstan()
```
4. Install all required packages via `install.packages(c("tidyverse", "xlsx", "ggdag", "brms", "tidyverse", "marginaleffects", "patchwork"))`.
5. Create a folder called *fits* within the *analysis* directory such that `brms` has a location to place all Bayesian models.
6. Open the `rq4tlr.Rproj` file with your IDE, which will setup the environment correctly.

## Usage

To reproduce the study that this replication package accompanies, we recommend the following steps:

1. **Review the causal assumptions**: The file [analysis/util/dag.Rmd](./analysis/util/dag.Rmd) specifies all of our causal assumptions under which we investigate the phenomenon of interest in our study.
2. **Inspect the data**: The [data-preparation.Rmd](./analysis/util/data-preparation.Rmd) loads and assembles our data for analysis.
3. **Follow the observational analyses**: The analyses contained in [analysis/observational/](./analysis/observational/) contain a step-wise description of the Bayesian regression analyses.
4. **Follow the experimental analysis**: The file [experimental-analysis.Rmd](./analysis/experimental/experimental-analysis.Rmd) describes the experimental analysis performed subsequently to the observational analyses.
5. **Assemble the results**: The file [estimate-visualization.Rmd](./analysis/util/estimate-visualization.Rmd) produces the core result of our study, the plot visualizing significant posterior distributions.

For all `.Rmd` files, there is also a precompiled `.html` file in [analysis/html/](./analysis/html/) to ease their access.
When compiling the data analysis notebooks yourself, keep in mind that training Bayesian models may take several minutes.

## License

The code and content of this repository is available under the [MIT License](./LICENSE).
