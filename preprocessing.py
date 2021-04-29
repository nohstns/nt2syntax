#!/usr/bin/env python3

import os
import pandas as pd
import regex as re
import numpy as np
import stanza
import sys
from string import punctuation

#---------------------------------------------------#
#   Load Stanza model                               #
#---------------------------------------------------#

try:
    nlp = stanza.Pipeline(lang='nl', processors='tokenize, ner')
except:
    stanza.download('nl')
    nlp = stanza.Pipeline(lang='nl', processors='tokenize, ner')

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
    pattern = re.compile(r'(?<=[a-z])(\s)?(\.|\?|\!|\;)*(?<! )((?=[A-Z])|($))')

    def get_punctuation(match):
        return match.group(3) + ' '

    corrected = re.sub(pattern, get_punctuation, text)
    return corrected


def capitalize_sentences(text):
    '''
    Fixes sentence capitalization for sentences where only
    punctuation, with or without a following space, is used
    to delimite sentences, but no upper-case is use to start
    a new sentence..
    '''
    pattern = re.compile(r'(((?<=[a-z])(\.|\?|\!\;) *)([a-z]))')
    pattern2 = re.compile(r'(^[a-z])')
    pattern3 = re.compile(r'(?<=[a-z]\.|\?|\!\;)([a-z])')


    def capitalize(match):
        return match.group(1).upper()

    corrected_text = []

    for line in text.split('\n'):
        corrected_line = re.sub(pattern, capitalize, line.strip())
        corrected_line = re.sub(pattern2, capitalize, corrected_line.strip())
        corrected_line = re.sub(pattern3, capitalize, corrected_line.strip())
        corrected_text.append(corrected_line)

    corrected = '\n'.join(corrected_text)

    return corrected

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


def check_ner(text):
    '''
    Corrects words that are "incorrectly" capitalized.

    i.e. if the capitalized word is not at the beginning of the
    sentence and is not recognized as a named entity, it will
    be replaced by a lowercase version.

    '''

    doc = nlp(text)
    l_doc = text.split(' ')

    pattern = re.compile(r'(?<=[\.|!|?] |^)([A-Z]\w*)')

    def check_start_sentence(tok):
        '''
        Controls that the capitalized word starts a new sentence.
        '''
        sentence_starters = re.findall(pattern, text)
        if tok in sentence_starters:
            return True
        else:
            return False

    def check_end_punct(tok):
        '''
        Controls whether the string in the untokenized text does not include
        punctuation marks that would prevent the match with the tokenized version.
        '''
        if len(tok.strip()) == 0:
            return False
        if tok[-1] in punctuation:
            return True
        else:
            return False

    def check_upper(tok):
        '''
        Checks whether the untokenized version is capitalized.
        '''
        return tok[0].isupper()


    def check_is_ent(token):
        '''
        Checks whether the token is a named entity.
        '''
        if token.ner == 'O':
            return False
        else:
            return True

    parsed = [t for sent in doc.sentences for t in sent.tokens if t.text not in punctuation]


    for i, tok in enumerate(l_doc):
        if check_end_punct(tok):
            w = tok[:-1]
        else:
            w = tok

        for token_i, token in enumerate(parsed):
            # Checking for match between tokenized and untokenized version
            if token.text == w:
                # Checking for match between the position of the tokenized
                # and the untokenized version
                if i == token_i:
                    # Checking whether the token is capitalized, whether it
                    # starts a sentence and whether it's a named entity. If it
                    # is not, the token becomes lowercased.

                    if check_upper(tok) and not check_start_sentence(tok) and not check_is_ent(token):
                            l_doc[i] = tok.lower()
                    break

    corrected = ' '.join(l_doc)
    return corrected


def split_sentences(text):
    '''
    Fixes formatting for parsing with Alpino by splitting sentences in such
    a way that every setence equals to one line. Adds a period to sentences
    missing a final punctuation.
    '''

    doc = nlp(text)
    split_text = ''

    def check_next_lower(i):
        try:
            next_sentence = doc.sentences[i + 1].text

            if next_sentence[0].islower():
                return True
            else:
                return False

        except IndexError:
            return False


    for i, sentence in enumerate(doc.sentences):
        s = sentence.text

        if check_next_lower(i):
            split_text += s + ' '
            continue


        if s[0].islower():
            if check_next_lower(i):
                split_text += s + ' '
            else:
                if s[-1] not in punctuation:
                    split_text += s + '.\n'
                else:
                    split_text += s + '\n'


        elif s[-1] not in punctuation:
            split_text += s + '.\n'

        else:
            split_text += s + '\n'



    return split_text


def apply_preprocessing(dataset):
    '''
    Apply preprocessing functions on the dataset
    '''
    actions = [
               replace_parenthesis,
                sentence_limit_fix,
                capitalize_sentences,
                remove_numbering,
                check_ner,
                split_sentences,
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
            f.write(f'{text}\n\n')

def generate_html_txt(dataset, dataset_label):
    '''
    Generates a *_html.txt file with the preprocessed texts, their corresponding
    code and a html line-break.
    '''

    file_n = 0

    def replace_end_line(text):
        pattern = re.compile(r'(\n)')
        replaced = re.sub(pattern, '<br>', text)
        return replaced


    dataset['TypedText'] = dataset.TypedText.apply(replace_end_line)


    with open(f'dataset{dataset_label}_html.txt', 'w', encoding = 'utf-8') as f:
        for text in dataset['TypedText']:
            part_n = dataset[dataset['TypedText']==text].index.values[0]
            part_n = f'{part_n:03d}'
            file_n_ = f'{file_n:03d}'

            try:
                dataset_n = dataset_label[-1]
            except IndexError:
                dataset_n = '0'

            f.write(f'{dataset_n}{file_n_}{part_n}\t{text}\n')
            file_n += 1

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

USAGE = f"Usage: python {sys.argv[0]} [--help | -h] | [<dataset filename> <dataset label> <html>]"

def main():
    html = False

    if len(sys.argv) == 4:
        if sys.argv[1] in os.listdir():
            script, filename, dataset_label = sys.argv[:-1]
            dataset_label = '_' + dataset_label
            html = True
        else:
            print('Dataset import error')
            raise SystemExit(USAGE)

    if len(sys.argv) == 3:
        if sys.argv[1] in os.listdir():
            if sys.argv[2] == 'html':
                script, filename = sys.argv[:-1]
                dataset_label = ''
                html = True
            else:
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

    if html:
        generate_html_txt(data, dataset_label)


if __name__ == "__main__":
   main()
