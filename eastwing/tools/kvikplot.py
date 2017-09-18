#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""

"""
__author__= "KLN"

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab

def plotdist(x, sv = 0, filename = "dist.png"):
    """ histogram with normal fit """
    mu = np.mean(x)
    sigma =  np.std(x)
    n, bins, patches = plt.hist(x, 50, normed=1, facecolor='k', alpha=0.75)
    y = mlab.normpdf( bins, mu, sigma)# best normal fit
    ax = plt.plot(bins, y, 'r--', linewidth=1)
    plt.ylabel('Probability')
    plt.grid(True)
    if sv == 1:
        plt.savefig(filename, dpi = 300)
    else:
        plt.show()
        plt.close()

def qd_plot(x,y = 0, sv = 0, filename = 'qd_plot.png', ax1 = '$x$', ax2 = '$f(x)$'):
    """
    quick and dirty x and x-y plotting
    """
    fig, ax = plt.subplots()
    if y:
        ax.scatter(x,y, color = 'k')
        ax.set_xlabel(ax1)
        ax.set_ylabel(ax2)
    else:
        ax.plot(x, color = 'k')
        ax.set_xlabel("$time$")
        ax.set_ylabel("$var~1$")
    plt.rc('text', usetex=True)
    font = {'family' : 'serif','serif': ['times'], 'weight' : 'bold', 'size': 12}
    mpl.rc('font', **font)
    mpl.rcParams['axes.linewidth'] = 2
    if sv == 1:
        plt.savefig(filename, dpi = 300)
    else:
        plt.show()
        plt.close()

def smooth(l, N = 5):
    """
    smooting with a moving average over N steps
    """
    sum = 0
    res = list(0 for x in l)# pre-allocate
    for i in range(0, N):
        sum = sum + l[i]
        res[i] = sum/(i+1)
    for i in range(N,len(l)):
        sum = sum - l[i-N] + l[i]
        res[i] = sum/N
    return res
