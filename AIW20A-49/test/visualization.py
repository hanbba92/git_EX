import matplotlib.pyplot as plt
import numpy as np
import sys
from aiw_task_cm.file.file_manager_factory import FileManagerFactory
import os

front_dir = 'D:/nc_inuse/front'
nonfront_dir = 'D:/nc_inuse/nonfront'
variable_name = 'FLOWDATA/49_9'

def access_values(fm, file_dir, var_name):
    task_var, _ = fm.read(file_dir, data_path=var_name)
    return task_var


def hist_plot():
    front = np.array([])
    nonfront= np.array([])
    fm = FileManagerFactory().get_instance('netcdf')
    for filename in os.listdir(front_dir):
        file_path = os.path.join(front_dir, filename)
        var = access_values(fm, file_path, variable_name)
        front = np.append(front, var[0,0,0])
    for filename in os.listdir(nonfront_dir):
        file_path = os.path.join(nonfront_dir, filename)
        var = access_values(fm, file_path, variable_name)
        nonfront = np.append(nonfront, var[0,0,0])
    bin_edge = np.linspace(np.min(nonfront), np.max(front), 90)
    plt.hist(front, label='front', alpha=0.5, histtype='bar', bins=bin_edge)
    plt.hist(nonfront, label='nonfront',alpha=0.5, histtype='bar', bins=bin_edge)
    plt.legend()
    plt.show()


hist_plot()
