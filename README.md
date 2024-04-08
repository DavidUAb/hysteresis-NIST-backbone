# hysteresis-NIST-backbone

This collection of python scripts seeks to compare and determine the magnitude of error between two hysteresis backbones. This process is done in 3 steps.

The first step is the determination of a backbone derived from a hysteresis curve generated using OpenSees for a material Steel01. In this step, first a strain history for the material was defined and applied to the material to generate a hysteresis curve. Then a python library named "Hysteresis" was used to analyze this curve and the data points comprising this curves' backbone.

The second step was the generation of a backbone according to the parameters and equations defined by the reference text NIST GCR 17-917-45, Table ES1, for wide flange steel beams. The python script titled get_params was used to generate the function acording to the reference text, this function serves as the second backbone for comparison. 

The third step was the comparison of the two generated backbones. The python script titled compare_backbones used the csv files containing the data points of each backbone, and using the Mean Absolute Error method the difference between the backbone generated from the OpenSees hysteresis curve and the reference backbone defined by general functions is found. In this analysis, two paramters having an effect on the shape of the reference backbone, those parameters being the cross-sectional area and theta ultimate (as identified in the reference text), were iterated over a range of values in grid search style. In this grid search, the MAE (mean absolute error) was computed for each set of values used in the grid search. The result of the analysis is the minimum computed MAE, and corresponding values of the iterated parameters. 

## Execution Instructions

Cd into `src` using the command: `cd src`

Run the file `get_hysteresis_data.py` using python.

Then run the file `get_params.py` using python.

Finally run the file `compare_backbone.py` using python.