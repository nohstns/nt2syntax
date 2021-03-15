#!/usr/bin/env python3

import os
import pandas as pd
import regex as re
import xml.etree.ElementTree as ET

#---------------------------------------------------#
#   Open T-scan output from different analysis' pov #
#                                                   #
#   df_doc = T-Scan's analysis on document level    #
#   df_sen = T-Scan's analysis on sentence level    #
#                                                   #
#   index_col = 0 ensures that the index is the     # Double-check whether this is a good idea programming-wise :s
#   document reference.                             #
#---------------------------------------------------#

df_doc = pd.read_csv('total.doc.csv', sep = ',', index_col = 0)
df_sen = pd.read_csv('total.sen.csv', sep = ',', index_col = 0)


#---------------------------------------------------#
#   Open Alpino output from outputfolder xml        #
#   where each text has its own folder with a .xml  #
#   output file, e.g.                               #
#                                                   #
#   xml > text_0.txt > 1.xml                        #
#---------------------------------------------------#

# Extract syntactic features

def get_synt_feat(root):
    '''
    Controls the <node lcat> attribute when counting NPs and PPs in the
    entire text and the <node pos> and <node rel> attributes when counting VPs
    and stores the corresponding <node word> attribute in a list.

    Returns a tuple with three integers:

    (number of vps, number of nps, number of pps)
    '''
    vp = []
    np = []
    pp = []

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



# Define number of texts to be analysed
n = len([f for f in os.listdir('./xml') if f.endswith('.txt')])

# Iterate through the texts to get the number of VPs (nvp), NPs (nnp) and PPs (npp)
for text in range(0, n):
    root = ET.parse(f'./xml/text_{text}.txt/1.xml').getroot()
    nvp, nnp, npp = get_synt_feat(root)
