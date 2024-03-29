#!/usr/bin/env python3

import os
import sys
import numpy as np
import regex as re
import xml.etree.ElementTree as ET
from apted import APTED
from apted.helpers import Tree
from parsing import tree_to_brackets
from utils import *
from get_tscan import df_doc, df_sen

file = sys.argv[1]
filename = file[:-4]

#---------------------------------------------------#
#   Alpino-generated features                       #
#---------------------------------------------------#

# Alpino-output directory
output_path = f'./alpino_output/{filename}'

# Define number of texts to be analysed based on the Alpino-output
n_texts = len([f for f in os.listdir(output_path) if f.endswith('.txt')])

pattern = re.compile(r'(?<=text_)(\d+)(\.p\.)(\d+)(\.s\.)(\d+)')
def get_metadata(file):
    match = re.split(pattern, file)
    txt_nr = match[1]
    p_n = match[3]
    s_n = match[5]

    return txt_nr, p_n, s_n

#---------------------------------------------------#
#   Feature getter definition.                      #
#                                                   #
#   All functions require the argument `path` to be #
#   a string with the relative path to the text's   #
#   Alpino output folder and the argument `text_n`  #
#   to be the text number unless otherwise stated.  #
#                                                   #
#---------------------------------------------------#

def get_mean_ted(path, level = 'doc'):
    '''
    path = text directory location

    e.g. './output/text_{n}.txt'

    Measures the average TED after comparing every sentence in the text with each other.

    Default is the measure on document level, in which case:

    Returns int -> average TED for entire text.

    If level is set to sentence level `'sen'`:

    Returns list with the distance between each sentence in the text except with themselves.

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

    parses = get_sentences(path)

    for n, xml in enumerate(parses):
        txt_nr, p_n, s_n = get_metadata(xml)

        for compared_n, compared_xml in enumerate(parses):
            if xml == compared_xml:
                continue

            else:
                compared_txt_nr, compared_p_n, compared_s_n = get_metadata(compared_xml)

                pair = f'{p_n}_{s_n}, {compared_p_n}_{compared_s_n}'
                reverse_pair = f'{compared_p_n}_{compared_s_n}, {p_n}_{s_n}'

                if s_n == compared_s_n:
                    continue

                if pair in distances or reverse_pair in distances:
                    continue

                else:
                    with open(f'{path}/{xml}', encoding = 'utf-8') as f:
                        reference_tree = tree_to_brackets(ET.parse(f))

                    with open(f'{path}/{compared_xml}', encoding = 'utf-8') as f2:
                        compared_tree = tree_to_brackets(ET.parse(f2))


                    tr1, tr2 = map(Tree.from_text, (reference_tree, compared_tree))

                    apted = APTED(tr1, tr2)
                    ted = apted.compute_edit_distance()
                    mapping = apted.compute_edit_mapping()


                    distances[pair] = ted

    values = list(distances.values())
    mean_ted = np.mean(values)

    if level == 'doc':
        return mean_ted

    if level == 'sen':
        return values


def get_synstut_adjacent(path, level = 'doc'):
    '''
    Measures sentence-to-sentence similarity.

    Average TED between adjacent sentence pairs in a text.

    Default is the measure on document level, in which case:
    Returns int-> Average TED for entire text.

    If level is set to sentence level `'sen'`:
    Returns list-> distance between each sentence and the next following sentence
    '''

    n_sentences = get_n_sentences(path)

    if n_sentences == 1:
        print('''
        Text is composed of one sentence only or has been parsed as such.
        No TED score will be returned.''')
        syntactic_similarity_score = None
        return syntactic_similarity_score

    distances = {}

    parses = get_sentences(path)

    for n, xml in enumerate(parses):
        txt_nr, p_n, s_n = get_metadata(xml)

        if n + 1 == len(parses):
            break
        else:
            compared_txt_nr, compared_p_n, compared_s_n = get_metadata(parses[n + 1])
            compared_xml = parses[n + 1]


        pair = f'{p_n}_{s_n}, {compared_p_n}_{compared_s_n}'
        reverse_pair = f'{compared_p_n}_{compared_s_n}, {p_n}_{s_n}'

        if s_n == compared_s_n:
            continue

        if pair in distances or reverse_pair in distances:
            continue


        with open(f'{path}/text_{txt_nr}.p.{p_n}.s.{s_n}.xml', encoding = 'utf-8') as f:
            reference_tree = tree_to_brackets(ET.parse(f))

        with open(f'{path}/text_{compared_txt_nr}.p.{compared_p_n}.s.{compared_s_n}.xml', encoding = 'utf-8') as f2:
            compared_tree = tree_to_brackets(ET.parse(f2))


        tr1, tr2 = map(Tree.from_text, (reference_tree, compared_tree))

        apted = APTED(tr1, tr2)
        ted = apted.compute_edit_distance()
        mapping = apted.compute_edit_mapping()


        distances[f'{s_n}, {compared_s_n}'] = ted

    values = list(distances.values())
    mean_ted = np.mean(values)

    if level == 'doc':
        return mean_ted

    if level == 'sen':
        return values

def get_n_words_main_verb(path, level = 'doc'):
    '''
    Counts the number of words before the main verb of the sentence,
    main verb understood as the finite verb, at sentence level.

    Returns a list with the wordcount for each sentence. If multiple counts
    were made (i.e. if there are multiple finite verbs in one sentence or there
    is a conjunction), these are added to the list.
    '''

    total = []

    sentences = get_sentences(path)


    for sentence in sentences:
        with open(f'{path}/{sentence}') as f:
            root = ET.parse(f)

        cnt = 0
        multiple = []
        order = 0
        loop = 0

        full_sentence = root.find('sentence').text.split(' ')

        for word in full_sentence:
            if loop != 0:
                order += 1
            loop += 1

            for element in root.iter('node'):


                if element.get('cat') == 'smain' and (element.get('rel') == 'cnj' or element.get('rel') == 'dp') and int(element.get('begin')) == order:
                    cnt = 0


                if element.get('word') == word and int(element.get('begin')) == order:
                    if element.get('wvorm') == 'pv' and (element.get('lcat') == 'smain' or element.get('lcat') == 'sv1'):
                        multiple.append(cnt)
                    cnt += 1

        for item in  multiple:
            total.append(item)

    mean_number = np.mean(total)

    if level == 'doc':
        return mean_number

    if level == 'sen':
        return total

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
    Total number of syntactic features on text level.

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

def get_phrase_incidence_sentence_level(path):
    '''
    Number of syntactic features on sentence level.

    path = text directory location

    e.g. './output/text_{n}.txt'

    Returns tuple with lists -> ([vp in each sentence], [np in each sentence], [pp in each sentence])
    '''

    sentences = get_sentences(path)

    total_vp = []
    total_np = []
    total_pp = []


    for sentence in (sentences):
        with open(f'{path}/{sentence}') as f:
            root = ET.parse(f)

        synt_feat = get_synt_feat(root)

        total_vp.append(synt_feat[0])
        total_np.append(synt_feat[1])
        total_pp.append(synt_feat[2])

    return(total_vp, total_np, total_pp)



def get_sentence_length(text_n, level = 'doc'):
    '''

    Returns the mean sentence length measured in number of words.

    '''

    if level == 'doc':
        value = df_doc.at[text_n, 'Wrd_per_zin']

    if level == 'sen':
        value = df_sen.at[text_n, 'Wrd_per_zin'].tolist()

    return value


def get_clause_incidence(text_n, level = 'doc'):

    if level == 'doc':
        value = df_doc.at[text_n, 'Pv_Alpino_per_zin']

    if level == 'sen':
        value = df_sen.at[text_n, 'Pv_Alpino_per_zin'].tolist()

    return value



def get_pp_incidence(path, level = 'doc'):

    if level == 'doc':
        return get_total_vp_np_pp(path)[2]

    if level == 'sen':
        return get_phrase_incidence_sentence_level(path)[2]


def get_rel_clauses(text_n, level = 'doc'):

    if level == 'doc':
        value = df_doc.at[text_n, 'Betr_bijzin_per_zin']

    if level == 'sen':
        value = df_sen.at[text_n, 'Betr_bijzin_per_zin'].tolist()

    return value

def get_s_bars(text_n, level = 'doc'):

    if level == 'doc':
        value = df_doc.at[text_n, 'Bijzin_per_zin']

    if level == 'sen':
        value = df_sen.at[text_n, 'Bijzin_per_zin'].tolist()

    return value

def get_infinitive_clause_incidence(text_n, level = 'doc'):

    if level == 'doc':
        value = df_doc.at[text_n, 'Infin_compl_per_zin']

    if level == 'sen':
        value = df_sen.at[text_n, 'Infin_compl_per_zin'].tolist()

    return value

def get_vp_incidence(path, level = 'doc'):

    if level == 'doc':
        return get_total_vp_np_pp(path)[1]

    if level == 'sen':
        return get_phrase_incidence_sentence_level(path)[1]

def get_n_mod_np(text_n, level = 'doc'):

    if level == 'doc':
        value = df_doc.at[text_n, 'Bijv_bep_dz_zbijzin']

    if level == 'sen':
        value = df_sen.at[text_n, 'Bijv_bep_dz_zbijzin'].tolist()

    return value

def get_incidence_negation(text_n, level = 'doc'):

    if level == 'doc':
        value = df_doc.at[text_n, 'Ontk_tot_d']

    if level == 'sen':
        value = df_sen.at[text_n, 'Ontk_tot_d'].tolist()

    return value

def get_n_words(text_n, level = 'doc'):

    if level == 'doc':
        value = df_doc.at[text_n, 'Word_per_doc']

    if level == 'sen':
        value = df_sen.at[text_n, 'Wrd_per_zin'].tolist()

    return value

def get_word_frequency(text_n, level = 'doc'):

    if level == 'doc':
        value = df_doc.at[text_n, 'Freq1000_inhwrd']

    if level == 'sen':
        value = df_sen.at[text_n, 'Freq1000_inhwrd'].tolist()

    return value

# Generate feature/column labels
indices = [
    'sentence_length',
    'n_words',
    'word_frequency',
    'syntactic_similarity',
    'clause_incidence',
    'pp_incidence',
    'rel_clauses',
    's_bars',
    'infinitive_clause_incidence',
    'vp_incidence',
    'n_mod_np',
    'n_words_main_verb',
    'incidence_negation',
    'mean_ted'
    ]

_index_getters = [
    get_sentence_length,
    get_n_words,
    get_word_frequency,
    get_synstut_adjacent,
    get_clause_incidence,
    get_pp_incidence,
    get_rel_clauses,
    get_s_bars,
    get_infinitive_clause_incidence,
    get_vp_incidence,
    get_n_mod_np,
    get_n_words_main_verb,
    get_incidence_negation,
    get_mean_ted
    ]

index_getters = dict(zip(indices, _index_getters))

_print_friendly_indices = [
    'Sentence length',
    'Text length in words',
    'Word frequency',
    'Syntactic similarity',
    'Clause incidence',
    'Prepositional phrase incidence',
    'Relative clauses incidence',
    'S-bar incidence',
    'Infinitive clause incidence',
    'Verb phrase incidence',
    'Number of modifiers per NP',
    'Number of words before the main verb',
    'Negation incidence',
    'Mean Tree Edit Distance'
    ]
print_friendly_indices = dict(zip(indices, _print_friendly_indices))

alpino_feats = [
    'syntactic_similarity',
    'pp_incidence',
    'vp_incidence',
    'mean_ted',
    'n_words_main_verb'
    ]

tscan_feats = [
    'sentence_length',
    'n_words',
    'word_frequency',
    'clause_incidence',
    'rel_clauses',
    's_bars',
    'infinitive_clause_incidence',
    'n_mod_np',
    'incidence_negation'
    ]







def get_index(n, index, level = None):
    '''
    Loops through the text numbers in the dataset and extracts the
    specified index.

    n = text number
    index = desired index/feature
    '''

    if index in alpino_feats:

        path = f'{output_path}/text_{n}.txt'

    if index in tscan_feats:
        path = str(n)

    value = index_getters[index](path, level)
    name = print_friendly_indices[index]

    print(f'{name}:\t{value}')

    return(value)

def apply_index_getter(dataframe, feature, level):
    dataframe[feature] = dataframe.text_n.apply(get_index, index = feature, level = level)
