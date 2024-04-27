import rasterio as r
import numpy as np
import earthpy.plot as ep
import matplotlib.pyplot as plt

"""
I've used code from a turorial: https://zectre.github.io/geospatialpython/2021/08/08/NDVI-With-Rasterio.html

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
    """
    :param band4 is red band in Landsat 8-9:
    :param band5 is near infrared in Landsat 8-9:
    """
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


def calc_ndsi(band3, band6):
    np.seterr(divide='ignore', invalid='ignore')
    ob3 = r.open(band3).read(1)
    ob6 = r.open(band6).read(1)
    green = ob3.astype('float64')
    swir1 = ob6.astype('float64')

    ndsi = np.where(
        (green + swir1) == 0.,  # It will return -1 for No Data value
        -1,
        (green - swir1) / (green + swir1))

    return ndsi


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
    ndviplot = r.open(path).read(1)
    ep.plot_bands(ndviplot,
                  cmap=cmap,
                  title=title)
    plt.show()


if __name__ == '__main__':
    band4 = 'data\LC08_L1TP_188024_20240110_20240122_02_T1_B4.TIF'
    band5 = 'data\LC08_L1TP_188024_20240110_20240122_02_T1_B5.TIF'
    ndvi = calc_ndvi(band4, band5)
    save_to_geotiff(ndvi, r'results\ndvi.tiff', band4)
    plot_raster(r'results\ndvi.tiff', "NDVI", 'RdYlGn')

    band3 = 'data\LC09_L1TP_187026_20240315_20240315_02_T1_B3.TIF'
    band6 = 'data\LC09_L1TP_187026_20240315_20240315_02_T1_B6.TIF'
    ndsi = calc_ndsi(band3, band6)
    save_to_geotiff(ndsi, r'results\ndsi_carpathian_mountains.tiff', band3)
    plot_raster(r'results\ndsi_carpathian_mountains.tiff', "NDSI", 'RdBu')

    band3 = 'data\LC09_L1TP_193028_20240325_20240325_02_T1_B3.TIF'
    band6 = 'data\LC09_L1TP_193028_20240325_20240325_02_T1_B6.TIF'
    ndsi = calc_ndsi(band3, band6)
    save_to_geotiff(ndsi, r'results\ndsi_alpes.tiff', band3)
    plot_raster(r'results\ndsi_alpes.tiff', "NDSI", 'RdBu')


