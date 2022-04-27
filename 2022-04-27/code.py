import numpy as np
from matplotlib.pyplot import *
from pickle import load
from gzip import open

file1 = 'data/detector1.pkl.gz' # HEIGHT x WIDTH x R/G/B x TIME
file2 = 'data/detector2.pkl.gz'
imgs1 = load(open(file1, 'rb'))
imgs2 = load(open(file2, 'rb'))

h, w, c, t = imgs1.shape
lft = imgs1[0:h, 0:w, 0:c, 0]
rgt = imgs2[0:h, 0:w, 0:c, 0]
res = [np.mean([lft, rgt], axis=0)]
for time in range(1, t):
    lft = imgs1[0:h, 0:w, 0:c, time]
    rgt = imgs2[0:h, 0:w, 0:c, time]
    res = np.concatenate([res, [np.mean([lft, rgt], axis=0)]], axis=0)

saturated_img = res.max(axis=0)
pcolormesh(saturated_img[0:h, 0:w, 0]) # red
savefig('output/' + file1.split('/')[-1] + 'vs' + file2.split('/')[-1] + 'red.png')
pcolormesh(saturated_img[0:h, 0:w, 1]) # green
savefig('output/' + file1.split('/')[-1] + 'vs' + file2.split('/')[-1] + 'green.png')
pcolormesh(saturated_img[0:h, 0:w, 2]) # blue
savefig('output/' + file1.split('/')[-1] + 'vs' + file2.split('/')[-1] + 'blue.png')
