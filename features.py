#!/usr/bin/env python3

import os
import numpy as np
import regex as re
import xml.etree.ElementTree as ET
from apted import APTED
from apted.helpers import Tree
from parsing import tree_to_brackets
from utils import *
from get_tscan import df_doc, df_sen

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
#   Alpino output folder and the argument `text_n`  #
#   to be the text number unless otherwise stated.  #
#                                                   #
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
    
    node_count = 0

    root = root.getroot()

    for element in root.iter('*'):
        if element.tag == 'node':
            lcat = element.get('lcat')
            pos = element.get('pos')
            rel = element.get('rel')
            word = element.get('word')
            
            if lcat:
                node_count += 1

            if pos == 'verb' and rel == 'hd':
                vp.append(word)

            if lcat == 'np':
                np.append(word)

            if lcat == 'pp':
                pp.append(word)

    return(len(vp), len(np), len(pp), node_count)

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
    total_nodes = 0


    for sentence in (sentences):
        with open(f'{path}/{sentence}') as f:
            root = ET.parse(f)

        synt_feat = get_synt_feat(root)

        total_vp += synt_feat[0]
        total_np += synt_feat[1]
        total_pp += synt_feat[2]
        total_nodes += synt_feat[3]

    return(total_vp/total_nodes, total_np/total_nodes, total_pp/total_nodes)


def get_sentence_length(text_n):
    '''
    Proxy text-level feature.
    
    Takes 
    
    Returns the mean sentence length measured in number of words.

    '''
    
    value = df_doc.at[text_n, 'Wrd_per_zin']
    
    return value

def get_word_frequency():
    return None

def get_clause_incidence(text_n):
    
    value = df_doc.at[text_n, 'Pv_Alpino_per_zin']

    return value

def get_pp_incidence(path):
    return get_total_vp_np_pp(path)[2]

def get_subj_rel_clauses(text_n):
    value = df_doc.at[text_n, 'Bijzin_per_zin']
    return value

def get_s_bars(text_n):
    value = df_doc.at[text_n, 'Bijzin_per_zin']
    return value

def get_infinitive_clause_incidence(text_n):
    value = df_doc.at[text_n, 'Infin_compl_per_zin']
    return value

def get_vp_incidence(path):
    return get_total_vp_np_pp(path)[1]

def get_n_mod_np(text_n):
    value = df_doc.at[text_n, 'AL_lidw_znw']
    return value

def get_n_words_main_verb():
    return None

def get_incidence_negation(text_n):
    value = df_doc.at[text_n, 'Ontk_tot_d']
    return value




# Generate feature/column labels
indices = [
    'sentence_length',
#    'word_frequency',
    'syntactic_similarity',
    'clause_incidence',
    'pp_incidence',
    'subj_rel_clauses',
    's_bars',
    'infinitive_clause_incidence',
    'vp_incidence',
    'n_mod_np',
#    'n_words_main_verb',
    'incidence_negation',
    'mean_ted'
    ]

_index_getters = [
    get_sentence_length,
#    get_word_frequency,
    get_synstut_adjacent,
    get_clause_incidence,
    get_pp_incidence,
    get_subj_rel_clauses,
    get_s_bars,
    get_infinitive_clause_incidence,
    get_vp_incidence,
    get_n_mod_np,
#    get_n_words_main_verb,
    get_incidence_negation,
    get_mean_ted
    ]

index_getters = dict(zip(indices, _index_getters))

_print_friendly_indices = [
    'Sentence length',
#    'Word frequency',
    'Syntactic similarity',
    'Clause incidence',
    'Prepositional phrase incidence',
    'Subject relative clauses incidence',
    'S-bar incidence',
    'Infinitive clause incidence',
    'Verb phrase incidence',
    'Number of modifiers per NP',
#    'Number of words before the main verb',
    'Negation incidence',
    'Mean Tree Edit Distance'
    ]
print_friendly_indices = dict(zip(indices, _print_friendly_indices))

alpino_feats = [
    'syntactic_similarity',
    'pp_incidence',
    'vp_incidence',
    'mean_ted'
    ]

tscan_feats = [
    'sentence_length',
    'word_frequency',
    'clause_incidence',
    'subj_rel_clauses',
    's_bars',
    'infinitive_clause_incidence',
    'n_mod_np',
    'n_words_main_verb',
    'incidence_negation'
    ]







def get_index(n, index):
    '''
    Loops through the text numbers in the dataset and extracts the
    specified index.

    n = text number
    index = desired index/feature
    '''
    
    if index in alpino_feats:
    
        path = f'./output/text_{n}.txt'
        
    if index in tscan_feats:
        path = str(n)
        
    value = index_getters[index](path)
    name = print_friendly_indices[index]

    print(f'{name}:\t{value}')

    return(value)

def apply_index_getter(dataframe, feature):
    dataframe[feature] = dataframe.text_n.apply(get_index, index = feature)