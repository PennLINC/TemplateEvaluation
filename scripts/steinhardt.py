#!/usr/bin/env python
import nibabel as nb
import numpy as np
import sys

"""

The spherical harmonic coefficients are stored as follows. First, since the
signal attenuation profile is real, it has conjugate symmetry, i.e. Y(l,-m) =
Y(l,m)* (where * denotes the complex conjugate). Second, the diffusion profile
should be antipodally symmetric (i.e. S(x) = S(-x)), implying that all odd l
components should be zero. Therefore, only the even elements are computed. Note
that the spherical harmonics equations used here differ slightly from those
conventionally used, in that the (-1)^m factor has been omitted. This should be
taken into account in all subsequent calculations. Each volume in the output
image corresponds to a different spherical harmonic component.

Each volume will
correspond to the following:

volume 0: l = 0, m = 0 ;
volume 1: l = 2, m = -2 (imaginary part of m=2 SH) ;
volume 2: l = 2, m = -1 (imaginary part of m=1 SH)
volume 3: l = 2, m = 0 ;
volume 4: l = 2, m = 1 (real part of m=1 SH) ;
volume 5: l = 2, m = 2 (real part of m=2 SH) ; etc…


lmax = 2

vol	l	m
0	0	0
1	2	-2
2	2	-1
3	2	0
4	2	1
5	2	2




"""

def get_l_m(lmax):
    ell = []
    m = []
    for _ell in range(0, lmax + 1, 2):
        for _m in range(-_ell, _ell+1):
            ell.append(_ell)
            m.append(_m)

    return np.array(ell), np.array(m)

lmax_lut = {
    6: 2,
    15: 4,
    28: 6,
    45: 8
}

def calculate_steinhardt(sh_l, sh_m, data, q_num):
    l_mask = sh_l == q_num
    images = data[..., l_mask]
    scalar = 4 * np.pi / (2 * q_num + 1)
    s_param = scalar * np.sum(images ** 2, 3)
    return np.sqrt(s_param)

def order_params(nii_file):
    img = nb.load(nii_file)
    data = img.get_fdata()
    num_vols = data.shape[3]
    if not num_vols in lmax_lut:
        raise ValueError("Not an SH image")
    lmax = lmax_lut[num_vols]
    sh_l, sh_m = get_l_m(lmax)

    q2 = calculate_steinhardt(sh_l, sh_m, data, 2)
    q4 = calculate_steinhardt(sh_l, sh_m, data, 4)
    q6 = calculate_steinhardt(sh_l, sh_m, data, 6)
    q8 = calculate_steinhardt(sh_l, sh_m, data, 8)
    nb.Nifti1Image(q2, img.affine).to_filename(nii_file + "q2.nii.gz")
    nb.Nifti1Image(q4, img.affine).to_filename(nii_file + "q4.nii.gz")
    nb.Nifti1Image(q6, img.affine).to_filename(nii_file + "q6.nii.gz")
    nb.Nifti1Image(q8, img.affine).to_filename(nii_file + "q8.nii.gz")

from glob import glob
sh_niis = glob("normed_mifs/*nii.gz")
from tqdm import tqdm

for sh_nii in tqdm(sh_niis):
    order_params(sh_nii)





