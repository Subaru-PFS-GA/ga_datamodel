import numpy as np

from pfs.datamodel import PfsTable, Column

class Velocities(PfsTable):
    damdVer = 2
    schema = [
        Column("method", str, "Line-of-sight velocity measurement method", ""),
        Column("frame", str, "Reference frame of velocity: helio, bary", ""),
        Column("unit", str, "Unit of velocity", ""),
        Column("value", np.float32, "Line-of-sight velocity", np.nan),
        Column("valueErr", np.float32, "Line-of-sight velocity error", np.nan),
        # TODO: add quantiles or similar for MCMC results
        Column("flag", bool, "Measurement flag (true means bad)", False),
        Column("status", str, "Measurement flags", ""),
    ]
    fitsExtName = 'VELOC'