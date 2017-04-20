#!/usr/bin/env python2
# -*- coding: utf-8 -*-

''' calculates word level entropy base 2 for tokenized documents'''

__author__      = "K.L. Nielbo"

import sys, io, re
from unidecode import unidecode
from collections import defaultdict
import numpy as np

def main():
    filename = sys.argv[1]
    doc = cleanimport(filename)
    ent = doc2ent(doc)
    #return ent
    print ent

def cleanimport(filename):
    '''import unicode plain text, remove punctuation and numerals, casefold and tokenize'''
    f = io.open(filename,'r',encoding = 'utf-8')
    content = f.read()
    f.close()
    content = unidecode(content)
    content = re.sub(r'\W+', ' ',content)
    content = re.sub(r'\d','',content)
    content = content.lower()
    token = content.split()
    return token

def doc2ent(doc):
    ''' estimates word level entropy for tokenized document'''
    bow = defaultdict(int)
    for token in doc:
        bow[token] += 1
    p_w = np.array(bow.values())
    n = np.sum(p_w)
    tmp = []
    for p in p_w:
        rp = p/float(n)# relative probability
        tmp.append(rp*np.log2(rp))
    return -np.sum(np.array(tmp))

if __name__ == '__main__':
    main()
