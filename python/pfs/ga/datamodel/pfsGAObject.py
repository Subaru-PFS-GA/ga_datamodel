import numpy as np

from pfs.datamodel.notes import makeNotesClass, Notes
from pfs.datamodel import PfsFiberArray
from pfs.datamodel import PfsTable, Column
from pfs.datamodel.utils import inheritDocstrings

from .gaFluxTable import GAFluxTable
from .abundances import Abundances
from .stellarParams import StellarParams
from .velocityCorrections import VelocityCorrections

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
    FluxTableClass = GAFluxTable

    StellarParamsFitsExtName = "STELLARCOVAR"
    AbundancesFitsExtName = "ABUNDCOVAR"

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
        stellarParams=None,
        velocityCorrections=None,
        abundances=None,
        paramsCovar=None,
        abundCovar=None,
        notes: Notes = None,
    ):
        super().__init__(target, observations, wavelength, flux, mask, sky, covar, covar2, flags, metadata=metadata, fluxTable=fluxTable, notes=notes)

        self.stellarParams = stellarParams
        self.velocityCorrections = velocityCorrections
        self.abundances = abundances
        self.paramsCovar = paramsCovar
        self.abundCovar = abundCovar

    def validate(self):
        """Validate that all the arrays are of the expected shape"""
        super().validate()

        # TODO: write any validation code

    @classmethod
    def _readImpl(cls, fits):
        data = super()._readImpl(fits)

        data["stellarParams"] = StellarParams.readHdu(fits)
        data["velocityCorrections"] = VelocityCorrections.readHdu(fits)
        data["abundances"] = Abundances.readHdu(fits)
        if cls.StellarParamsFitsExtName in fits:
            data["paramsCovar"] = fits[cls.StellarParamsFitsExtName].data.astype(np.float32)
        if cls.AbundancesFitsExtName in fits:
            data["abundCovar"] = fits[cls.AbundancesFitsExtName].data.astype(np.float32)

        return data

    def _writeImpl(self, fits):
        from astropy.io.fits import ImageHDU

        header = super()._writeImpl(fits)

        self.stellarParams.writeHdu(fits)
        self.velocityCorrections.writeHdu(fits)
        self.abundances.writeHdu(fits)
        if self.paramsCovar is not None:
            fits.append(ImageHDU(self.paramsCovar.astype(np.float32), header=header, name=self.StellarParamsFitsExtName))
        if self.abundCovar is not None:
            fits.append(ImageHDU(self.abundCovar.astype(np.float32), header=header, name=self.AbundancesFitsExtName))

        return header