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
    Extracts the values of the <node lcat> attribute for the entire text
    and stores them in a list.
    This node corresponds to the syntactic feature of each phrase.
    '''
    vp = []
    np = []
    pp = []
    all_p = [] # Variable for testing purposes

    for element in root.iter('*'):
        if element.tag == 'node':
            xp = element.get('lcat')
            if xp != None:
                all_p.append(xp)
            if xp == 'vp':
                vp.append(xp)
            if xp == 'np':
                np.append(xp)
            if xp == 'pp':
                pp.append(xp)

    return(all_p, len(vp), len(np), len(pp))


# Define number of texts to be analysed
n = len([f for f in os.listdir('./xml') if f.endswith('.txt')])

for text in range(0, n):
    root = ET.parse(f'./xml/text_{text}.txt/1.xml').getroot()
    print(text, '\t', get_synt_feat_(root))
    print('\n\n\n')
