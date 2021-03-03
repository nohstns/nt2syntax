#!/usr/bin/env python3

import os
import pandas as pd

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

def check_parsing(df):
    if 1 in df.Alpino_status.values:
        print('WARNING: Alpino parsing was unsuccessful for one or more sentences.')
