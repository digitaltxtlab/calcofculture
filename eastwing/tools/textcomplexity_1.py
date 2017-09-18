
#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""
data experiment testing measures of text complexity
"""
__author__  = 'KLN'

import os, io, re, glob, math
from unidecode import unidecode
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib as mpl

def dirimport(filepath):
    """ import multiple unicode plain text from directory, remove punctuation and numerals, casefold and tokenize """
    res = []
    files = glob.glob(filepath+'*.txt')
    for filename in files:
        f = io.open(filename,'r',encoding = 'utf-8')
        content = f.read()
        f.close()
        content = unidecode(content)
        content = re.sub(r'\W+', ' ',content)
        content = re.sub(r'\d','',content)
        content = content.lower()
        token = content.split()
        res.append(token)
    return res

def dirchunk(doc_list, n = 100):
    """ chunk list of tokenized documents from dirimport """
    res = []
    for doc in doc_list:
        idx = range(0, len(doc)+1, n)
        chunks = []
        for i in idx:
            if i == idx[len(idx)-1]:
                if not doc[i:-1]:
                    continue
                else:
                    chunks.append(doc[i:-1])
            else:
                if not doc[i:i+n]:
                    continue
                else:
                    chunks.append(doc[i:i+n])
        res.append(chunks)
    return res

#def ttr_list(doc_list):
#    """ type-token ratio for chunked tokenized documents in list """
#    res = []
#    for d in doc_list:
#        tmp = []
#        for c in d:
#            num = len(set(c))
#            den = len(c)
#            tmp.append(num/float(den))
#        ttr = sum(tmp)/float(len(tmp))
#        res.append(ttr)
#    return res

def doc2ttr(doc):
    """ type token ratio for tokenized document """
    num = len(set(doc))
    den = len(doc)
    return num/float(den)

def doc2ttrnorm(doc):# length normalized TTR from (Carroll 1964 in Hess 1984)
    num = len(set(doc))
    denom = np.sqrt(2*len(doc))
    return res

def ttr_list(doc_list):
    """ estimates type-token ratio for list of chunked tokenized documents """
    res = []
    for d in doc_list:
        tmp = []
        for c in d:
            tmp.append(doc2ttr(c))
        res.append(sum(tmp)/float(len(tmp)))
    return res

#def doc2ent(doc):
#    ''' estimates word level entropy for tokenized document'''
#    bow = defaultdict(int)
#    for token in doc:
#        bow[token] += 1
#    p_w = np.array(bow.values())
#    n = np.sum(p_w)
#    tmp = []
#    for p in p_w:
#        rp = p/float(n)# relative probability
#        tmp.append(rp*np.log2(rp))
#    return -np.sum(np.array(tmp))

def doc2ent(string):
    "Shannon entropy for strings (char-level) or tokenized documents (ngram-level)"
    prob = [float(string.count(c))/len(string) for c in dict.fromkeys(list(string))]
    res = - sum([ p * math.log(p) / math.log(2.0) for p in prob ])
    return res

def ent_list(doc_list):
    """ word level entropy for chunked tokenized documents in list """
    res = []
    for d in doc_list:
        tmp = []
        for c in d:
            tmp.append(doc2ent(c))
        res.append(sum(tmp)/float(len(tmp)))
    return res

def scattermat(l,lab,figname = 'figure'):
    n = len(l)
    f, ax = plt.subplots(n,n, sharey=False, figsize=(n*3,n*3), dpi = 300)
    sns.set_style('white',{'legend.frameon': True,'axes.linewidth': 2})
    plt.rc('font', family='serif', serif='Times')
    plt.rc('text', usetex=True)
    for i in range(n):
        for ii in range(n):
            x = np.array(l[i])
            y = np.array(l[ii])
            if i == ii:
                ax[i,ii].hist(x, 50, normed=1, facecolor='k', alpha=0.75)
                ax[i,ii].set_xlabel(lab[i], fontsize=10, color='k')
            else:
                m, b = np.polyfit(x, y, 1)
                ax[i,ii].plot(x, y, '.', color = 'k')
                ax[i,ii].plot(x, m*x + b, '-', color = 'r')
                ax[i,ii].set_xlabel(lab[i], fontsize=10, color='k')
                ax[i,ii].set_ylabel(lab[ii], fontsize=10, color='k')
            ax[i,ii].tick_params(
                    axis='both',
                    which='both',
                    bottom='off',
                    left='off',
                    top='off',
                    labelbottom='off',
                    labelleft = 'off')
    f.savefig('/home/kln/Documents/fig/'+figname+'.png')
    plt.close(f)




# main
doxs_l =  dirimport(os.path.expanduser('~/Documents/data/test_txt/'))
chnk_l = dirchunk(doxs_l,1000)
ttr_l = ttr_list(chnk_l)
ent_l =  ent_list(chnk_l)


### experiment 1: length matter
## ttr and word-level entropy as a function of document length
filepath = '~/Documents/proj/clear_local/CLEAR/ADL/plain/'
adlfull = dirimport(os.path.expanduser(filepath))
ttr_l = []
ent_l = []
lens_l = []
for doc in adlfull:
    ttr_l.append(doc2ttr(doc))
    ent_l.append(doc2ent(doc))
    lens_l.append(len(doc))
# plot
x = lens_l
y1 = ttr_l
y2 = ent_l
f, axarr = plt.subplots(1,2, sharey=False, figsize=(12,5), dpi = 300)
sns.set_style('whitegrid')
sns.set(style="ticks",font_scale=2)
sns.set_style({'legend.frameon': True,'axes.linewidth': 2})
plt.rc('font', family='serif', serif='Times')
plt.rc('text', usetex=True)
axarr[0].scatter(x, y1, color='k', s=5)
axarr[0].set_title('TTR')
axarr[1].scatter(x, y2, color='k', s=5)
axarr[1].set_title('Entropy')
for i in range(len(axarr)):
    axarr[i].set_xlabel('Tokens', fontsize=24, color='k')
f.savefig('/home/kln/Documents/fig/lengthmatters.png')
plt.close(f)

### experiment 2: slice length
doxs_l =  dirimport(os.path.expanduser('~/Documents/data/test_txt/'))
chnk_l = dirchunk(doxs_l,1000)
ttr_l = ttr_list(chnk_l)
ent_l =  ent_list(chnk_l)

x = range(1,1501)
y1 = []
y2 = []
for i in x:
    c_list = dirchunk(doxs_l,i)
    t_list = ttr_list(c_list)
    e_list = ent_list(c_list)
    y1.append(sum(t_list)/float(len(t_list)))
    y2.append(sum(e_list)/float(len(e_list)))

import numpy as np
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt

f, axarr = plt.subplots(1,2, sharey=False, figsize=(12,5), dpi = 300)
sns.set_style('whitegrid')
sns.set(style="ticks",font_scale=2)
sns.set_style({'legend.frameon': True,'axes.linewidth': 2})
plt.rc('font', family='serif', serif='Times')
plt.rc('text', usetex=True)
axarr[0].plot(x, y1, color='k', lw = 2)
axarr[0].set_title('TTR')
axarr[1].plot(x, y2, color='k', lw = 2)
axarr[1].set_title('Entropy')
for i in range(len(axarr)):
    axarr[i].set_xlabel('Slice size', fontsize=24, color='k')
f.savefig('/home/kln/Documents/fig/slice_size.png')


### experiment 3: length normalized comparison
## compare ttr and word-level entropy on document normalized to slices of 100 unigrams
filepath = '~/Documents/proj/clear_local/CLEAR/ADL/plain/'
adlfull = dirimport(os.path.expanduser(filepath))
adhchnk_l = dirchunk(adlfull,100)
adlttr_l = ttr_list(adhchnk_l)
adlent_l =  ent_list(adhchnk_l)
r = np.corrcoef(adlttr_l,adlent_l)
plt.scatter(adlttr_l, adlent_l,c = 'k', s = 2)
plt.show()

### experiment 4: level of analysis
# comprehensive comparision of length, character-level and word-level entropy, and TTR
filepath = '~/Documents/proj/clear_local/CLEAR/ADL/plain/'
adlfull = dirimport(os.path.expanduser(filepath))
adhchnk_l = dirchunk(adlfull,100)
string_l = [[' '.join(t) for t in chnk] for chnk in adhchnk_l] # chunked tokens to string
# measures
lens = [len(doc) for doc in adlfull]
wordent =  ent_list(adhchnk_l)
charent =  ent_list(string_l)
ttr = ttr_list(adhchnk_l)

l = [lens, charent,wordent,ttr]
r = np.corrcoef(l)
lab = ['Tokens',r'$H(char)$',r'$H(word)$','TTR']
def scattermat(l,lab,figname = 'figure'):
    n = len(l)
    f, ax = plt.subplots(n,n, sharey=False, figsize=(n*3,n*3), dpi = 300)
    sns.set_style('white',{'legend.frameon': True,'axes.linewidth': 2})
    plt.rc('font', family='serif', serif='Times')
    plt.rc('text', usetex=True)
    for i in range(n):
        for ii in range(n):
            x = np.array(l[i])
            y = np.array(l[ii])
            if i == ii:
                ax[i,ii].hist(x, 50, normed=1, facecolor='k', alpha=0.75)
                ax[i,ii].set_xlabel(lab[i], fontsize=10, color='k')
            else:
                m, b = np.polyfit(x, y, 1)
                ax[i,ii].plot(x, y, '.', color = 'k')
                ax[i,ii].plot(x, m*x + b, '-', color = 'r')
                ax[i,ii].set_xlabel(lab[i], fontsize=10, color='k')
                ax[i,ii].set_ylabel(lab[ii], fontsize=10, color='k')
            ax[i,ii].tick_params(
                    axis='both',
                    which='both',
                    bottom='off',
                    left='off',
                    top='off',
                    labelbottom='off',
                    labelleft = 'off')
    f.savefig('/home/kln/Documents/fig/'+figname+'.png')
    plt.close(f)

scattermat(l,lab,'complexmeas')

### experiment 5: normalized measures of type-token ratios
doxs_l =  dirimport(os.path.expanduser('~/Documents/data/test_txt/'))

print doc2ttr(doxs_l[0])
print doc2ttrnorm(doxs_l[0])





#
## alpha
import math

def doc2ent(string):
    "Shannon entropy for strings (char-level) or tokenized documents (ngram-level)"
    prob = [float(string.count(c))/len(string) for c in dict.fromkeys(list(string))]
    res = - sum([ p * math.log(p) / math.log(2.0) for p in prob ])
    return res
