#!/usr/bin/env python3

import os
import pandas as pd
import regex as re
import numpy as np
import stanza
import sys

#---------------------------------------------------#
#   Load Stanza model                               #
#---------------------------------------------------#

try:
    nlp = stanza.Pipeline(lang='nl', processors='tokenize')
except:
    stanza.download('nl')
    nlp = stanza.Pipeline(lang='nl', processors='tokenize')

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
    Fixes sentence delimitation where the space between sentences has been lost.
    Adds a space between the sentences.

    Requires properly capitalized sentences.
    '''
    pattern = re.compile(r'(?<=[a-z])(\s)?(\.|\?|\!|\;)*(?<! )((?=[A-Z])|$)')

    def get_punctuation(match):
        return match.group(3) + ' '

    corrected = re.sub(pattern, get_punctuation, text)
    return corrected

def end_sentence_with_period(text):
    '''
    Adds a period at the end of a sentence with no punctuation.
    '''

    pattern = re.compile(r'(?<=\w$)')

    corrected_text = []

    for line in text.split('\n'):
        corrected_line = re.sub(pattern, '.', line)
        corrected_text.append(corrected_line)

    corrected = '\n'.join(corrected_text)
    return corrected

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

    corrected_text = []

    for line in text.split('\n'):
        corrected_line = re.sub(pattern, capitalize, line)
        corrected_text.append(corrected_line)

    corrected = '\n'.join(corrected_text)

    return sentence_limit_fix(corrected)

def remove_numbering(text):
    '''
    Removes the sentence numbers added by the author to count the amount
    of sentences written.
    '''
    pattern = re.compile(r'^\d[\.|\-]\s?')

    corrected_text = []
    for line in text.split('\n'):
        corrected_line = re.sub(pattern, '', line)
        corrected_text.append(corrected_line)

    corrected = '\n'.join(corrected_text)
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

def apply_preprocessing(dataset):
    '''
    Apply preprocessing functions on the dataset
    '''
    actions = [
                replace_parenthesis,
                sentence_limit_fix,
                capitalize_sentences,
                split_sentences,
                remove_numbering,
                end_sentence_with_period
                ]

    for action in actions:
        dataset['TypedText'] = dataset.TypedText.apply(action)


#---------------------------------------------------#
#   File generation                                 #
#---------------------------------------------------#


def generate_txt(dataset, dataset_label):
    '''
    Generates a *.txt file with the texts preprocessed
    for analysis with T-scan.
    '''
    with open(f'dataset{dataset_label}.txt', 'w', encoding = 'utf-8') as f:
        for text in dataset['TypedText']:
            f.write(f'{text}\n')

def split_text_files(dataset, dataset_label):
    '''
    Generates an individual *.txt file for every preprocessed
    text for analysis with T-scan.
    '''
    try:
        os.mkdir(f'preprocessed{dataset_label}')
    except FileExistsError:
        pass

    cnt = 0
    for text in dataset['TypedText']:
        with open(f'preprocessed{dataset_label}/text_{cnt}.txt', 'w', encoding = 'utf-8') as f:
            f.write(text)
        cnt += 1

def generate_csv(dataset, dataset_label):
    '''
    Generates a *.csv file with the texts preprocessed
    for analysis with T-scan, their corresponding evaluation
    and the participants' ID.
    '''
    dataset.to_csv(f'dataset{dataset_label}.csv', sep = ',')


#---------------------------------------------------#
#   main() definition                               #
#---------------------------------------------------#

USAGE = f"Usage: python {sys.argv[0]} [--help | -h] | [<dataset filename> <dataset label>]"

def main():
    if len(sys.argv) == 3:
        if sys.argv[1] in os.listdir():
            script, filename, dataset_label = sys.argv
            dataset_label = '_' + dataset_label
        else:
            print('Dataset import error')
            raise SystemExit(USAGE)

    elif len(sys.argv) == 2:
        script = sys.argv[0]

        if sys.argv[1] == '--help' or sys.argv[1] == '-h':
            print(f'''
            {USAGE}

            Make sure that the dataset is stored in a *.csv file, separated by `;`.
            It should contain a column  `'typedText'` where the to preprocess
            text is stored and a column `'participantnummer'` with the author's
            id number.

            An optional second argument can be used to keep multiple outputs separated.
            Not specifying a label can lead to overwriting files.

            e.g. python {script} dataset.csv v1
            ''')
            sys.exit()

        if sys.argv[1] in os.listdir():
            filename = sys.argv[1]
            dataset_label = ''
        else:
            print('Dataset import error')
            raise SystemExit(USAGE)

    #---------------------------------------------------#
    #   Open raw dataset and extract typedText only;    #
    #   preprocess the texts according to T-scan's      #
    #   formatting requirements.                        #
    #---------------------------------------------------#

    data = pd.read_csv(filename, sep = ';', index_col = 0)
    data = data['typedText'].to_frame(name = 'TypedText')
    data['Evaluation'] = np.nan

    apply_preprocessing(data)
    generate_csv(data, dataset_label)
    generate_txt(data, dataset_label)
    split_text_files(data, dataset_label)

if __name__ == "__main__":
   main()
