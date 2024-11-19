#!/usr/bin/env python
#
# Run the rebrab tool to look for a offending antennas and baselines...
#
import os

import argparse
import logging

import matplotlib.pyplot as plt
from matplotlib import colors

from astropy.utils.data import get_pkg_data_filename
from astropy.io import fits

import numpy as np

from datetime import datetime as dt

from astropy.visualization import astropy_mpl_style
plt.style.use(astropy_mpl_style)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Rebrab: It will remove your fringe in a jiffy.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--fits', required=True,
                        help="The image with RFI.")

    parser.add_argument('--version', action="store_true",
                        help="Display the current version")
    parser.add_argument('--debug', action="store_true",
                        help="Display debugging information")

    ARGS = parser.parse_args()

    if ARGS.debug:
        level = logging.DEBUG
    else:
        level = logging.ERROR

    logging.basicConfig()
    logger = logging.getLogger('rebrab')
    logger.setLevel(level)

    if ARGS.debug:
        fh = logging.FileHandler(filename=f"rebrab.{dt.now().timestamp()}.log")
        fh.setLevel(level)

        # create console handler and set level to debug
        ch = logging.StreamHandler()
        ch.setLevel(level)

        # create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # add formatter to ch
        ch.setFormatter(formatter)
        fh.setFormatter(formatter)

        # add ch to logger
        logger.addHandler(ch)
        logger.addHandler(fh)

    logger.info("Rebrab parameters:")
    for k in vars(ARGS).keys():
        val = getattr(ARGS, k, "Information Unavailable")
        reprk = str(k).ljust(20, " ")
        logger.info(f"\t{reprk}: {val}")

    logger.info(f"Getting Data from FITS image: {ARGS.fits}")

    if not os.path.exists(ARGS.fits):
        raise RuntimeError(f"FITS image {ARGS.fits} not found")

    image_file = get_pkg_data_filename(ARGS.fits)
    logger.info(fits.info(image_file))
    image_data = fits.getdata(image_file, ext=0)

    if True:
        uv_plane = np.fft.fftshift(np.fft.fft2(np.fft.ifftshift(image_data)))[0,0,:,:]

        '''
        num_bin = 2**9  # Image resolution
        nw=num_bin/4

        bl_pos = ant_pos[baselines]
        uu_a, vv_a, ww_a = (bl_pos[:,0] - bl_pos[:,1]).T/constants.L1_WAVELENGTH

        # Grid the visibilities in the UV plane.
        uu_edges = np.linspace(-nw, nw, num_bin+1)
        vv_edges = np.linspace(-nw, nw, num_bin+1)

        uv_plane = np.zeros((num_bin, num_bin), dtype=np.complex64)
        uu_comb = np.concatenate((uu_a, -uu_a))
        vv_comb = np.concatenate((vv_a, -vv_a))
        all_v     = np.concatenate((vis_l, np.conjugate(vis_l)))
        h_real,_,_ = np.histogram2d(vv_comb, uu_comb, weights = all_v.real, bins=[vv_edges, uu_edges])
        h_imag,_,_ = np.histogram2d(vv_comb, uu_comb, weights = all_v.imag, bins=[vv_edges, uu_edges])
        num_entries,_,_ = np.histogram2d(vv_comb, uu_comb, bins=[vv_edges, uu_edges])
        uv_plane[:,:] = (h_real+(1j*h_imag))
        pos = np.where(num_entries.__gt__(1))
        uv_plane[pos] /= num_entries[pos]


        cal_ift = np.fft.fftshift(fft.ifft2(np.fft.ifftshift(uv_plane)))  # 

        # Take the absolute value to make an intensity image
        img = np.abs(cal_ift)
        # Scale it to multiples of the image standard deviation
        img /= np.std(img)
        '''
    absvis = np.abs(uv_plane)
    max_index = np.unravel_index(np.argmax(absvis, axis=None), shape=absvis.shape)

    max_vis = absvis[max_index]
    p01, p05, p50, p95, p99, p999, p9995 = np.percentile(absvis, [1, 5, 50, 95, 99, 99.9, 99.95])

    print("Rebrab UV Report")
    print(f"    Max |v| = {max_vis}")
    print(f"    vis percentiles (n={absvis.shape[0]}):")
    print(f"        5%={p05 :5.2f}")
    print(f"        50%={p50 :5.2f}")
    print(f"        95%={p95:5.2f}")
    print(f"        99%={p99:5.2f}")
    print(f"        99.9%={p999:5.2f}")
    print(f"        99.99%={p9995:5.2f}")

    clear = np.where(absvis < p9995)
    absvis[clear] = float("nan")
    plt.figure()
    plt.imshow(absvis, cmap="viridis_r", norm=colors.Normalize(vmin=p999, clip=True))
    plt.colorbar()
    plt.show()

    # print(f"    ANT1 = {ant1[dump_index]}")
    # print(f"    ANT2 = {ant2[dump_index]}")
    # print(f"    u = {u_arr[dump_index]}")
    # print(f"    v = {v_arr[dump_index]}")
    # print(f"    w = {w_arr[dump_index]}")
    # 
    # if ARGS.debug:
    #     min_index = np.unravel_index(np.argmin(absvis, axis=None), shape=absvis.shape)
    #     dump_index = min_index[0]
    # 
    #     print("\n DEBUG: Min Vis Report")
    #     print(f"    Min |v| = {absvis[min_index]}")
    #     print(f"    flags[{min_index}] = {flags[min_index]}")
    #     print(f"    ANT1 = {ant1[dump_index]}")
    #     print(f"    ANT2 = {ant2[dump_index]}")
    #     print(f"    u = {u_arr[dump_index]}")
    #     print(f"    v = {v_arr[dump_index]}")
    #     print(f"    w = {w_arr[dump_index]}")

