#!/bin/bash
#SBATCH --time=00-00:10:00
#SBATCH --partition=cpu_short,cpu_medium
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=2G
#SBATCH --job-name=loop_cp

INPUT=parameters.csv

while IFS=$',' read input output working_dir types name END blank
do
  echo "input : $input"
  echo "output : $output"
  echo "working_dir : $working_dir"
  echo "types : $types"
  echo "name : $name"

  for i in $(seq 1 $END);
    do sbatch submit_jobs_agg.sh $END $i $output;
  done

done < $INPUT
