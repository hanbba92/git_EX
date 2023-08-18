import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from itertools import product
from ArmijoLineSearch import *
import math
from geomdl import operations

def GradientDescent(f,surf, init, alpha=1, tol=1e-4, max_iter = 1000):
    """Gradient descent method for unconstraint optimization poblem.
    given a starting point x in R^n,
    repeat
        1. Define direction. p := -Gradient(f(x)).
        2. Line Search. Choose step length a using Armijo Line Search.
        3. Update. x := x + ap.
    until stopping criterion is satisfied.

    Parameters
    -------------------------
    f : callable
            Function to be minimized.
        f_grad : callable
            The first derivative of f.
        init : array
            initial value of x.
        alpha : scalar, optional
            the initial value of step length.
        tol : float, optional
            tolerance for the norm of f_grad.
        max_iter : integer, optional
            maximum number of steps.

    Returns
    -------------------------
    xs : array
        x in the learning path
    ys : array
        f(x) in the learning path
    """
    # initialize x, f(x), and f'(x)
    xk = init

    tan=operations.tangent(surf,list(xk))

    fk = tan[0][2]

    #f_threshold=np.median(f)-np.std(f)*0.5
    #print(np.std(f), np.median(f), f_threshold)
    gfk = np.array([tan[1][2],tan[2][2]])
    gfk_norm = np.linalg.norm(gfk)


    #initialize number of steps, save x and f(x)
    num_iter = 0
    curve_x = [xk]
    curve_y = [fk]
    print('initial condition: y = {:.4f}, x = {} \n'.format(fk,xk))
    #take steps
    while gfk_norm > tol and num_iter < max_iter:
        #determine direction
        pk = -gfk
        # print(alpha*pk)


        alpha,fk=ArmijoLineSearch(f,surf,xk,pk,gfk,fk,alpha0=alpha)
        xk=xk+alpha*pk
        # if xk[0] < 0 or xk[1] < 0 or xk[0] > 1 or xk[1] >1:
        #     curve_x.append([int(tan[0][0]), int(tan[0][1])])
        #     curve_y.append(fk)
        #     return 0, 0, 0
        if xk[0] < 0 or xk[0] > 1 or xk[1] < 0 or xk[1] > 1:
            return 0, np.array(curve_x), np.array(curve_y)
        tan=operations.tangent(surf,list(xk))
        gfk = np.array([tan[1][2],tan[2][2]])
        gfk_norm = np.linalg.norm(gfk)
        # increase number of steps by 1, save new x and f(x)
        num_iter += 1
        curve_x.append([int(tan[0][0]),int(tan[0][1])])
        curve_y.append(fk)

        #print('Iteration: {} \t y = {:.4f}. x = {}, gradient = {:4f}'.format(num_iter, fk, xk, gfk_norm))


    #print results
    if num_iter == max_iter:
        print('\nGradient descent does not converge. gradient = {:4f}, pk = {}'.format(gfk_norm,xk))
        return 0, np.array(curve_x), np.array(curve_y)

    else:
        print('\nSolution: \t y = {:.4f}, x = {}'.format(fk, xk))
        return 1, np.array(curve_x), np.array(curve_y)
