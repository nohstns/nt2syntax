#!/usr/bin/env python3

import os
import pandas as pd
import regex as re
import numpy as np

#---------------------------------------------------#
#   Open raw dataset and extract typedText only;    #
#   preprocess the texts according to T-scan's      #
#   formatting requirements.                        #
#---------------------------------------------------#

data = pd.read_csv('NT2schrijven.csv', sep = ';', index_col = 0)
data = data['typedText'].to_frame(name = 'TypedText')
data['Evaluation'] = np.nan

def replace_parenthesis(text):
    for char in text:
        if char == '[':
            text = text.replace('[', '(')
        if char ==']':
            text = text.replace(']', ')')
    return text

# Generate new version of the text without spelling errors
def spellcheck():
    pass


# Apply preprocessing functions on the dataset
actions = [replace_parenthesis]

for action in actions:
    data['TypedText'] = data.TypedText.apply(action)

print(data.head(10))

#---------------------------------------------------#
#   Generate two files with the preprocessed data;  #
#   a *.txt for use with T-scan and a *.csv         #
#   containing the participant ID linked to the     #
#   actual text. Line order between the two files   #
#   is the same.                                    #
#---------------------------------------------------#

#data['TypedText'].to_csv('dataset_v1.txt', sep = ' ', index = False, header = False)

# Write *.txt
with open('dataset.txt', 'w', encoding = 'utf-8') as f:
    for text in data['TypedText']:
        f.write(f'{text}\n')


#data.to_csv(r'dataset_v2.csv', sep = ',')

print('DONE')
