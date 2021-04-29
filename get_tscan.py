#!/usr/bin/env python3

import os
import sys
import pandas as pd
from utils import get_text_n_from_df
#---------------------------------------------------#
#   Open T-scan output from different analysis' pov #
#                                                   #
#   df_doc = T-Scan's analysis on document level    #
#   df_sen = T-Scan's analysis on sentence level    #
#                                                   #
#---------------------------------------------------#

file = sys.argv[1]
filename = file[:-4]

df_doc = pd.read_csv(f'./tscan_output/{filename}_total.doc.csv', sep = ',')
df_sen = pd.read_csv(f'./tscan_output/{filename}_total.sen.csv', sep = ',')

df_doc['text_n'] = df_doc.Inputfile.apply(get_text_n_from_df)
df_doc = df_doc.set_index('text_n')
df_sen['text_n'] = df_sen.Inputfile.apply(get_text_n_from_df)
df_sen = df_sen.set_index('text_n')
