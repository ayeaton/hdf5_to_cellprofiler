#!/bin/bash
#SBATCH --time=00-20:00:00
#SBATCH --partition=cpu_short,cpu_medium
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=10G
#SBATCH --job-name=cp

# Print the task id.
echo "My SLURM_ARRAY_TASK_ID: " $SLURM_ARRAY_TASK_ID

input=$1
chunks=$2
rank=$3
output=$4
working_dir=$5
types=$6
name=$7

echo $input
echo $chunks
echo $rank
echo $output
echo $working_dir
echo $types
echo $name

module purge
module load python/cpu/3.6.5

python hdf5_to_cellprofiler.py --input $input \
 --chunks $chunks \
 --rank $rank \
 --output $output \
 --working_dir $working_dir \
 --type $types \
 --name $name
