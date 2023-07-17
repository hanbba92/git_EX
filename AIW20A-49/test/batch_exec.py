import os
import subprocess

interpreter_dir = 'C:/Users/user/Documents/project/aiw-task-cm/venv/Scripts/python.exe'
code_dir = '../application.py'
nc_folder1 = 'D:/nc_inuse/front'
nc_folder2 = 'D:/nc_inuse/nonfront'
argv1 = 'flow1234'
argv3 = 'FLOWDATA/900-600'
argv4 = 'FLOWDATA/task53_3'
argv5 = 'task49_3'



# Iterate over the files in the folder
for filename in os.listdir(nc_folder1):
    input_file_path = os.path.join(nc_folder1, filename)
    subprocess.run(['python',code_dir, argv1, input_file_path, argv3, argv4, argv5])

for filename in os.listdir(nc_folder2):
    input_file_path = os.path.join(nc_folder2, filename)
    subprocess.run(['python',code_dir, argv1, input_file_path, argv3, argv4, argv5])

