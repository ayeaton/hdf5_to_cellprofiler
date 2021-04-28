#!/bin/bash
#SBATCH --time=00-00:10:00
#SBATCH --partition=cpu_short,cpu_medium
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=2G
#SBATCH --job-name=loop_cp

END=$1
echo $END

for i in $(seq 1 $END);
  do sbatch submit_jobs_agg.sh $END $i;
done
