#!/usr/bin/env python3

import os
import pandas as pd
import regex as re
import numpy as np
import stanza

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
try:
    nlp = stanza.Pipeline(lang='nl', processors='tokenize')
except:
    stanza.download('nl')
    nlp = stanza.Pipeline(lang='nl', processors='tokenize')

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


# TO FIX: The regex recognises all punctuation recognised by T-scan as
#         a sentence delimiter, but the function replaces them all with periods.

def sentence_limit_fix(text):
    '''
    Fixes sentence delimitation where the space between
    sentences has been lost, whether a period is used
    or not. Splits joined sentences, ends the first one with a
    period if not present and adds a space between
    the sentences.

    Requires properly capitalized sentences.

    /!\ This function replaces all sentence-end punctuations with a period!

    '''
    pattern = re.compile(r'(?<=[a-z])(\s)?(\.|\?|\!|\;)*(?<! )((?=[A-Z])|$)')
    corrected = re.sub(pattern, '. ', text)
    return corrected.strip(' ') # Dirty solution for the space at the end of the sentence


def capitalize_sentences(text):
    '''
    Fixes sentence capitalization for sentences where only
    punctuation, with or without a following space, is used
    to delimite sentences, but no upper-case is use to start
    a new sentence. Applies sentence_limit_fix().
    '''
    pattern = re.compile(r'(((?<=[a-z])(\.|\?|\!\;)( )*|^)([a-z]))')

    def capitalize(match):
        return match.group(5).upper()

    corrected = sentence_limit_fix(re.sub(pattern, capitalize, text))
    return corrected

def split_sentences(text):
    '''
    Fixes formatting for parsing with Alpino by splitting sentences in such
    a way that every setence equals to one line.
    '''
    doc = nlp(text)
    split_text = ''

    for i, sentence in enumerate(doc.sentences):
        split_text += sentence.text + '\n'
    return split_text

def apply_preprocessing():
    '''
    Apply preprocessing functions on the dataset
    '''
    actions = [replace_parenthesis, capitalize_sentences, sentence_limit_fix, split_sentences]

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
    generate_txt()
    split_text_files()

main()
