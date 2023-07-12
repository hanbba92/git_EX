import numpy as np

def vector_conv_sameshape(arr, filter):
    # 필터가 항상 3*3 크기라고 가정하고 패딩은 1로줌
    pad = 1
    # 리턴값은 2d 격자
    ret = np.zeros_like(arr[0])
    # 각 2d격자마다 패딩을 넣음
    arr = np.pad(arr, ((0,), (pad,), (pad,)),mode='reflect')
    # 바람성분을 하나의 벡터로 보기위해 가장 끝으로 뺌
    arr = np.moveaxis(arr, 0, 2)
    y, x, n = arr.shape
    # 각 moving window의 모양
    sub_shape = (3,3,3)
    # 결과로 나올 배열의 모양. (y-2, x-2, 3,3,3)
    view_shape = (y-2, x-2, *sub_shape)
    # 바이트 단위의 보폭
    strides = arr.strides[:2]+arr.strides
    sub_matrices = np.lib.stride_tricks.as_strided(arr, view_shape, strides)
    # submatrices의 배열을 구해서 여기에 filter를 적용한다.
    m = np.einsum('ij,abijk->abk', filter, sub_matrices)
    # 벡터의 크기를 구한다.
    ret = np.linalg.norm(m, axis=2)
    return ret


