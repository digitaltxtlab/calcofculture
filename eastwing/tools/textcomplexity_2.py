#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
data experiment testing measures of text complexity
- readability and entropy for single text
- data: Moby Dick and Peter Panl
"""
import glob, io, math, os, re
from textstat.textstat import textstat as ts
from __future__ import division
import nltk.data

import kvikplot as kvk

### text processing
def read_txt(filepath):
    """
    import text file on filepath
    """
    f = io.open(filepath, "r", encoding = "utf-8")
    content = f.read()
    f.close()
    return content

def read_txts(dirpath, format = '.txt'):
    """
    read multiple vanilla files of specific format from directory
    """
    filenames = glob.glob(dirpath+"/*"+format)
    output = []
    for f in filenames:
        output.append(read_txt(f))
    return output

def tokenize(input, length = 0, casefold = False, sent_lvl = False):
    """
    tokenize w. case folding at unigram or sentence level
    - at unigram levels remove unigrams of len(unigram) == length
    """
    if casefold:
        input = input.lower()
    if sent_lvl:
        tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
        return tokenizer.tokenize(input)
        sd
    else:
        tokenizer = re.compile('\W*')
        return [unigram for unigram in tokenizer.split(input) if len(unigram) > length]

def slice_string(s, slc = 1000, cut_off = True):
    """
    slice string in slc slices
    """
    N = len(s)
    if slc > N:
        "string insufficient length"
        return s
    else:
        n = slc + 1
        slc_len = int(math.ceil(N/n))
        output = []
        for i in range(0,N,slc_len):
            output.append(s[i:(i+slc_len)])
        if cut_off & len(output[-1]) != slc_len:
            del output[-1]
        return output

def slice_tokens(tokens, n = 100, cut_off = True):
    """
    slice tokenized text in slices of n tokens
    - end cut off for full length normalization
    """
    slices = []
    for i in range(0,len(tokens),n):
        slices.append(tokens[i:(i+n)])
    if cut_off:
        del slices[-1]
    return slices

### entropy measures

def renyi_entropy(input, alpha = 2, logbase = 2):
    """
    Renyi entropy for quantifying text diversity/uncertainty/randomness
    - for char and ngram levels
    - alpha = 1 is special case, returns Shannon Entropy
    - not defined for alpha <= 0
    """
    px = [float(input.count(c))/len(input) for c in dict.fromkeys(list(input))]
    if alpha <= 0:
        print 'not defined for alpha <= 0'
        return None
    elif alpha == 1:
        return - sum([x*math.log(x,logbase) for x in px])
    else:
        px = [x**alpha for x in px]
        return 1/(1-alpha)* math.log(sum(px),logbase)

def shannon_ideal(input, logbase = 2):
    p = 1.0/len(input)
    return -1.0 * len(input) * p * math.log(p, logbase)

### readability
def lix(s):
    """
    LIX from string s
    läsbarhetsindex (Björnsson, C. H. (1968). Läsbarhet. Stockholm: Liber.)
    sum of number of words pr. full stop length and fraction of long words
    key:
    >55 very hard, academic literature
    45-54 hard, e.g., non-fiction, popular science
    35-44 middle, e.g. newspaper articles
    25-34 easy for trained readers, e.g., tabloid articles
    <24 easy for all readers, e.g. childrens literature
    """
    unigrams = tokenize(s, casefold = True)
    o = len(unigrams)
    p = len(re.findall(r'\.',s))
    if p == 0:
        p = 1
    l = len([w for w in unigrams if len(w) > 6])
    return o/p + l*100/o

# pipeline
def complex_str_pipeline(s):
    sh_ent = renyi_entropy(s, alpha = 1)# shannon
    col_ent = renyi_entropy(s, alpha = 2)# collision
    sh_delta = shannon_ideal(s, logbase = 2) - sh_ent# distance to ideal encoding
    f_ease = ts.flesch_reading_ease(s)# Flesch reading ease
    fk_grade = ts.flesch_kincaid_grade(s)# Flesch–Kincaid grade level
    lix_scr = lix(s)
    #return {'Shannon': sh_ent,'Collision': col_ent, 'Delta': sh_delta,
    #'Flesch_ease': f_ease, 'Flesch_Kincaid': fk_grade, 'LIX': lix_scr}
    return [sh_ent, col_ent, sh_delta, f_ease, fk_grade, lix_scr]

def loop_pipeline(l):
    output = []
    for s in l:
        output.append(complex_str_pipeline(s))
    return output


### data
datapath = os.path.expanduser('~/Documents/proj/text_complex')
# literary texts
texts = read_txts(datapath)
# sentences
s1 = 'This sentence, taken as a reading passage unto itself, is being used to prove a point.'
s2 = 'The Australian platypus is seemingly a hybrid of a mammal and reptilian creature.'


unigrams = [tokenize(text, length = 0, casefold = True, sent_lvl = False) for text in texts]
sents =  [tokenize(text, length = 0, casefold = False, sent_lvl = True) for text in texts]


### main

# sent level
res = loop_pipeline(sents[0])

shannon = [l[0] for l in res]
collision = [l[1] for l in res]
delta_shannon = [l[2] for l in res]
flesh = [l[3] for l in res]
flesh_kincaid = [l[4] for l in res]
lix_scr = [l[5] for l in res]

kvk.plotdist(shannon)
kvk.plotdist(collision)

kvk.plotdist(flesh)

kvk.plotdist(lix_scr)
kvk.plotdist(flesh_kincaid)
kvk.qd_plot(shannon,delta_shannon)

# slice in equal length



#### ALPHA
