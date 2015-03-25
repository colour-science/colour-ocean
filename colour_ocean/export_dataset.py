#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Export Dataset
==============

Exports *Colour* dataset for "Eclat Digital - Ocean" renderer.
"""

import codecs
import os
import re

import colour

__author__ = 'Colour Developers'
__copyright__ = 'Copyright (C) 2013 - 2015 - Colour Developers'
__license__ = 'New BSD License - http://opensource.org/licenses/BSD-3-Clause'
__maintainer__ = 'Colour Developers'
__email__ = 'colour-science@googlegroups.com'
__status__ = 'Production'

__all__ = ['BIBLIOGRAPHY',
           'DEFAULT_DIRECTORY',
           'write_spds',
           'export_csv_dataset',
           'write_bibliography']

BIBLIOGRAPHY = """BIBLIOGRAPHY
============

ILLUMINANTS
-----------

- CIE. (n.d.). CIE Spectral Data. Retrieved from http://files.cie.co.at/204.xls
- CIE. (n.d.). CIE 15:2004 Tables Data. Retrieved from https://law.resource.org/pub/us/cfr/ibr/003/cie.15.2004.tables.xls
- Digital Cinema Initiatives. (2007). Digital Cinema System Specification - Version 1.1. Retrieved from http://www.dcimovies.com/archives/spec_v1_1/DCI_DCinema_System_Spec_v1_1.pdf

LIGHT SOURCES
-------------

- Pointer, M. R. (1980). Pointer’s Gamut Data. Retrieved from http://www.cis.rit.edu/research/mcsl2/online/PointerData.xls
- Ohno, Y., & Davis, W. (2008). NIST CQS simulation 7.4. Retrieved from http://cie2.nist.gov/TC1-69/NIST CQS simulation 7.4.xls

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
"""

DEFAULT_DIRECTORY = os.path.join(os.path.dirname(__file__), 'csv')


def write_spds(spds, directory):
    not os.path.exists(directory) and os.makedirs(directory)

    for name, spd in spds.items():
        wl, values = spd.wavelengths * 1e-9, spd.values
        spd = colour.SpectralPowerDistribution(name,
                                               dict(zip(wl, values)))
        name = re.sub(r'[^a-zA-Z0-9_\-\.\(\)]', '-', name)
        colour.write_spds_to_csv_file({name: spd},
                                      os.path.join(directory,
                                                   '{0}.csv'.format(name)))


def export_csv_dataset(directory=DEFAULT_DIRECTORY, dataset='all'):
    if dataset in ('all', 'illuminants'):
        output_directory = os.path.join(directory, 'illuminants')
        write_spds(colour.ILLUMINANTS_RELATIVE_SPDS, output_directory)

    if dataset in ('all', 'light_sources'):
        output_directory = os.path.join(directory, 'light_sources')
        write_spds(colour.LIGHT_SOURCES_RELATIVE_SPDS, output_directory)

    if dataset in ('all', 'cmfs'):
        base_output_directory = os.path.join(directory, 'cmfs')
        for name, cmfs in colour.CMFS.items():
            if name in ('cie_2_1931', 'cie_10_1964'):
                continue

            output_directory = os.path.join(base_output_directory, name)

            for channel in ('x', 'y', 'z'):
                write_spds({cmfs.mapping[channel]: getattr(cmfs, channel)},
                           output_directory)

    if dataset in ('all', 'characterisation'):
        base_output_directory = os.path.join(directory,
                                             'characterisation',
                                             'colour_checkers')
        for name, colour_checker in colour.COLOURCHECKERS_SPDS.items():
            if name in ('babel_average', 'cc_ohta'):
                continue

            output_directory = os.path.join(base_output_directory, name)

            write_spds(colour_checker, output_directory)

    if dataset in ('all', 'quality'):
        output_directory = os.path.join(directory, 'quality', 'TCS')
        write_spds(colour.TCS_SPDS, output_directory)
        output_directory = os.path.join(directory, 'quality', 'VS')
        write_spds(colour.VS_SPDS, output_directory)


def write_bibliography(directory=DEFAULT_DIRECTORY):
    not os.path.exists(directory) and os.makedirs(directory)

    path = os.path.join(directory, 'BIBLIOGRAPHY.rst')
    with codecs.open(path, 'w', encoding='utf-8') as file:
        file.write(BIBLIOGRAPHY)


if __name__ == '__main__':
    export_csv_dataset()
    write_bibliography()