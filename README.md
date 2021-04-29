

This is my solution to running cellprofiler on hdf5s. I could not figure out how
to actually run cellprofiler on hdf5s. It seems like it would be a difficult task to
implement given the flexibility of hdf5 files. In the hdf5s that I am working with
I have one dataset containing the images, and several datasets with relevant
labels for each image. There are no special groupings or hierarchy.

I have created a wrapper to write the images in an hdf5 into temporary
directories, and uses these images as input into cellprofiler. The code then moves
the relevant output files to a specified output path and deletes the tmp directories.
The code  employs parallelization to make things faster.

Step 1. Create a cellprofiler pipeline.

Step 2. Change the inputs in parameters.csv to fit your needs.

Step 3. Run loop_jobs.sh

Step 4. Aggregate all of the separate cellprofiler outputs of measurements of objects
by running loop_jobs_agg.sh.
My aggregate code in aggregate.py is pretty specific to what I care about.

The code that does the actual work is hdf5_to_cellprofiler.py. This code takes
a chunk of the hdf5, creates a temporary directory and write the images in the chunk
as jpegs and runs a cellprofiler subprocess on these images. At the end, the code will move the
output files to a specified output directory and delete the tmp directory.

The cellprofiler pipeline is just called pipeline. Change the pipeline name in
cellprofiler.sh if you want to use a different one.
