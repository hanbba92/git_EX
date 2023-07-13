import numpy as np

def conv_sameshape(val, filter):
    pad = filter.shape[0]//2
    # 각 2d격자마다 패딩을 넣음
    arr = np.pad(val, pad,mode='reflect')
    # 바람성분을 하나의 벡터로 보기위해 가장 끝으로 뺌
    # 각 moving window의 모양
    sub_shape = (5,5)
    view_shape = tuple(np.subtract(arr.shape, sub_shape)+1) + sub_shape
    # 바이트 단위의 보폭
    strides = arr.strides+arr.strides
    sub_matrices = np.lib.stride_tricks.as_strided(arr, view_shape, strides)
    # submatrices의 배열을 구해서 여기에 filter를 적용한다.
    ret = np.einsum('ij,klij->kl', filter, sub_matrices)
    return ret


