import re
import numpy as np
from unittest import TestCase

from pfs.datamodel import Target, TargetType
from pfs.datamodel import Observations
from pfs.datamodel import MaskHelper
from pfs.datamodel import FluxTable
from pfs.ga.datamodel import PfsGAObject, StellarParams, Abundances, Velocities, VelocityCorrections

class PfsGAObjectTestCase(TestCase):
    """ Check the format of example datamodel files are
        consistent with that specified in the corresponding
        datamodel classes.
    """

    def extractAttributes(self, cls, fileName):
        matches = re.search(cls.filenameRegex, fileName)
        if not matches:
            self.fail(
                "Unable to parse filename: {} using regex {}"
                .format(fileName, cls.filenameRegex))

        # Cannot use algorithm in PfsSpectra._parseFilename(),
        # specifically cls.filenameKeys, due to ambiguity in parsing
        # integers in hex format (eg objId). Need to parse cls.filenameFormat
        ff = re.search(r'^[a-zA-Z]+(.*)\.fits', cls.filenameFormat)[1]
        cmps = re.findall(r'-{0,1}(0x){0,1}\%\((\w+)\)\d*(\w)', ff)
        fmts = [(kk, tt) for ox, kk, tt in cmps]

        d = {}
        for (kk, tt), vv in zip(fmts, matches.groups()):
            if tt == 'd':
                ii = int(vv)
            elif tt == 'x':
                ii = int(vv, 16)
            elif tt == 's':
                ii = vv
            d[kk] = ii
        return d
    
    def test_FilenameRegex(self):
        d = self.extractAttributes(
                PfsGAObject,
                'pfsGAObject-07621-01234-2,2-02468ace1234abcd-003-0x0123456789abcdef.fits')
        self.assertEqual(d['catId'], 7621)
        self.assertEqual(d['tract'], 1234)
        self.assertEqual(d['patch'], '2,2')
        self.assertEqual(d['objId'], 163971054118939597)
        self.assertEqual(d['nVisit'], 3)
        self.assertEqual(d['pfsVisitHash'], 81985529216486895)

    def test_Write(self):
        """Construct a PfsGAObject and save it to a FITS file."""

        catId = 12345
        tract = 1
        patch = '1,1'
        objId = 123456789
        ra = -100.63654
        dec = -68.591576
        targetType = TargetType.SCIENCE

        target = Target(catId, tract, patch, objId, ra, dec, targetType)

        visit = np.array([ 83219, 83219 ])
        arm = np.array([ 'b', 'm', ])
        spectrograph = np.array([1, 1])
        pfsDesignId = np.array([8854764194165386399, 8854764194165386399])
        fiberId = np.array([476, 476])
        pfiNominal = np.array([[ra, dec], [ra, dec]])
        pfiCenter = np.array([[ra, dec], [ra, dec]])

        observations = Observations(visit, arm, spectrograph, pfsDesignId, fiberId, pfiNominal, pfiCenter)

        npix = 4096
        wavelength = np.concatenate([
            np.linspace(380, 650, npix, dtype=np.float32),
            np.linspace(710, 885, npix, dtype=np.float32)
        ])
        flux = np.zeros_like(wavelength)
        error = np.zeros_like(wavelength)
        mask = np.zeros_like(wavelength, dtype=np.int32)
        sky = np.zeros_like(wavelength)
        covar = np.zeros((3, wavelength.size), dtype=np.float32)    # Tridiagonal covariance matrix of flux
        covar2 = np.zeros((1, 1), dtype=np.float32)                 # ?

        flags = MaskHelper() # {'BAD': 0, 'BAD_FIBERTRACE': 11, 'BAD_FLAT': 9, 'BAD_FLUXCAL': 13, 'BAD_SKY': 12, 'CR': 3, 'DETECTED': 5, 'DETECTED_NEGATIVE': 6, 'EDGE': 4, 'FIBERTRACE': 10, 'INTRP': 2, 'IPC': 14, 'NO_DATA': 8, 'REFLINE': 15, 'SAT': 1, 'SUSPECT': 7, 'UNMASKEDNAN': 16})
        metadata = {}                                               # Key-value pairs to put in the header

        fluxTable = FluxTable(wavelength, flux, error, mask, flags)

        velocities = Velocities(
            method=np.array([]),
            frame=np.array([]),
            unit=np.array([]),
            value=np.array([]),
            valueErr=np.array([]),
            flag=np.array([]),
            status=np.array([]),
        )

        abundances = Abundances(
            method=np.array([]),
            element=np.array([]),
            value=np.array([]),
            valueErr=np.array([]),
        )

        pfsGAObject = PfsGAObject(target, observations,
                                  wavelength, flux, mask, sky, covar, covar2,
                                  flags, metadata,
                                  fluxTable,
                                  velocities,
                                  abundances)

        pfsGAObject.writeFits('/home/dobos/project/ga_datamodel/temp/pfsGAObject.fits')

    def test_Read(self):
        pass