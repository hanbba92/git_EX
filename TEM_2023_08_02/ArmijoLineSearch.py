import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from itertools import product
from geomdl import operations
def ArmijoLineSearch(f,surf, xk, pk, gfk, phi0, alpha0, rho=0.5, c1=1e-4):
    """Minimize over alpha, the function ''f(x_k + ap_k)''.
    a > 0 is assumed to be a descent direction.

    Parameters
    --------------------------
    f : callable
        function to be minimized.
    xk : array
        Current point.
    pk : array
        Search direction
    gfk : array
        Gradient of 'f' at point 'xk'.
    phi0 : float
        Value of 'f' at point 'xk'.
    alpha0 : scalar
        Value of 'alpha' at the start of the optimization.
    rho : float, optional
        Value of alpha shrinkage factor.
    c1 : float, optional
        Value oto control stopping criterion.

    Returns

    ------------------
    alpha : scalar
        Value of 'alpha' at the end of the optimization.
    phi: float
        Value of 'f' at the new point 'x_{k+1}'.
        """
    deriphi0 = np.dot(gfk, pk)
    q=xk+alpha0*pk
    if q[0] < 0 or q[1] < 0 or q[0] > 1 or q[1] >1:
        return alpha0, phi0
    print(q)
    tan=operations.tangent(surf,list(q))
    phi_a0 = tan[0][2]
    prev_a0=phi_a0
    print(f"iy= {tan[0][0]}, ix = {tan[0][1]}, alpha0 = {alpha0} deriphi0 = {deriphi0}, pk= {pk}, phi_a0 = {phi_a0}, phi0= {phi0}")
    count=0
    while not abs(phi_a0) <= abs(phi0 + c1*alpha0*deriphi0):
        q = xk + alpha0 * pk
        if q[0] < 0 or q[1] < 0 or q[0] > 1 or q[1] > 1:
            break
        alpha0=alpha0*rho

        tan=operations.tangent(surf,list(q))
        phi_a0=tan[0][2]
        if phi_a0 == prev_a0:
            break
        prev_a0=phi_a0

        print(f"alpha0 = {alpha0} deriphi0 = {deriphi0}, pk= {pk}, phi_a0 = {phi_a0}, phi0= {phi0}")


    return alpha0, phi_a0