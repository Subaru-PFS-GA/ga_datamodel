import numpy as np

from pfs.datamodel import PfsTable, Column

class Abundances(PfsTable):
    damdVer = 2
    schema = [
        Column("method", str, "Abundance measurement method", ""),
        Column("element", str, "Chemical element the abundance is measured for", ""),
        Column("value", np.float32, "Abundance value", np.nan),
        Column("valueErr", np.float32, "Abundance error", np.nan),
    ]
    fitsExtName = 'ABUND'

# TODO: abundance full covariance matrix?