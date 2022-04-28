import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
from gzip import open
from pathlib import Path

data_dir, output_dir = Path('./data'), Path('./output')
files = {
    'lft': data_dir / 'detector1.npy.gz',
    'rgt': data_dir / 'detector2.npy.gz',
}

images = {}
for det, fn in files.items():
    with open(fn, 'rb') as f:
        images[det] = xr.DataArray(
            data=np.load(f),
            dims=['height', 'width', 'channel', 'time'],
            coords={'channel': ['red', 'green', 'blue']},
        )
        assert images[det].shape == (100, 100, 3, 10)

combined_img = sum(images.values()) / len(images)
saturated_img = combined_img.max(dim='time')

for chan in saturated_img.coords['channel']:
    filename = output_dir / f'{"-vs-".join(images.keys())}-{chan.item()}.png'
    plt.imshow(saturated_img.sel(channel=chan))
    plt.savefig(filename)
