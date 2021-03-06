import os
import numpy as np
import pytest
import xrfac


THIS_DIR = os.path.abspath(os.path.dirname(__file__))


@pytest.mark.parametrize('files', [
    ('ne.lev', 'ne.lev.b'),
    ('ne.tr', 'ne.tr.b'),
    ('Ne03a.en', 'Ne03b.en'),  # 1.1.5
    ])
def test(files):
    ascii_file = THIS_DIR + '/example_data/' + files[0]
    binary_file = THIS_DIR + '/example_data/' + files[1]

    ds_from_ascii = xrfac.ascii.load(ascii_file)
    ds_from_binary = xrfac.binary.load(binary_file)
    for k in ds_from_ascii.variables:
        if ds_from_ascii[k].dtype.kind in 'iuf':
            assert np.allclose(ds_from_ascii[k], ds_from_binary[k])
        else:
            assert (ds_from_ascii[k] == ds_from_binary[k]).all()


def test_tr():
    tr_ascii_file = THIS_DIR + '/example_data/ne_multipole.tr'
    tr_bin_file = THIS_DIR + '/example_data/ne_multipole.tr.b'
    en_bin_file = THIS_DIR + '/example_data/ne.lev.b'

    ds_ascii = xrfac.ascii.load(tr_ascii_file)
    ds_bin = xrfac.binary.load(tr_bin_file)
    ds_bin_en = xrfac.binary.load(en_bin_file)

    ds_bin = xrfac.binary.oscillator_strength(ds_bin, ds_bin_en)
    for k in ds_ascii.variables:
        if ds_ascii[k].dtype.kind in 'iuf':
            assert np.allclose(ds_ascii[k], ds_bin[k])
        else:
            assert (ds_ascii[k] == ds_bin[k]).all()
