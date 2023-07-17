import matplotlib.pyplot as plt
import numpy as np
import sys
from aiw_task_cm.file.file_manager_factory import FileManagerFactory
import os

front_dir = 'D:/nc_inuse/front'
nonfront_dir = 'D:/nc_inuse/nonfront'
variable_name = 'FLOWDATA/task49_3'

def access_values(fm, file_dir, var_name):
    task_var, _ = fm.read(file_dir, data_path=var_name)
    return task_var


def see_values():
    fm = FileManagerFactory().get_instance('netcdf')
    print('===============front===============')
    for filename in os.listdir(front_dir):
        file_path = os.path.join(front_dir, filename)
        var = access_values(fm, file_path, variable_name)[0,0] / 1e9
        print(filename, var)
    print('===============nonfront===============')
    for filename in os.listdir(nonfront_dir):
        file_path = os.path.join(nonfront_dir, filename)
        var = access_values(fm, file_path, variable_name)[0,0] /1e9
        print(filename, var)


see_values()
