# AUTOGENERATED! DO NOT EDIT! File to edit: ../notebooks/api/03_data.ipynb.

# %% auto 0
__all__ = ['read_dicom', 'load_example_ct']

# %% ../notebooks/api/03_data.ipynb 3
from pathlib import Path

import numpy as np
from pydicom import dcmread

# %% ../notebooks/api/03_data.ipynb 4
def read_dicom(dcmdir, correct_zero=True):
    """
    Inputs
    -----
    dcmdir : Path or str
        Path to a DICOM directory
    correct_zero : bool
        Make 0 the minimum value the CT
    Returns
    -------
    volume : ndarray
        3D array containing voxels of imaging data
    spacing : list
        X-, Y-, and Z-directional voxel spacings
    """

    dcmfiles = Path(dcmdir).glob("*.dcm")
    dcmfiles = list(dcmfiles)
    dcmfiles.sort()
    ds = dcmread(dcmfiles[0])

    nx, ny = ds.pixel_array.shape
    nz = len(dcmfiles)
    del_x, del_y = ds.PixelSpacing
    del_x, del_y = float(del_x), float(del_y)
    volume = np.zeros((nx, ny, nz)).astype(np.float32)

    del_zs = []
    for idx, dcm in enumerate(dcmfiles):
        ds = dcmread(dcm)
        volume[:, :, idx] = ds.pixel_array
        del_zs.append(ds.ImagePositionPatient[2])

    if correct_zero:
        volume[volume == volume.min()] = 0

    del_zs = np.diff(del_zs)
    del_z = float(np.abs(np.unique(del_zs)[0]))
    spacing = [del_x, del_y, del_z]

    return volume, spacing

# %% ../notebooks/api/03_data.ipynb 5
def load_example_ct():
    """Load an example chest CT for demonstration purposes."""
    currdir = Path(__file__).resolve().parent
    dcmdir = currdir / "data/cxr"
    return read_dicom(dcmdir)