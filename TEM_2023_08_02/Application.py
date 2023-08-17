from GradientDescent import *
from plot import *
from generate_surf import *
import os
from netCDF4 import Dataset
from geomdl import operations
from geomdl import BSpline
from geomdl import control_points
import sys
import numpy as np
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Examples for the NURBS-Python Package
    Released under MIT License
    Developed by Onur Rauf Bingol (c) 2016-2018
"""




class Application(object):
    def __init__(self, input_data_path, initial_alpha):
        self.input_data_path = input_data_path
        #self.initial_array = np.array([int(i) for i in initial_array.split(',')])
        self.initial_alpha = float(initial_alpha)
        self.Grad=GradientDescent
        self.Plot = plot


    def run(self):
        nc = dataset(self.input_data_path)
        # Fix file path
        os.chdir(os.path.dirname(os.path.realpath(__file__)))

        # Create a BSpline surface instance

        # Set degrees

        # Set control points



        prmsl_all = nc['INPUTDATA'].variables['PRMSL']
        nc_dim=prmsl_all[0].shape
        lat = np.arange(nc_dim[0])
        lon = np.arange(nc_dim[1])
        XX, YY = np.meshgrid(lon, lat)

        u = XX.flatten()
        v = YY.flatten()

        lat = np.linspace(0.01, 0.99, 10)
        lon = np.linspace(0.01,0.99,10)
        times = nc['INPUTDATA'].variables['times']
        for i in range(len(times)):
            prmsl=prmsl_all[i]
            p=prmsl.flatten()
            surf=generate_surf(u,v,p)
            p_reversed = p*-1
            surf_reversed=generate_surf(u,v,p_reversed)
            print('sur calculated done')
            dims = (len(times), nc['INPUTDATA'].variables['longitude'].shape[0], nc['INPUTDATA'].variables['longitude'].shape[1])
            result = np.empty(dims)
            high=[]
            low=[]
            total=0
            prmsl_threshold_low=np.median(prmsl)-np.std(prmsl)*0.5
            prmsl_threshold_high=np.median(prmsl)+np.std(prmsl)*0.5
            for y in lat:
                for x in lon:
                    ans,xr,yr=self.Grad(prmsl,surf, np.array([y,x]), self.initial_alpha)

                    if ans:
                        iy,ix=xr[-1]
                        if yr[-1] <= prmsl_threshold_low:
                            low.append([int(iy),int(ix)])

                            result[i,int(iy),int(ix)]=-1

                    ans, xr,yr=self.Grad(p_reversed, surf_reversed, np.array([y,x]), self.initial_alpha)


                    if ans:
                        iy,ix=xr[-1]
                        if yr[-1] >= prmsl_threshold_high:
                            result[i,int(iy),int(ix)]=1
                            high.append([int(iy),int(ix)])
                    total+=1
                    print(f'{total}/100 done')
            self.Plot(self.input_data_path,low,high,i)







def main():
    input_data_path = sys.argv[1]

    initial_alpha = sys.argv[2]

    result = 0
    try:
        app = Application(input_data_path, initial_alpha)
        app.run()
    except Exception as e:
        print(e)
        result = 1
    finally:
        sys.exit(result)


if __name__ == '__main__':
    main()