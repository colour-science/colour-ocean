# -*- coding: utf-8 -*-
"""
Export Refractive Index Info Dataset
====================================

Exports *http://refractiveindex.info/* dataset for "Eclat Digital - Ocean"
renderer.
"""

import codecs
import numpy as np
import os
import yaml

import colour
from colour_ocean.common import replace, write_sds

__author__ = 'Colour Developers'
__copyright__ = 'Copyright (C) 2013-2019 - Colour Developers'
__license__ = 'New BSD License - https://opensource.org/licenses/BSD-3-Clause'
__maintainer__ = 'Colour Developers'
__email__ = 'colour-science@googlegroups.com'
__status__ = 'Production'

__all__ = [
    'OUTPUT_DIRECTORY', 'LIBRARY', 'export_csv_dataset', 'write_bibliography'
]

LIBRARY = os.path.join(
    os.path.dirname(__file__), 'resources', 'rii', 'database', 'library.yml')

OUTPUT_DIRECTORY = os.path.join(os.path.dirname(__file__), 'csv', 'rii')


def export_csv_dataset(directory=OUTPUT_DIRECTORY, library=LIBRARY):
    library_directory = os.path.dirname(library)
    shelves = yaml.load(codecs.open(LIBRARY, encoding='utf-8'))
    for shelf in shelves:
        shelf_name = shelf['name']
        for shelved in shelf['content']:
            if shelved.get('DIVIDER'):
                divider_name = shelved['DIVIDER']
            elif shelved.get('BOOK'):
                book_name = shelved['BOOK']
                for page in shelved['content']:
                    page_name = replace(page['PAGE'], {
                        'α': 'alpha',
                        'β': 'beta',
                        'γ': 'gamma'
                    })
                    path = os.path.join(library_directory, page['path'])
                    content = yaml.load(
                        codecs.open(path, encoding='utf-8', errors='ignore'))

                    output_directory = os.path.join(directory, shelf_name,
                                                    book_name, page_name)

                    data_type = (content['DATA'][0]['type'])
                    if data_type == 'tabulated nk':
                        data = np.array([
                            np.float_(x)
                            for x in content['DATA'][0]['data'].split()
                        ])
                        data = np.reshape(data, (-1, 3))
                        wavelengths = data[..., 0]
                        n = data[..., 1]
                        k = data[..., 2]

                        sds = {
                            'n':
                            colour.SpectralDistribution(
                                dict(zip(wavelengths, n)), name='n'),
                            'k':
                            colour.SpectralDistribution(
                                dict(zip(wavelengths, k)), name='k')
                        }

                        write_sds(
                            sds, output_directory, unit_conversion=1e-6)


if __name__ == '__main__':
    export_csv_dataset()
