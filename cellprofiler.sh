#!/bin/bash

module purge
module add miniconda2/4.5.4 jbig/2.1
conda activate cellprofiler
export PATH=/gpfs/share/apps/miniconda2/4.5.4/envs/cellprofiler/bin:$PATH

files=$1
working_dir=$2

cellprofiler -c -r -p pipeline.cppipe --file-list "$files" -o "$working_dir"
