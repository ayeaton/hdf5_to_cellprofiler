#!/bin/bash
#SBATCH --time=00-20:00:00
#SBATCH --partition=cpu_short,cpu_medium
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=10G
#SBATCH --job-name=cp

# Print the task id.
echo "My SLURM_ARRAY_TASK_ID: " $SLURM_ARRAY_TASK_ID

chunks=$1
rank=$2


echo $chunks
echo $rank

module purge
module load python/cpu/3.6.5


python hdf5_to_cellprofiler.py --input /gpfs/data/abl/deepomics/AdalQuiros/SharedData/Raw_HDF5/FFPE_90pc_Bkg_rescaled/hdf5_TCGAFFPE4_set00_test.h5 \
 --chunks $chunks \
 --rank $rank \
 --output /gpfs/home/ay1392/scratch/Lung/data/TCGAFFPE4_set00 \
 --working_dir /gpfs/home/ay1392/scratch/Lung/data \
 --type "test" \
 --name "TCGAFFPE4_set00_test"
 
