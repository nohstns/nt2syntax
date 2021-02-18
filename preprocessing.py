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


#---------------------------------------------------#
#   Preprocessing functions definition to fit       #
#   T-scan's formatting requirements.               #
#---------------------------------------------------#

def replace_parenthesis(text):
    '''
    Replaces all squared brackets with round brackets.
    '''
    for char in text:
        if char == '[':
            text = text.replace('[', '(')
        if char ==']':
            text = text.replace(']', ')')
    return text

def spellcheck(): # Function for tool testing purposes; not analysis
    '''
    Corrects spelling mistakes in the texts.
    '''
    pass




def apply_preprocessing():
    '''
    Apply preprocessing functions on the dataset
    '''
    actions = [replace_parenthesis]

    for action in actions:
        data['TypedText'] = data.TypedText.apply(action)


#---------------------------------------------------#
#   File generation                                 #
#---------------------------------------------------#


def generate_txt():
    '''
    Generates a *.txt file with the texts preprocessed
    for analysis with T-scan.
    '''
    with open('dataset.txt', 'w', encoding = 'utf-8') as f:
        for text in data['TypedText']:
            f.write(f'{text}\n')

def generate_csv():
    '''
    Generates a *.csv file with the texts preprocessed
    for analysis with T-scan, their corresponding evaluation
    and the participants' ID.
    '''
    data.to_csv(r'dataset_v2.csv', sep = ',')


#---------------------------------------------------#
#   main() definition                               #
#---------------------------------------------------#

def main():
    apply_preprocessing()
    generate_txt()

main()
