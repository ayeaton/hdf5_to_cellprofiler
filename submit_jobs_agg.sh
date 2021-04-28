#!/bin/bash
#SBATCH --time=00-20:00:00
#SBATCH --partition=cpu_short,cpu_medium
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=10G
#SBATCH --job-name=cp

chunks=$1
rank=$2


echo $chunks
echo $rank

module load python/cpu/3.6.5

python aggregate.py --chunks $chunks --rank $rank
