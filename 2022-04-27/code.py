import numpy as np
from matplotlib.pyplot import * # TODO: don't import *
from pickle import load
from gzip import open
# TODO: use xarray to name the dimensions!
# TODO: use pathlib.Path
# TODO: put the repeated code into functions
# TODO: better variable names
# TODO: use a `list` for the individual files
file1 = 'data/detector1.pkl.gz' # HEIGHT x WIDTH x R/G/B x TIME
file2 = 'data/detector2.pkl.gz' # TODO: don't use pickle; use HDF5, TIFF for long-term, shared use
imgs1 = load(open(file1, 'rb')) # TODO: use PEP-343 context managers/`with`-statement
imgs2 = load(open(file2, 'rb'))

h, w, c, t = imgs1.shape
# TODO: add assertions to check/document assumptions
lft = imgs1[0:h, 0:w, 0:c, 0] # TODO: use `...` for indexing; e.g., imgs1[..., 0] or imgs1[:, :, :, 0]
rgt = imgs2[0:h, 0:w, 0:c, 0]
res = [np.mean([lft, rgt], axis=0)]
for time in range(1, t):
    lft = imgs1[0:h, 0:w, 0:c, time]
    rgt = imgs2[0:h, 0:w, 0:c, time]
    res = np.concatenate([res, [np.mean([lft, rgt], axis=0)]], axis=0) # TODO: use a `list` to append
                                                                       #       then concatenate at the end

# TODO: use pcolormesh only for non-evenly gridded data; use imshow instead
saturated_img = res.max(axis=0)
pcolormesh(saturated_img[0:h, 0:w, 0]) # red
savefig('output/'+file1.split('/')[-1]+'vs'+file2.split('/')[-1]+'red.png') # TODO: use a variable for the filenames
pcolormesh(saturated_img[0:h, 0:w, 1]) # green                              # TODO: use fstring instead of `+`
savefig('output/'+file1.split('/')[-1]+'vs'+file2.split('/')[-1]+'green.png')
pcolormesh(saturated_img[0:h, 0:w, 2]) # blue
savefig('output/'+file1.split('/')[-1]+'vs'+file2.split('/')[-1]+'blue.png')
