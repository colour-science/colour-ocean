# -*- coding: utf-8 -*-
"""
Export Colour Dataset
=====================

Exports *Colour* datasets for "Eclat Digital - Ocean" renderer.
"""

import codecs
import os

import colour
from colour.characterisation.datasets.displays.crt import (
    CRT_DISPLAYS_RGB_PRIMARIES)
from colour.characterisation.datasets.displays.lcd import (
    LCD_DISPLAYS_RGB_PRIMARIES)
from colour.characterisation.datasets.cameras.dslr import (
    DSLR_CAMERAS_RGB_SPECTRAL_SENSITIVITIES)
from colour_ocean.common import write_sds

__author__ = 'Colour Developers'
__copyright__ = 'Copyright (C) 2013-2021 - Colour Developers'
__license__ = 'New BSD License - https://opensource.org/licenses/BSD-3-Clause'
__maintainer__ = 'Colour Developers'
__email__ = 'colour-developers@colour-science.org'
__status__ = 'Production'

__all__ = [
    'BIBLIOGRAPHY', 'OUTPUT_DIRECTORY', 'export_csv_dataset',
    'write_bibliography'
]

BIBLIOGRAPHY = """BIBLIOGRAPHY
============

ILLUMINANTS
-----------

- CIE. (n.d.). CIE Spectral Data. Retrieved from http://files.cie.co.at/204.xls
- CIE. (n.d.). CIE 15:2004 Tables Data. Retrieved from https://law.resource.org/pub/us/cfr/ibr/003/cie.15.2004.tables.xls
- Digital Cinema Initiatives. (2007). Digital Cinema System Specification - Version 1.1. Retrieved from http://www.dcimovies.com/archives/spec_v1_1/DCI_DCinema_System_Spec_v1_1.pdf

LIGHT SOURCES
-------------

- Pointer, M. R. (1980). Pointer's Gamut Data. Retrieved from http://www.cis.rit.edu/research/mcsl2/online/PointerData.xls
- Ohno, Y., & Davis, W. (2008). NIST CQS simulation 7.4. Retrieved from http://cie2.nist.gov/TC1-69/NIST CQS simulation 7.4.xls

CAMERAS
-------

- Darrodi, M. M., Finlayson, G., Goodman, T., & Mackiewicz, M. (2015). Reference data set for camera spectral sensitivity estimation. Journal of the Optical Society of America A, 32(3), 381. doi:10.1364/JOSAA.32.000381

COLOUR MATCHING FUNCTIONS
-------------------------

- CVRL. (n.d.). Cone Fundamentals. Retrieved June 23, 2014, from http://www.cvrl.org/cones.htm
- Broadbent, A. D. (2009). Calculation from the original experimental data of the CIE 1931 RGB standard observer spectral chromaticity co-ordinates and color matching functions. Retrieved June 12, 2014, from http://www.cis.rit.edu/mcsl/research/1931.php
- CVRL. (n.d.). Stiles & Burch individual 10-deg colour matching data. Retrieved February 24, 2014, from http://www.cvrl.org/stilesburch10_ind.htm
- CVRL. (n.d.). Stiles & Burch individual 2-deg colour matching data. Retrieved February 24, 2014, from http://www.cvrl.org/stilesburch2_ind.htm
- CVRL. (n.d.). Older CIE Standards. Retrieved February 24, 2014, from http://cvrl.ioo.ucl.ac.uk/cie.htm
- CVRL. (n.d.). New CIE XYZ functions transformed from the CIE (2006) LMS functions. Retrieved February 24, 2014, from http://cvrl.ioo.ucl.ac.uk/ciexyzpr.htm

COLOUR CHECKERS
---------------

- Ohta, N. (1997). The basis of color reproduction engineering.
- Munsell Color Science. (n.d.). Macbeth Colorchecker. Retrieved from http://www.rit-mcsl.org/UsefulData/MacbethColorChecker.xls
- BabelColor. (2012). ColorChecker RGB and spectra. Retrieved from http://www.babelcolor.com/download/ColorChecker_RGB_and_spectra.xls
- BabelColor. (2012). The ColorChecker (since 1976!). Retrieved September 26, 2014, from http://www.babelcolor.com/main_level/ColorChecker.htm

COLOUR QUALITY
--------------

- Ohno, Y., & Davis, W. (2008). NIST CQS simulation 7.4. Retrieved from http://cie2.nist.gov/TC1-69/NIST CQS simulation 7.4.xls

DISPLAYS
--------

- Machado, G. (2010). A model for simulation of color vision deficiency and a color contrast enhancement technique for dichromats. Retrieved from http://www.lume.ufrgs.br/handle/10183/26950
"""

