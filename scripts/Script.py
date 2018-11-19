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
@click.option('--window', default=100000, help='')
@click.option('--cutoff', default=2, help='')
@click.option('--binsize', default=-1, help='')

def main(mcoolfile,outdir,filename,window,cutoff,binsize):
 f=mcoolfile

 #Get list of resolutions in the mcool file:
 cooler_list=cooler.io.ls(f)
 list_lenght = len(cooler_list)
 res_list = [1] * list_lenght
 x = 0

 for res in cooler_list:
    res_list[x] = int(res.split('/')[-1])
    x = x + 1

 #Test input parameters:
 if binsize == -1:
    binsize = min(res_list)

 if binsize in res_list:
    if window % binsize != 0:
        print("Error: window size must be a multiple of binsize ")
        sys.exit()
 else:
    print( "Error: The binsize is not available in this mcool file. This is the list of binsizes:")
    print(res_list)
    sys.exit()

 #Getting cooler file in a convinient interface
 cooler_path=str(f)+'::'+ cooler_list[res_list.index(binsize)]
 c=cooler.Cooler(cooler_path)
 print(c)
 chromsizes=pd.Series(c.chroms()[:]['length'].values, index=c.chroms()[:]['name'].values)

 #Getting insulating boundaries
 insul = find_insulating_boundaries(c,balance='weight',window_bp=window,min_dist_bad_bin=2)

 #Convert to BigWig
 bioframe.to_bigwig(insul, chromsizes,
                       f'./{outdir}/{filename}.bw',
                       f'log2_insulation_score_{window}')

if __name__ == "__main__":
    main()

