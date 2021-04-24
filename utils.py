#!/usr/bin/env python3

import os
import regex as re

#---------------------------------------------------#
#   Utils                                           #
#---------------------------------------------------#

def get_sentences(path):
    '''
    Takes a directory as argument where the parsing of every sentence
    is stored in a different *.xml file.

    Returns a list of strings with the sentences' file names.
    '''
    sentences = sorted([f for f in os.listdir(path) if f.endswith('.xml')])
    return sentences

def get_n_sentences(text):
    return(len(get_sentences(text)))


def get_text_n_from_df(name):
    pattern = r'(?<=input\/text_)[0-9]+(?=\.txt)'
    n = re.search(pattern, name).group(0)
    return(n)
