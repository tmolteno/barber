'''
    Read data from a measurement set.
    Author: Tim Molteno, tim@elec.ac.nz
    Copyright (c) 2019-2024.

    License. GPLv3.
'''

import logging
import numpy as np

from casacore.tables import table

logger = logging.getLogger(__name__)


def read_ms(ms_file, field_id=0, bl_max=9e99, uncorrected=True, pol=None):

    ms = table(ms_file, ack=False)

    logger.debug(f"colnames{ms.colnames()}")
    logger.debug(f"keywordnames{ms.keywordnames()}")
    logger.debug(f"fields{ms.fieldnames()}")

    ant = table(ms.getkeyword("ANTENNA"), ack=False)
    ant_p = ant.getcol("POSITION")
    logger.debug("Antenna Positions {}".format(ant_p.shape))

    # Now use TAQL to select only good data from the correct field
    subt = ms.query(f"FIELD_ID=={field_id}",
                    sortlist="ARRAY_ID", columns="TIME, DATA, UVW, ANTENNA1, ANTENNA2, FLAG")

    fields = table(subt.getkeyword("FIELD"), ack=False)
    # field columns ['DELAY_DIR', 'PHASE_DIR', 'REFERENCE_DIR', 'CODE', 'FLAG_ROW', 'NAME', 'NUM_POLY', 'SOURCE_ID', 'TIME']
    phase_dir = fields.getcol("PHASE_DIR")[field_id][0]
    name = fields.getcol("NAME")[field_id]
    field_time = fields.getcol("TIME")[field_id]
    print(f"Field {name} (index {field_id}): Phase Dir {np.degrees(phase_dir)}, t={field_time}")

    times = subt.getcol("TIME")
    logger.debug(f"times {times.shape}")
    time_steps, inverse = np.unique(times, return_inverse=True)
    logger.debug(f"time_steps {time_steps - time_steps[0]}")
    logger.debug(f"inverse {inverse}")

    uvw = subt.getcol("UVW")
    logger.debug(f"uvw {uvw.shape}")

    ant1 = subt.getcol("ANTENNA1")
    ant2 = subt.getcol("ANTENNA2")
    logger.debug(f"ant = {ant1.shape}")

    flags = subt.getcol("FLAG")
    logger.debug(f"flags = {flags.shape}")

    raw_vis = subt.getcol("DATA")

    def get_all(_x):
        if pol is None:
            return _x[:, :, :]
        else:
            return _x[:, :, pol]

    raw_vis = get_all(raw_vis)
    flags = get_all(flags)

    uvw = uvw[:, :]
    logger.debug("uvw {}".format(uvw.shape))
    ant1 = ant1[:]
    ant2 = ant2[:]

    # Create datasets representing each row of the spw table
    spw = table(ms.getkeyword("SPECTRAL_WINDOW"), ack=False)
    logger.debug(spw.colnames())

    frequencies = spw.getcol("CHAN_FREQ")[0]

    logger.debug(f"Frequencies = {frequencies.shape}")
    logger.debug(f"NUM_CHAN = {np.array(spw.NUM_CHAN[0])}")



    ms.close()




    logger.debug("Flags: {}".format(flags.shape))

    # Now report the recommended resolution from the data.
    # 1.0 / 2*np.sin(theta) = limit_u
    limit_uvw = np.max(np.abs(uvw), 0)

    # bl = np.sqrt(uvw[:, 0] ** 2 + uvw[:, 1] ** 2 + uvw[:, 2] ** 2)
    good_data = np.transpose(np.nonzero(flags))
    logger.debug(f"Indices {good_data.shape}")

    logger.debug("Maximum UVW: {}".format(limit_uvw))
    logger.debug("Minimum UVW: {}".format(np.min(np.abs(uvw), 0)))

    for i in range(3):
        p05, p50, p95 = np.percentile(np.abs(uvw[:, i]), [5, 50, 95])
        logger.debug(
            "       U[{}]: {:5.2f} {:5.2f} {:5.2f}".format(i, p05, p50, p95)
        )

    good_dumps = good_data[:,0]
    logger.debug(f"Good Dumps {good_dumps.shape}")
    #
    #   Now read the remaining data
    #
    ant1 = ant1
    ant2 = ant2

    logger.debug(f"Raw Vis {raw_vis.shape}")

    u_arr = uvw[:, 0]
    v_arr = uvw[:, 1]
    w_arr = uvw[:, 2]
    logger.debug(f"u_arr {u_arr.shape}")

    # return ant_p, ant1, ant2, u_arr, v_arr, w_arr, frequencies, raw_vis, corrected_vis, seconds, rms_arr
    return ant1, ant2, u_arr, v_arr, w_arr, raw_vis, flags, times, inverse
