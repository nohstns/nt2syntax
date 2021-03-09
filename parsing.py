import stanza
stanza.download('nl') # download Dutch model
nlp = stanza.Pipeline('nl') # initialize Dutch neural pipeline


def count_phrase_incidence(doc, phrase_type):
    '''
    Returns a tuple with the instance count and a list with all instances.

    TO BE EDITED.
    Currently POS-based; this should be corrected to be done based on the
    dependency parse tags and not the POS ones (although it can be kept as
    an extra feature I guess?)
    '''
    pos_tags = {'VP':'VERB', 'PP':'ADP'} # Possible to add other types if necessary
    XP = []
    for sent in doc.sentences:
        for word in sent.words:
            if word.upos == pos_tags[phrase_type]:
                XP.append(word.text)
    return XP

def apply_incidence_count(doc):
    '''
    Applies the phrase incidence counter function to a predefined set of
    phrase types.
    Returns a list with tuples:
    [
    (feature name, instance count, list with instances),
    (feature name, instance count, list with instances)
    ]
    ''' # Would be cleaner/more fun to do this with classes, but no time for that right now :p

    features = ['VP', 'PP']
    doc_features = []
    for feat in features:
        cnt = count_phrase_incidence(doc, feat)
        doc_features.append((feat, len(cnt), cnt))

    return doc_features



for file in sorted(os.listdir('./preprocessed')):
    if file.endswith(".txt"):
        with open(f'./preprocessed/{file}', encoding = 'utf-8') as f:
            doc = nlp(f.read())

            # TO DO: Store this information somewhere; as soon as the loop
            # moves to the next file, this data gets lost
            apply_incidence_count(doc)

            #print(*[f'word: {word.text}\tupos: {word.upos}\txpos: {word.xpos}\tfeats: {word.feats if word.feats else "_"}' for sent in doc.sentences for word in sent.words], sep='\n')
            #with open(f'./preprocessed/xml/{file}.txt', 'w', encoding = 'utf-8') as f2:
            #    f2.write(doc)
