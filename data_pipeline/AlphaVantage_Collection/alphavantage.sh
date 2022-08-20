#!/bin/bash

# Change to Alphavantage_Collection folder
cd /Users/daniel/Documents/GitHub/Sentiment-Analysis-Stock-Performance/data_pipeline/Alphavantage_Collection

# Activate environment
# eval "$(conda shell.bash hook)"
source /Users/daniel/opt/anaconda3/bin/activate
conda activate carrosell2

# echo $CONDA_DEFAULT_ENV

# Execute python script
python alphavantage.py