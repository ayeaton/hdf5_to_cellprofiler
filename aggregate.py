import glob
import pandas as pd
import argparse

parser = argparse.ArgumentParser(description="Convert jpeg images sorted is subfolders (1 per class) to hdf5 format.")
parser.add_argument("--chunks", type=int, default='')
parser.add_argument("--rank", type=int, default='')
parser.add_argument("--output", type=int, default='')

args = parser.parse_args()
chunks = args.chunks
rank = args.rank - 1
output = args.output


# read in all the file rank files
l = list(glob.glob(output + "/IdentifySecondaryObjects" + '*.txt'))
num_images = len(l)

# size of the chunks
chunk_size, remainder = divmod(num_images, chunks)
chunk_size = chunk_size + 1
remainder = num_images - (chunk_size * (chunks -1))
print("total images:" + str(num_images) + ", " + str(chunk_size) + " chunks")
# get start and end indices of the hdf5
## does this over write one space??
#if rank == (chunks - 1):
if rank == (chunks - 1):
    start = int(rank * chunk_size)
    end = int(start + remainder)
    print("rank: " + str(rank) + " start: " + str(start) + " end: " + str(end))
else:
    start = int(rank * chunk_size)
    end = int(start + chunk_size)
    print("rank: " + str(rank) + " start: " + str(start) + " end: " + str(end))

l = l[start:end]

# for unique tile name

corpus = []
for file_path in l:
    print(file_path)
    data = pd.read_csv(file_path, delimiter = '\t')
    summ_stats  = data[["AreaShape_Center_X", "AreaShape_Area", "Metadata_FileLocation", "AreaShape_Center_Y",
          "AreaShape_Center_Z", "AreaShape_Compactness", "AreaShape_Eccentricity",
          'AreaShape_EulerNumber', 'AreaShape_Extent', 'AreaShape_FormFactor',
          'AreaShape_MajorAxisLength', 'AreaShape_MaxFeretDiameter',
          'AreaShape_MaximumRadius', 'AreaShape_MeanRadius',
          'AreaShape_MedianRadius', 'AreaShape_MinFeretDiameter',
          'AreaShape_MinorAxisLength', 'AreaShape_Orientation',
          'AreaShape_Perimeter', 'AreaShape_Solidity']].groupby("Metadata_FileLocation").describe()
    new_list = ['.'.join(words) for words in summ_stats.columns]
    summ_stats.columns = new_list
    corpus.append(summ_stats)

fin = pd.concat(corpus)
fin.to_csv(output + "/" + str(start) + "-" + str(end) + "-aggregate-cells.csv")
