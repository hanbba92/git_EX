import os
import subprocess

interpreter_dir = 'C:/Users/user/Documents/project/aiw-task-cm/venv/Scripts/python.exe'
code_dir = '../application.py'
nc_folder = 'D:/nc_inuse/front'
argv1 = 'flow1234'
argv3 = 'FLOWDATA/4000_2'
argv4 = 'FLOWDATA/52_850_5'
argv5 = '49_9'



# Iterate over the files in the folder
for filename in os.listdir(nc_folder):
    input_file_path = os.path.join(nc_folder, filename)
    subprocess.run(['python',code_dir, argv1, input_file_path, argv3, argv4, argv5])

