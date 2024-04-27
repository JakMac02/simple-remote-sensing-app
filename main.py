import os
import earthpy as et
import earthpy.spatial as es
import rasterio as r
import numpy as np
from rasterio.plot import show
import earthpy.plot as ep
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import matplotlib.colors as colors

"""
It's a code from a turorial: https://zectre.github.io/geospatialpython/2021/08/08/NDVI-With-Rasterio.html

Libraries copyrights:
    Rasterio github: https://github.com/rasterio/rasterio?tab=readme-ov-file
        Copyright (c) 2013-2021, Mapbox
        All rights reserved.
    
    EarthPy github: https://github.com/earthlab/earthpy?tab=readme-ov-file
        article - Wasser2019EarthPy
        journal Journal of Open Source Software
        doi 10.21105/joss.01886
        issn 2475-9066
        number 43
        publisher The Open Journal
        title EarthPy: A Python package that makes it easier to explore and plot raster and vector data using open source Python tools.
        url https://doi.org/10.21105/joss.01886
        volume 4
        author Wasser, Leah and Joseph, Maxwell and McGlinchy, Joe and Palomino, Jenny and Korinek, Nathan and Holdgraf, Chris and Head, Tim
        pages 1886
        date 2019-11-13
        year 2019
        month 11
        day 13
"""

def calc_ndvi(band4, band5):
    np.seterr(divide='ignore', invalid='ignore')
    ob4 = r.open(band4).read(1)
    ob5 = r.open(band5).read(1)
    red = ob4.astype('float64')
    nir = ob5.astype('float64')

    ndvi=np.where(
        (nir+red) == 0., #It will return 0 for No Data value
        0,
        (nir-red)/(nir+red))

    return ndvi


def save_to_geotiff(raster, path, b4data):
    b4data = r.open(b4data)
    ndviTiff = r.open(path,
                  'w',
                  driver='Gtiff',
                  width = b4data.width,
                  height = b4data.height,
                  count=1, crs=b4data.crs,
                  transform=b4data.transform,
                  dtype='float64')
    ndviTiff.write(raster, 1)
    ndviTiff.close()


def plot_raster(path, title, cmap):
    ndviplot = r.open(r'results\ndvi.tiff').read(1)
    ep.plot_bands(ndviplot,
                  cmap='RdYlGn',
                  title="NDVI")
    plt.show()


if __name__ == '__main__':
    band4 = 'data\LC08_L1TP_188024_20240110_20240122_02_T1_B4.TIF'
    band5 = 'data\LC08_L1TP_188024_20240110_20240122_02_T1_B5.TIF'
    ndvi = calc_ndvi(band4, band5)
    save_to_geotiff(ndvi, r'results\ndvi.tiff', 'data\LC08_L1TP_188024_20240110_20240122_02_T1_B4.TIF')
    plot_raster(r'results\ndvi.tiff', "NDVI", 'RdYlGn')