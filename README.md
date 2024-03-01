# Which is better

This program was designed to compare files for the SEE-Insight Group.  It uses a simple GUI to compare files in a folder.


## Install instructions

This analysis requires the statsmodels python library. Install using the following command:

```pip install statsmodels```

## Files

The file 'EloAnalysis.py' is the code for generating Elo scores and the Elo distance matrices.

The file 'Correlation.py' is the code for generating the corresponding distance matrices for the fitness functions and performing a linear regression between those and the Elo distances.

The file 'ExperimentGUI.py' is the GUI for the Which Is Better Experiment, in which participants are shown pairs of ground truths and prompted to select the one closer to the original image. Matrices reflecting the choices are saved as CSV files when run.

The notebook 'Analysis.ipynb' takes the data from the experiment and analyzes it by performing a linear regression with data from the fitness functions. The Elo distance matrices and the fitness function distance matrices will be saved into the chosen image's designated folder in the 'images' directory as they are generated.



