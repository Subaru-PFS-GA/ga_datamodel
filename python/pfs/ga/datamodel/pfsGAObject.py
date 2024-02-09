import numpy as np

from pfs.datamodel.notes import makeNotesClass, Notes
from pfs.datamodel import PfsFiberArray
from pfs.datamodel import PfsTable, Column
from pfs.datamodel.utils import inheritDocstrings


__all__ = [
    "PfsGAObject"
]

PfsGAObjectNotes = makeNotesClass(
    "PfsGAObjectNotes",
    []
)

@inheritDocstrings
class PfsGAObject(PfsFiberArray):
    """Coadded spectrum of a GA target with derived quantities"""

    filenameFormat = ("pfsGAObject-%(catId)05d-%(tract)05d-%(patch)s-%(objId)016x"
                      "-%(nVisit)03d-0x%(pfsVisitHash)016x.fits")
    filenameRegex = r"^pfsGAObject-(\d{5})-(\d{5})-(.*)-([0-9a-f]{16})-(\d{3})-0x([0-9a-f]{16})\.fits.*$"
    filenameKeys = [("catId", int), ("tract", int), ("patch", str), ("objId", int),
                    ("nVisit", int), ("pfsVisitHash", int)]
    NotesClass = PfsGAObjectNotes

    def __init__(
        self,
        target,
        observations,
        wavelength,
        flux,
        mask,
        sky,
        covar,
        covar2,
        flags,
        metadata=None,
        fluxTable=None,
        velocityMeasurements=None,
        abundanceMeasurements=None,
        notes: Notes = None,
    ):
        # TODO: write parameters for there once settled on the member list
        self.paramCovar = None
        self.abundCovar = None

        super().__init__(target, observations, wavelength, flux, mask, sky, covar, covar2, flags, metadata=metadata, fluxTable=fluxTable, notes=notes)




