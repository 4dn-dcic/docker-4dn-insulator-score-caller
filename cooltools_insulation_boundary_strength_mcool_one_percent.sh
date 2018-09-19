#!/bin/bash

#SBATCH -c 4
#SBATCH -N 1
#SBATCH -t 0-10:00
#SBATCH -p short
#SBATCH --mem=10G
#SBATCH -o one_percent_cooltools_mcool_%j.out
#SBATCH -e one_percent_cooltools_mcool_%j.err
#SBATCH --mail-type=ALL
#SBATCH --mail-user=raag@bu.edu

source activate test_bootcamp_env
cd /home/ag474/DATA/one_percent_files/
python ~/cooltools_insulation_boundary_strength_mcool_scripts/cooltools_insulation_boundary_strength_mcool_one_percent.py 
