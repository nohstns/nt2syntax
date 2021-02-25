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

def sentence_limit_fix(text):
    '''
    Fixes sentence delimitation where the space between
    sentences has been lost, whether a period is used
    or not. Splits
    joined sentences, ends the first one with a
    period if not present and adds a space between
    the sentences.
    '''
    pattern = re.compile(r'(?<=[a-z])(\.|\?|\!)*(?<! )((?=[A-Z])|$)')
    corrected = re.sub(pattern, '. ', text)
    return corrected

def apply_preprocessing():
    '''
    Apply preprocessing functions on the dataset
    '''
    actions = [replace_parenthesis, sentence_limit_fix]

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

def split_text_files():
    '''
    Generates an individual *.txt file for every preprocessed
    text for analysis with T-scan.
    '''
    try:
        os.mkdir('preprocessed')
    except FileExistsError:
        pass

    cnt = 0
    for text in data['TypedText']:
        with open(f'preprocessed/text_{cnt}.txt', 'w', encoding = 'utf-8') as f:
            f.write(text)
        cnt += 1

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
    split_text_files()
main()
