import matplotlib.pyplot as plt
import numpy as np
import sys
from aiw_task_cm.file.file_manager_factory import FileManagerFactory
import os
from matplotlib import font_manager, rc
font_path = "C:/Windows/Fonts/NGULIM.TTF"
font = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font)
front_dir = 'D:/nc_inuse/front'
nonfront_dir = 'D:/nc_inuse/nonfront'
variable_name = 'FLOWDATA/task49_3'

# def access_values(fm, file_dir, var_name):
#     task_var, _ = fm.read(file_dir, data_path=var_name)
#     return task_var
x=[15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35]
front= [49, 49, 49, 49, 48, 47, 46, 45, 44, 41, 40, 40, 39, 38, 36, 32, 29, 28, 25, 23, 22]
nonfront=[49, 48, 45, 43, 41, 40, 37, 34, 29, 26, 23, 21, 17, 14, 12, 10, 9, 8, 8, 8, 5]
import pandas as pd
df = pd.DataFrame({'front':front, 'nonfront':nonfront}, index=x)
df.to_csv('D:/shear.csv')
print(df)

def hist_plot():
    # front = np.array([])
    # nonfront= np.array([])
    # fm = FileManagerFactory().get_instance('netcdf')
    # for filename in os.listdir(front_dir):
    #     file_path = os.path.join(front_dir, filename)
    #     var = access_values(fm, file_path, variable_name)
    #     front = np.append(front, var[0,0])
    # for filename in os.listdir(nonfront_dir):
    #     file_path = os.path.join(nonfront_dir, filename)
    #     var = access_values(fm, file_path, variable_name)
    #     nonfront = np.append(nonfront, var[0,0])
    #bin_edge = np.linspace(np.min(nonfront), np.max(front), 50)
    plt.bar(x, front, label='front', alpha=0.5)
    plt.bar(x, nonfront, label='nonfront',alpha=0.5)
    plt.xlabel('윈드시어 기준치')
    plt.ylabel('케이스 수')
    plt.title('윈드시어가 기준치보다 큰 케이스 수')
    plt.legend()

    plt.show()


hist_plot()
