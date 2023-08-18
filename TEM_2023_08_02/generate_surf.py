from GradientDescent import *
from plot import *
import os
from netCDF4 import Dataset
from geomdl import operations
from geomdl import BSpline
from geomdl import control_points
import sys
import numpy as np
from geomdl.visualization import VisMPL as mpl

def generate_surf(u,v,p):

    ctr = np.c_[v, u, p]
    # surf.set_ctrlpts(ctr, 419,491)

    size_u = 419
    size_v = 491
    # Number of control points in all parametric dimensions

    # Create control points manager
    points = control_points.SurfaceManager(size_u, size_v)

    # Set control points
    for u in range(size_u):
        for v in range(size_v):
            # 'pt' is the control point, e.g. [10, 15, 12]
            points.set_ctrlpt(list(ctr[491 * u + v]), u, v)

    # # Create spline geometry
    # Create spline geometry
    surf = BSpline.Surface()

    # Set control points
    surf.degree_v = 3
    surf.degree_u = 3
    surf.ctrlpts_size_u = size_u
    surf.ctrlpts_size_v = size_v
    surf.ctrlpts = points.ctrlpts

    # Set knot vectors
    knot_u = [float(x) for x in range(415)]
    knot_u = [0.0, 0.0, 0.0, 0.0] + knot_u + [415.0, 415.0, 415.0, 415.0]
    knot_v = [float(x) for x in range(487)]
    knot_v = [0.0, 0.0, 0.0, 0.0] + knot_v + [487.0, 487.0, 487.0, 487.0]

    surf.knotvector_u = knot_u
    surf.knotvector_v = knot_v

    # Set evaluation delta
    surf.delta = 0.005

    # Evaluate surface points
    surf.evaluate()

    # from matplotlib import cm
    #
    # # Plot the control point grid and the evaluated surface
    # vis_comp = mpl.VisSurface()
    # # vis_comp = vis.VisSurface()
    # surf.vis = vis_comp
    # surf.render(colormap=cm.cool)

    return surf