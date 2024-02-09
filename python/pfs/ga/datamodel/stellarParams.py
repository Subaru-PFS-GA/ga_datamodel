import numpy as np

from pfs.datamodel import PfsTable, Column

class StellarParams(PfsTable):
    damdVer = 2
    schema = [
        Column("method", str, "Stellar parameter measurement method", ""),
        Column("param", str, "Stellar parameter: M_H, T_eff, log_g, a_M", ""),
        Column("paramId", str, "Param ID", -1),
        Column("unit", str, "Unit of the parameter", ""),
        Column("value", np.float32, "Stellar parameter value", np.nan),
        Column("valueErr", np.float32, "Stellar parameter error", np.nan),
        # TODO: add quantiles or similar for MCMC results
    ]

# TODO: velocity - stellar parameters full covariance matrix?