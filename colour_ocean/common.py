#!/usr/bin/env python
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
__copyright__ = 'Copyright (C) 2013-2017 - Colour Developers'
__license__ = 'New BSD License - http://opensource.org/licenses/BSD-3-Clause'
__maintainer__ = 'Colour Developers'
__email__ = 'colour-science@googlegroups.com'
__status__ = 'Production'

__all__ = ['replace', 'write_spds']


def replace(string, data):
    for old, new in data.items():
        string = string.replace(old, new)
    return string


def write_spds(spds, directory, unit_conversion):
    not os.path.exists(directory) and os.makedirs(directory)

    for name, spd in spds.items():
        wl, values = spd.wavelengths * unit_conversion, spd.values
        spd = colour.SpectralPowerDistribution(
            dict(zip(wl, values)), name=name)
        name = re.sub(r'\\|/', '', name)
        colour.write_spds_to_csv_file({
            name: spd
        }, os.path.join(directory, '{0}.csv'.format(name)))
