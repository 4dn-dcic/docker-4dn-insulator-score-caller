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
import click

@click.command()
@click.argument('mcoolfile')
@click.argument('outdir')
@click.argument('filename')
@click.option('--window', default=5, help='')
@click.option('--cutoff', default=2, help='')
#@click.option('--binsize', default=1000, help='')

def main(mcoolfile,outdir,filename,window,cutoff ):
 f=mcoolfile
 cooler_list=cooler.io.ls(f)
 binsize = int(cooler_list[0].split('/')[-1])

 cooler_path=str(f)+'::'+ cooler_list[0]
 c=cooler.Cooler(cooler_path)
 print(c)
 chromsizes=pd.Series(c.chroms()[:]['length'].values, index=c.chroms()[:]['name'].values)

 window_bp = binsize * window

 insul = find_insulating_boundaries(c,balance='weight',window_bp=window_bp,min_dist_bad_bin=2)
 bioframe.to_bigwig(insul, chromsizes,
                       f'./{outdir}/{filename}.bw',
                       f'log2_insulation_score_{window_bp}')

if __name__ == "__main__":
    main()
