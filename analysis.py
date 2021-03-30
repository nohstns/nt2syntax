#!/usr/bin/env python3

import os
import pandas as pd
from features import *
from indices import *


#---------------------------------------------------#
#   Open T-scan output from different analysis' pov #
#                                                   #
#   df_doc = T-Scan's analysis on document level    #
#   df_sen = T-Scan's analysis on sentence level    #
#                                                   #
#   index_col = 0 ensures that the index is the     # Double-check whether this is a good idea programming-wise :s
#   document reference.                             #
#---------------------------------------------------#

df_doc = pd.read_csv('total.doc.csv', sep = ',', index_col = 0)
df_sen = pd.read_csv('total.sen.csv', sep = ',', index_col = 0)


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
