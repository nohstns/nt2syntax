#!/usr/bin/env python3

import os
import pandas as pd
from features import *

#---------------------------------------------------#
#   Open dataset and generate dataframe to store    #
#   the extracted features.                         #
#---------------------------------------------------#

df = pd.read_csv('dataset.csv', sep = ',')

# Add column with the text number for its use in the feature extraction functions

df['text_n'] = df.index

# Add feature columns and fill them with empty values
for index in indices:
    df[index] = np.nan


for index in indices:
    apply_index_getter(df, index)

    
df.to_csv(r'dataset_features.csv', sep = ',')
