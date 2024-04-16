#!/usr/bin/env python
#
# Run the barber tool to look for a possible fringe...
#
import os

from datetime import datetime as dt

import argparse
import logging

import numpy as np

from casa_read_ms import read_ms as casa_read_ms

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Barber: It will remove your fringe in a jiffy.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--ms', required=True,
                        help="The source measurement set.")
    parser.add_argument('--field', type=int, default=0,
                        help="Use this FIELD_ID from the measurement set.")

    parser.add_argument('--debug', action="store_true",
                        help="Display debugging information")
    parser.add_argument('--version', action="store_true",
                        help="Display the current version")

    ARGS = parser.parse_args()

    if ARGS.debug:
        level = logging.DEBUG
    else:
        level = logging.ERROR

    logging.basicConfig()
    ms_logger = logging.getLogger('casa_read_ms')
    ms_logger.setLevel(level)
    logger = logging.getLogger('barber')
    logger.setLevel(level)

    if ARGS.debug:
        fh = logging.FileHandler(filename=f"barber.{dt.now().timestamp()}.log")
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

    logger.info("Barber parameters:")
    for k in vars(ARGS).keys():
        val = getattr(ARGS, k, "Information Unavailable")
        reprk = str(k).ljust(20, " ")
        logger.info(f"\t{reprk}: {val}")

    logger.info(f"Getting Data from MS file: {ARGS.ms}")

    if not os.path.exists(ARGS.ms):
        raise RuntimeError(f"Measurement set {ARGS.ms} not found")

    ant1, ant2, u_arr, v_arr, w_arr, raw_vis = casa_read_ms(ARGS.ms, ARGS.field)

    absvis = np.abs(raw_vis)
    max_index = np.unravel_index(np.argmax(absvis, axis=None), shape=absvis.shape)

    max_vis = np.max(absvis)
    p05, p50, p95, p99 = np.percentile(absvis, [5, 50, 95, 99])

    print("Max Vis Report")
    print(f"    Max Vis = {max_vis}")
    print(f"    Index = {max_index}")
    print(f"    vis percentiles (n={absvis.shape[0]}):")
    print(f"        5%={p05 :5.2f}")
    print(f"        50%={p50 :5.2f}")
    print(f"        95%={p95:5.2f}")
    print(f"        99%={p99:5.2f}")
    print(f"    ANT1 = {ant1[max_index[0]]}")
    print(f"    ANT2 = {ant2[max_index[0]]}")
    print(f"    u = {u_arr[max_index[0]]}")
    print(f"    v = {v_arr[max_index[0]]}")
    print(f"    w = {w_arr[max_index[0]]}")