import os
import subprocess

interpreter_dir = 'C:/Users/user/Documents/project/aiw-task-cm/venv/Scripts/python.exe'
code_dir = '../application.py'
nc_folder1 = 'D:/nc_inuse/front_unis_mod'
nc_folder2 = 'D:/nc_inuse/nonfront_unis_mod'
argv1 = 'flow1234'
argv3 = 'INPUTDATA/PRMSL'
argv4 = 'task59'



# Iterate over the files in the folder
for filename in os.listdir(nc_folder1):
    input_file_path = os.path.join(nc_folder1, filename)
    subprocess.run(['python',code_dir, argv1, input_file_path, argv3, argv4])

for filename in os.listdir(nc_folder2):
    input_file_path = os.path.join(nc_folder2, filename)
    subprocess.run(['python',code_dir, argv1, input_file_path, argv3, argv4])

