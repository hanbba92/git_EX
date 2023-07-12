import matplotlib.pyplot as plt
import numpy as np
import sys
from aiw_task_cm.file.file_manager_factory import FileManagerFactory
import os

front_dir = 'D:/nc_inuse/front'
nonfront_dir = 'D:/nc_inuse/nonfront'
variable_name = 'FLOWDATA/900-600'

def access_values(fm, file_dir, var_name):
    task_var, _ = fm.read(file_dir, data_path=var_name)
    return task_var


def max_plot():
    front_max = np.array([])
    nonfront_max= np.array([])
    fm = FileManagerFactory().get_instance('netcdf')
    for filename in os.listdir(front_dir):
        file_path = os.path.join(front_dir, filename)
        var = access_values(fm, file_path, variable_name)
        front_max = np.append(front_max, np.max(var))
    for filename in os.listdir(nonfront_dir):
        file_path = os.path.join(nonfront_dir, filename)
        var = access_values(fm, file_path, variable_name)
        nonfront_max = np.append(nonfront_max, np.max(var))
    bin_edge = np.linspace(0, np.max(front_max), 30)
    plt.hist(front_max, label='front_max', alpha=0.5, histtype='bar', bins=bin_edge)
    plt.hist(nonfront_max, label='nonfront_max',alpha=0.5, histtype='bar', bins=bin_edge)
    plt.legend()
    plt.show()

def variance_plot():
    front_var = np.array([])
    nonfront_var= np.array([])
    fm = FileManagerFactory().get_instance('netcdf')
    for filename in os.listdir(front_dir):
        file_path = os.path.join(front_dir, filename)
        var = access_values(fm, file_path, variable_name)
        front_var = np.append(front_var, np.var(var))
    for filename in os.listdir(nonfront_dir):
        file_path = os.path.join(nonfront_dir, filename)
        var = access_values(fm, file_path, variable_name)
        nonfront_var = np.append(nonfront_var, np.var(var))
    bin_edge = np.linspace(0, np.max(front_var), 30)
    plt.hist(front_var, label='front_var', alpha=0.5, histtype='bar', bins=bin_edge)
    plt.hist(nonfront_var, label='nonfront_var',alpha=0.5, histtype='bar', bins=bin_edge)
    plt.legend()
    plt.show()

def max_mult_variance_plot():
    front_max = np.array([])
    nonfront_max= np.array([])
    fm = FileManagerFactory().get_instance('netcdf')
    for filename in os.listdir(front_dir):
        file_path = os.path.join(front_dir, filename)
        var = access_values(fm, file_path, variable_name)
        front_max = np.append(front_max, np.var(var) * np.max(var))
    for filename in os.listdir(nonfront_dir):
        file_path = os.path.join(nonfront_dir, filename)
        var = access_values(fm, file_path, variable_name)
        nonfront_max = np.append(nonfront_max, np.var(var) * np.max(var))
    bin_edge = np.linspace(0, np.max(front_max), 30)
    plt.hist(front_max, label='front_max*var', alpha=0.5, histtype='bar' , bins=bin_edge)
    plt.hist(nonfront_max, label='nonfront_max*var',alpha=0.5, histtype='bar', bins=bin_edge)
    plt.legend()
    plt.show()

max_plot()
variance_plot()
max_mult_variance_plot()