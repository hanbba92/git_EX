import numpy as np

def vector_conv_sameshape(arr, filter):
    pad = 1
    ret = np.zeros_like(arr[0])

    arr = np.pad(arr, ((0,), (pad,), (pad,)),mode='reflect')
    arr = np.moveaxis(arr, 0, 2)
    y, x, n = arr.shape
    sub_shape = (3,3,3)
    view_shape = (y-2, x-2, *sub_shape)
    strides = arr.strides[:2]+arr.strides
    sub_matrices = np.lib.stride_tricks.as_strided(arr, view_shape, strides)
    m = np.einsum('ij,abijk->abk', filter, sub_matrices)
    ret = np.linalg.norm(m, axis=2)
    return ret


