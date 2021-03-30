#!/usr/bin/env python3

import os
from apted import APTED
from apted.helpers import Tree
import numpy as np
import xml.etree.ElementTree as ET

#---------------------------------------------------#
#   Alpino-generated features                       #
#---------------------------------------------------#

# Alpino-output directory
output_path = './output'

# Define number of texts to be analysed based on the Alpino-output
n_texts = len([f for f in os.listdir(output_path) if f.endswith('.txt')])

#---------------------------------------------------#
#   Feature getter definition.                      #
#                                                   #
#   All functions require the argument `path` to be #
#   a string with the relative path to the text's   #
#   Alpino output folder unless otherwise stated.   #
#---------------------------------------------------#

def get_mean_ted(path):
    '''
    path = text directory location

    e.g. './output/text_{n}.txt'

    Measures the average TED after comparing every sentence in the text with each other.

    Returns int -> average TED for entire text.

    If the text is only composed of one sentenced or was parsed as such,
    the function returns None for an empty mean TED.
    '''

    n_sentences = get_n_sentences(path)

    if n_sentences == 1:
        print('''
        Text is composed of one sentence only or has been parsed as such.
        No TED score will be returned.
        ''')
        mean_ted = None
        return mean_ted


    distances = {}

    for ref_sentence_n in range(1, n_sentences+1):
        for compared_sentence_n in range(1, n_sentences+1):

            if ref_sentence_n == compared_sentence_n:
                continue

            if f'{ref_sentence_n}, {compared_sentence_n}' in distances:
                continue
            if f'{compared_sentence_n}, {ref_sentence_n}' in distances:
                continue

            else:

                with open(f'{path}/{ref_sentence_n}.xml', encoding = 'utf-8') as f:
                    reference_tree = tree_to_brackets(ET.parse(f))

                with open(f'{path}/{compared_sentence_n}.xml', encoding = 'utf-8') as f2:
                    compared_tree = tree_to_brackets(ET.parse(f2))


                tr1, tr2 = map(Tree.from_text, (reference_tree, compared_tree))

                apted = APTED(tr1, tr2)
                ted = apted.compute_edit_distance()
                mapping = apted.compute_edit_mapping()


                distances[f'{ref_sentence_n}, {compared_sentence_n}'] = ted




    values = list(distances.values())
    mean_ted = np.mean(values)

    return mean_ted

def get_synstut_adjacent(path):
    '''
    Measures sentence-to-sentence similarity.

    Average TED between adjacent sentence pairs in a text.

    Returns int-> Average TED for entire text.
    '''

    n_sentences = get_n_sentences(path)

    if n_sentences == 1:
        print('''
        Text is composed of one sentence only or has been parsed as such.
        No TED score will be returned.''')
        syntactic_similarity_score = None
        return syntactic_similarity_score

    distances = {}

    for ref_sentence_n in range(1, n_sentences):
        with open(f'{path}/{ref_sentence_n}.xml', encoding = 'utf-8') as f:
            reference_tree = tree_to_brackets(ET.parse(f))

        compared_sentence_n = ref_sentence_n + 1

        with open(f'{path}/{compared_sentence_n}.xml', encoding = 'utf-8') as f2:
            compared_tree = tree_to_brackets(ET.parse(f2))


        tr1, tr2 = map(Tree.from_text, (reference_tree, compared_tree))

        apted = APTED(tr1, tr2)
        ted = apted.compute_edit_distance()
        mapping = apted.compute_edit_mapping()


        distances[f'{ref_sentence_n}, {compared_sentence_n}'] = ted

    values = list(distances.values())
    mean_ted = np.mean(values)

    return mean_ted

def get_synt_feat(root:ET.Element):
    '''
    Syntactic features on sentence level.

    Controls the <node lcat> attribute when counting NPs and PPs in the
    entire text and the <node pos> and <node rel> attributes when counting VPs
    and stores the corresponding <node word> attribute in a list.

    Requires root to be an ElementTree Element.

    Returns a tuple with three integers:

    (number of vps, number of nps, number of pps)
    '''
    vp = []
    np = []
    pp = []

    root = root.getroot()

    for element in root.iter('*'):
        if element.tag == 'node':
            lcat = element.get('lcat')
            pos = element.get('pos')
            rel = element.get('rel')
            word = element.get('word')

            if pos == 'verb' and rel == 'hd':
                vp.append(word)

            if lcat == 'np':
                np.append(word)

            if lcat == 'pp':
                pp.append(word)

    return(len(vp), len(np), len(pp))

def get_total_vp_np_pp(path):
    '''
    Number of syntactic features on text level.

    path = text directory location

    e.g. './output/text_{n}.txt'

    Returns tuple -> total vp, total np, total pp for entire text
    '''

    sentences = get_sentences(path)

    total_vp = 0
    total_np = 0
    total_pp = 0


    for sentence in (sentences):
        with open(f'{path}/{sentence}') as f:
            root = ET.parse(f)

        synt_feat = get_synt_feat(root)

        total_vp += synt_feat[0]
        total_np += synt_feat[1]
        total_pp += synt_feat[2]

    return(total_vp, total_np, total_pp)

def get_sentences(path):
    '''
    Takes a directory as argument where the parsing of every sentence
    is stored in a different *.xml file.

    Returns a list of strings with the sentences' file names.
    '''
    sentences = [f for f in os.listdir(path) if f.endswith('.xml')]
    return sentences

def get_n_sentences(text):
    return(len(get_sentences(text)))

def get_sentence_length():
    return None

def get_word_frequency():
    return None

def get_clause_incidence():
    return None

def get_pp_incidence(path):
    return get_total_vp_np_pp(path)[2]

def get_subj_rel_clauses():
    return None

def get_s_bars():
    return None

def get_infinitive_clause_incidence():
    return None

def get_vp_incidence(path):
    return get_total_vp_np_pp(path)[1]

def get_n_mod_np():
    return None

def get_n_words_main_verb():
    return None

def get_incidence_negation():
    return None
