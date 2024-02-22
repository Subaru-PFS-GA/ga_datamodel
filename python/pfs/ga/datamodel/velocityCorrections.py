import numpy as np

from pfs.datamodel import PfsTable, Column

class VelocityCorrections(PfsTable):
    damdVer = 2
    schema = [
        Column("visit", np.int32, "ID of the visit these corrections apply for", -1),
        Column("JD", np.float32, "Julian date of the visit", -1),
        Column("helio", np.float32, "Heliocentric correction", np.nan),
        Column("bary", np.float32, "Barycentric correction", np.nan),
    ]
    fitsExtName = 'VELCORR'