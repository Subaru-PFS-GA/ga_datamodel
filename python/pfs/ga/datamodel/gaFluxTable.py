import numpy as np

from pfs.datamodel.utils import astropyHeaderToDict, astropyHeaderFromDict
from pfs.datamodel.masks import MaskHelper
from pfs.datamodel import FluxTable

__all__ = ["GAFluxTable"]


class GAFluxTable():
    # TODO: update docs

    """Table of coadded fluxes at near-original sampling and model fits

    Merged and coadded spectra have been resampled to a standard wavelength
    sampling. This representation provides coadded fluxes at approximately the
    native wavelength sampling, for those that want the data with a minimum of
    resampling. This is mostly of use for single exposures and coadds made from
    back-to-back exposures with the same top-end configuration. For coadds made
    from exposures with different top-end configurations, the different
    wavelength samplings obtained from the different fibers means there's no
    single native wavelength sampling, and so this is less useful.

    This is like a `pfs.datamodel.PfsSimpleSpectrum`, except that it includes a
    variance array, and is written to a FITS HDU rather than a file (so it can
    be incorporated within a `pfs.datamodel.PfsSpectrum`).

    Parameters
    ----------
    wavelength : `numpy.ndarray` of `float`
        Array of wavelengths.
    flux : `numpy.ndarray` of `float`
        Array of fluxes.
    error : `numpy.ndarray` of `float`
        Array of flux errors.
    norm : `numpy.ndarray` of `float`
        Array of continuum-normalized flux.
    norm_error : `numpy.ndarray` of `float`
        Array of continuum-normalized flux error.
    cont : `numpy.ndarray` of `float`
        Array of continuum model.
    mask : `numpy.ndarray` of `int`
        Array of mask pixels.
    flags : `pfs.datamodel.MaskHelper`
        Helper for dealing with symbolic names for mask values.
    """
    _hduName = "FLUX_TABLE"  # HDU name to use

    def __init__(self, wavelength, flux, error, norm, norm_error, cont, model, mask, flags):
        data = (wavelength, flux, error, norm, norm_error, cont, model, mask)
        dims = np.array([ len(d.shape) for d in data ])
        lengths = set([ d.shape for d in data ])
        if np.any(dims != 1) or len(lengths) > 1:
            raise RuntimeError("Bad shapes for wavelength,flux,error,norm,norm_error,cont,model,mask,: %s" %
                               ','.join([ d.shape for d in data ]))
        self.wavelength = wavelength
        self.flux = flux
        self.error = error
        self.norm = norm
        self.norm_error = norm_error
        self.cont = cont
        self.model = model
        self.mask = mask
        self.flags = flags

    def __len__(self):
        """Return number of elements"""
        return len(self.wavelength)
    
    def getFitsColumns(self):
        from astropy.io.fits import BinTableHDU, Column

        return [
            Column("wavelength", "D", array=self.wavelength),
            Column("flux", "E", array=self.flux),
            Column("error", "E", array=self.error),
            Column("norm", "E", array=self.norm),
            Column("norm_error", "E", array=self.norm_error),
            Column("cont", "E", array=self.cont),
            Column("model", "E", array=self.model),
            Column("mask", "K", array=self.mask),
        ]
    
    @classmethod
    def getFitsData(cls, hdu):
        return [
            hdu.data["wavelength"].astype(float),
            hdu.data["flux"].astype(np.float32),
            hdu.data["error"].astype(np.float32),
            hdu.data["norm"].astype(np.float32),
            hdu.data["norm_error"].astype(np.float32),
            hdu.data["cont"].astype(np.float32),
            hdu.data["model"].astype(np.float32),
            hdu.data["mask"].astype(np.int32),
        ]

    def toFits(self, fits):
        """Write to a FITS file

        Parameters
        ----------
        fits : `astropy.io.fits.HDUList`
            Opened FITS file.
        """
        # NOTE: When making any changes to this method that modify the output
        # format, increment the DAMD_VER header value and record the change in
        # the versions.txt file.
        from astropy.io.fits import BinTableHDU, Column
        header = astropyHeaderFromDict(self.flags.toFitsHeader())
        header['DAMD_VER'] = (1, "FluxTable datamodel version")
        hdu = BinTableHDU.from_columns(self.getFitsColumns(), header=header, name=self._hduName)
        fits.append(hdu)

    @classmethod
    def fromFits(cls, fits):
        """Construct from a FITS file

        Parameters
        ----------
        fits : `astropy.io.fits.HDUList`
            Opened FITS file.

        Returns
        -------
        self : `FluxTable`
            Constructed `FluxTable`.
        """

        hdu = fits[cls._hduName]
        header = astropyHeaderToDict(hdu.header)
        flags = MaskHelper.fromFitsHeader(header)
        return cls(*cls.getFitsData(hdu), flags)
