import os
import pandas as pd


#-------------------------------------------------#
#  	   Feature extraction: pos, dependency        #
#      tag and misspellings - provided they       #
#      exist - for future vectorization           #
#-------------------------------------------------#

data = pd.read_csv('NT2schrijven.csv', sep = ';', index_col = 0)
data = data['typedText']

data.to_csv('dataset_v1.txt', sep = ' ', index = False, header = False)

data.to_csv(r'dataset_v2.csv', sep = ',')

print('DONE')
