# -*- coding: utf-8 -*-
"""
Common Utilities
================

Defines common utilities objects that don't fall in any specific category.
"""

import os
import re

import colour

__author__ = 'Colour Developers'
__copyright__ = 'Copyright (C) 2013-2019 - Colour Developers'
__license__ = 'New BSD License - http://opensource.org/licenses/BSD-3-Clause'
__maintainer__ = 'Colour Developers'
__email__ = 'colour-science@googlegroups.com'
__status__ = 'Production'

__all__ = ['replace', 'write_sds']


def replace(string, data):
    for old, new in data.items():
        string = string.replace(old, new)
    return string


def write_sds(sds, directory, unit_conversion):
    not os.path.exists(directory) and os.makedirs(directory)

    for name, sd in sds.items():
        wl, values = sd.wavelengths * unit_conversion, sd.values
        sd = colour.SpectralDistribution(
            dict(zip(wl, values)), name=name)
        name = re.sub(r'\\|/', '', name)
        colour.write_sds_to_csv_file({
            name: sd
        }, os.path.join(directory, '{0}.csv'.format(name)))
