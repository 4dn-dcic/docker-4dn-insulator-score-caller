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
#@click.argument('filename')
@click.option('--window', default=100000, help='')
@click.option('--cutoff', default=2, help='')
@click.option('--binsize', default=-1, help='')

def main(mcoolfile,outdir,window,cutoff,binsize):
    f = mcoolfile

    #Get the list of resolutions in the mcool file
    cooler_list = cooler.io.ls(f)
    old_version= False

    if not any([res for res in cooler_list if '/resolutions/' in res]): #gets the resolutions from a file in a older version of cooler
        old_version = True
        binsize_list = []
        for res in cooler_list:
            cooler_path = str(f)+'::'+ res
            c = cooler.Cooler(cooler_path)
            binsize_list.append(int(c.binsize))
    else:
        binsize_list = []
        for res in cooler_list:
            binsize_list.append(int(res.split('/')[-1]))

    # Check the input parameters
    if binsize == -1:
        binsize = min(binsize_list)
    else:
        if binsize in binsize_list:
            if window % binsize != 0:
                print("Error: Window size must be multiple of binsize")
                sys.exit()
        else:
            print("Error: This binsize is not available in this mcool file. This is the list of binsizes availables:")
            print(binsize_list)
            sys.exit()

    # Creates a cooler object
    if old_version:
        res_list = []
        for res in cooler_list:
            res_list.append(int(res.split('/')[-1]))
            res_index = max(res_list)

        cooler_path = str(f) + '::' + str(res_index)
    else:
        cooler_path = str(f) + '::' + cooler_list[binsize_list.index(binsize)]
    c = cooler.Cooler(cooler_path)
    print(c)

    # Gets the chromsizes
    chromsizes=pd.Series(c.chroms()[:]['length'].values, index=c.chroms()[:]['name'].values)
    #Getting insulating boundaries
    insul = find_insulating_boundaries(c,balance='weight',window_bp=window,min_dist_bad_bin=2)

    #Convert to BigWig
    bioframe.to_bigwig(insul, chromsizes,
                       f'/{outdir}/output2.bw',
                       f'log2_insulation_score_{window}')


if __name__ == "__main__":
    main()


