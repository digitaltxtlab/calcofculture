#!/usr/bin/env python2
# -*- coding: utf-8 -*-
'''
calculates mean and standard deviation of word level entropy (log base 2) for a tokenized document in chunks of n tokens

mona@wintermute:~$ python word2entropy.py nattergalen.txt 500
'''

__author__      = "KLN"

import sys, io, re
from unidecode import unidecode
from collections import defaultdict
import numpy as np

def main():
    filename = sys.argv[1]
    n = int(sys.argv[2])
    doc = cleanimport(filename)
    chunks = chunkize(doc,n)
    ent = chunks2ent(chunks)
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

def chunkize(t,n):
    '''chunkize document t in chunks of n tokens'''
    idx = range(0,len(t)+1,n)
    res = []
    for i in idx:
        if i == idx[len(idx)]:
            res.append(t[i:-1])
        else:
            res.append(t[i:i+n])
    return res

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

def chunks2ent(chunks):
    ''' mean and sd entropy for chunks'''
    vec = []
    for l in chunks:
        vec.append(doc2ent(l))
    M = np.mean(np.array(vec))
    SD = np.std(np.array(vec))
    return M, SD


if __name__ == '__main__':
    main()