OUTPUT_DIRECTORY = os.path.join(os.path.dirname(__file__), 'csv', 'colour')


def export_csv_dataset(directory=OUTPUT_DIRECTORY, dataset='all'):
    if dataset in ('all', 'illuminants'):
        output_directory = os.path.join(directory, 'illuminants')
        write_sds(
            colour.ILLUMINANTS_SDS, output_directory, unit_conversion=1e-9)

    if dataset in ('all', 'light_sources'):
        output_directory = os.path.join(directory, 'light_sources')
        write_sds(
            colour.LIGHT_SOURCES_SDS, output_directory, unit_conversion=1e-9)

    if dataset in ('all', 'cmfs'):
        base_output_directory = os.path.join(directory, 'cmfs')
        for name, cmfs in colour.CMFS.items():
            if name in ('cie_2_1931', 'cie_10_1964'):
                continue

            output_directory = os.path.join(base_output_directory, name)
            for channel in cmfs.labels:
                write_sds(
                    {
                        channel: cmfs.signals[channel]
                    },
                    output_directory,
                    unit_conversion=1e-9)

    if dataset in ('all', 'characterisation'):
        base_output_directory = os.path.join(directory, 'characterisation',
                                             'colour_checkers')
        for name, colour_checker in colour.COLOURCHECKERS_SDS.items():
            if name in ('babel_average', 'cc_ohta'):
                continue

            output_directory = os.path.join(base_output_directory, name)
            write_sds(colour_checker, output_directory, unit_conversion=1e-9)

        base_output_directory = os.path.join(directory, 'characterisation',
                                             'cameras', 'dslr')
        for name, dslr in DSLR_CAMERAS_RGB_SPECTRAL_SENSITIVITIES.items():
            output_directory = os.path.join(base_output_directory, name)
            for channel in dslr.labels:
                write_sds(
                    {
                        channel: dslr.signals[channel]
                    },
                    output_directory,
                    unit_conversion=1e-9)

        base_output_directory = os.path.join(directory, 'characterisation',
                                             'displays', 'crt')
        for name, crt in CRT_DISPLAYS_RGB_PRIMARIES.items():
            output_directory = os.path.join(base_output_directory, name)
            for channel in crt.labels:
                write_sds(
                    {
                        channel: crt.signals[channel]
                    },
                    output_directory,
                    unit_conversion=1e-9)

        base_output_directory = os.path.join(directory, 'characterisation',
                                             'displays', 'lcd')
        for name, lcd in LCD_DISPLAYS_RGB_PRIMARIES.items():
            output_directory = os.path.join(base_output_directory, name)
            for channel in lcd.labels:
                write_sds(
                    {
                        channel: lcd.signals[channel]
                    },
                    output_directory,
                    unit_conversion=1e-9)

    if dataset in ('all', 'quality'):
        output_directory = os.path.join(directory, 'quality', 'TCS')
        write_sds(
            colour.quality.TCS_SDS, output_directory, unit_conversion=1e-9)
        output_directory = os.path.join(directory, 'quality', 'VS',
                                        'NIST CQS 7.4')
        write_sds(
            colour.quality.VS_SDS['NIST CQS 7.4'],
            output_directory,
            unit_conversion=1e-9)
        output_directory = os.path.join(directory, 'quality', 'VS',
                                        'NIST CQS 9.0')
        write_sds(
            colour.quality.VS_SDS['NIST CQS 9.0'],
            output_directory,
            unit_conversion=1e-9)


def write_bibliography(directory=OUTPUT_DIRECTORY):
    not os.path.exists(directory) and os.makedirs(directory)

    path = os.path.join(directory, 'BIBLIOGRAPHY.rst')
    with codecs.open(path, 'w', encoding='utf-8') as file:
        file.write(BIBLIOGRAPHY)


if __name__ == '__main__':
    export_csv_dataset()
    write_bibliography()
