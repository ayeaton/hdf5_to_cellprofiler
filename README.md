This is my solution to running cellprofiler on hdf5s. I could not figure out how
to actually run cellprofiler on hdf5s so instead of poking around in the cellprofiler
code, I have created a wrapper that write the images in an hdf5 into temporary
directories, and using these images as input into cellprofiler. The code also employs
parallelization to make things faster. This pipeline uses MPI to accomplish
handling the hdf5 in parallel.

Step 1. Create a cellprofiler pipeline.

Step 2. Change the inputs in submit_jobs.sh to match your needs

Step 3. Run loop_jobs.sh specifying how many chunks you want. For 100 chunks: sbatch loop_jobs.sh 100

Step 4. Aggregate all of the separate cellprofiler outputs of measurements of objects
by running loop_jobs_agg.sh. 
My aggregate code in aggregate.py is pretty specific to what I care about.

The code that does the actual work is hdf5_to_cellprofiler.py. This code takes
a chunk of the hdf5, creates a temporary directory and write the images in the chunk
as jpegs and runs a cellprofiler subprocess on these images. At the end, the code will move the
output files to a specified output directory and delete the tmp directory.

The cellprofiler pipeline is just called pipeline. Change the pipeline name in
cellprofiler.sh if you want to use a different one.
