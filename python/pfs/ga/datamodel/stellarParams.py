import numpy as np

from pfs.datamodel import PfsTable, Column

class StellarParams(PfsTable):
    damdVer = 2
    schema = [
        Column("method", str, "Line-of-sight velocity measurement method", ""),
        Column("frame", str, "Reference frame of velocity: helio, bary", ""),
        Column("param", str, "Stellar parameter: v_los, M_H, T_eff, log_g, a_M", ""),
        Column("covarId", np.uint8, "Param position within covariance matrix", -1),
        Column("unit", str, "Physical unit of parameter", ""),
        Column("value", np.float32, "Stellar parameter value", np.nan),
        Column("valueErr", np.float32, "Stellar parameter error", np.nan),
        # TODO: add quantiles or similar for MCMC results
        Column("flag", bool, "Measurement flag (true means bad)", False),
        Column("status", str, "Measurement flags", ""),
    ]
    fitsExtName = 'STELLARPARAM'