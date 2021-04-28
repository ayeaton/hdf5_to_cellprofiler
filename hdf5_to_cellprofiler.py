import h5py
import glob
import os
import numpy as np
import cv2
from itertools import chain
import random
import pandas
import argparse
import tempfile
import subprocess
import sys
import shutil
import tempfile

parser = argparse.ArgumentParser(description="Convert jpeg images sorted is subfolders (1 per class) to hdf5 format.")
parser.add_argument("--input", type=str, default='/gpfs/data/abl/deepomics/AdalQuiros/SharedData/Raw_HDF5/FFPE/hdf5_TCGAFFPE_set00_test.h5',
                        help="path and name of output")
parser.add_argument("--chunks", type=int, default=10,
                        help="number of sub-chunks")
parser.add_argument("--rank", type=int, default=10,
                        help="number of sub-chunks")
parser.add_argument("--type", type = str, default = "train")
parser.add_argument("--output", type = str, default = "/gpfs/home/ay1392/scratch/Lung/data/test")
parser.add_argument("--working_dir", type = str, default = "/gpfs/home/ay1392/scratch/Lung/")
parser.add_argument("--name", type = str, default = "rank")
args = parser.parse_args()

input = args.input
working_dir = args.working_dir
type = args.type
output = args.output
name = args.name
rank = args.rank - 1
chunks = args.chunks

print(sys.argv[1:])

## get the indices of the hdf5 file

# create hdf5 dataset
f = h5py.File(input, 'r')
# get the keys in the dataset
keys =  [x if isinstance(x, str) else '' for x in f.keys()]
# get the number of entries
f_tiles = f[keys[0]]
num_images = f_tiles.shape[0]
f.close()
# size of the chunks
chunk_size, remainder = divmod(num_images, chunks)
chunk_size = chunk_size + 1
remainder = num_images - (chunk_size * (chunks -1))
print("total images:" + str(num_images) + ", " + str(chunk_size) + " chunks")
if rank == (chunks - 1):
    start = int(rank * chunk_size)
    end = int(start + remainder)
    print("rank: " + str(rank) + " start: " + str(start) + " end: " + str(end))
else:
    start = int(rank * chunk_size)
    end = int(start + chunk_size)
    print("rank: " + str(rank) + " start: " + str(start) + " end: " + str(end))

## create lists of the keys and images

# re open the file
f = h5py.File(input, 'r')
#get unique labels for each entry
datasets_subbed =  [f[key][start:end, ] if len(f[key][start:end, ].shape) == 1 else "NOT1D" for key in keys]
if "NOT1D" in datasets_subbed:
    datasets_subbed.remove("NOT1D")
unique_information_str =  [[str(x.decode("utf-8")) if hasattr(x, 'decode') else str(x) for x in key]  for key in datasets_subbed]

# assume image dataset is the only one that is not one dimensional
f_img = [f[key][start:end, ] if len(f[key][start:end, ].shape) != 1 else '1D' for key in keys]
if "NOT1D" in f_img:
    f_img.remove("1D")
f_img = f_img[0]

## write the images to a temp file

ranges = end - start
print("ranges" + str(ranges))
temp_path = tempfile.mkdtemp(dir = working_dir)
for i, img in enumerate(f_img):
    current_info =  [inf[i] for inf in unique_information_str]
    filename = '_'.join(current_info)
    filename = temp_path + "/" + filename
    print(filename)
    cv2.imwrite(filename, img)

## create a file listing all the images

file_path = temp_path + '/file_list.txt'
print(file_path)
l = list(glob.glob(temp_path + '/*.jpeg'))
f1 = open(file_path, 'w')
s1 = '\n'.join(l)
f1.write(s1)
f1.close()

## run a cellprofiler subprocess
proc = subprocess.call([os.path.join(os.path.abspath(sys.path[0]), "cellprofiler.sh"),
                         file_path,
                         working_dir])
print(os.listdir(temp_path))

os.mkdir(output)

os.rename(temp_path + '/nuclei.txt', output + '/nuclei'  + str(name) + str(rank)  +  '.txt')
os.rename(temp_path + '/file_list.txt', output + '/file_list' + str(name) + str(rank)  + '.txt')
os.rename(temp_path + '/Image.txt', output + '/Image' + str(name) + str(rank) + '.txt')

for fn in l:
   os.remove(fn)

l2 = list(glob.glob(temp_path + '/*.txt'))
for fn in l2:
   os.remove(fn)

os.rmdir(temp_path)

f.close()
