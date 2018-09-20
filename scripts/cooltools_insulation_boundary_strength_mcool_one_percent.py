#!/usr/bin/env python3

import sys
from matplotlib.gridspec import GridSpec
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
import numpy as np
import pandas as pd
import bioframe
import cooltools
from cooltools.insulation import find_insulating_boundaries
import cooler
import bbi
import multiprocess as mp
import os as os

f='one_percent.mcool'
cooler_list=cooler.io.ls(f)
print(cooler_list)

for res in cooler_list:
    binsize=int(res.split('/')[-1])
    print(binsize)
    cooler_path=str(f)+'::'+res
    c=cooler.Cooler(cooler_path)
    print(c)
    chromsizes=pd.Series(c.chroms()[:]['length'].values, index=c.chroms()[:]['name'].values)


    window_bp = binsize * 10

    # Diamond insulation score
    insul = find_insulating_boundaries(c,balance='weight',window_bp=window_bp,min_dist_bad_bin=2)
    insul.to_csv(f'/usr/local/bin/result_files/one_percent.{binsize//1000}kb.window_{window_bp//1000}kb.insul.tsv', sep='\t')
    bioframe.to_bigwig(insul, chromsizes,
                           f'/usr/local/bin/result_files/one_percent.{binsize//1000}kb.window_{window_bp//1000}kb.insul_score.bw',
                           f'log2_insulation_score_{window_bp}')

    bioframe.to_bigwig(insul, chromsizes,
                           f'/usr/local/bin/result_files/one_percent.{binsize//1000}kb.window_{window_bp//1000}kb.insul_pp.bw',
                           f'boundary_strength_{window_bp}')
