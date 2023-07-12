import os
import subprocess

# Specify the folder containing the files
input_folder_path = 'D:/nonfront/output'
#output_folder_path = '/mnt/d/raw/220727'

# Specify the program you want to run
program_path = 'C:/Users/user/Documents/aiwroot/aiw/AIW20A-50/application.py'

# Iterate over the files in the folder

for filename in os.listdir(input_folder_path):


    input_file_path = input_folder_path+'/'+filename
    #output_file_path = os.path.join(output_folder_path, filename) + '.nc'
    print(input_file_path)
    # print(output_file_path)

    # Check if the current item is a file
    if os.path.isfile(input_file_path):
        # Execute the program for the current file
        subprocess.run(['C:/Users/user/AppData/Local/Programs/Python/Python36/python.exe', program_path, 'flow', input_file_path, '900', '600'])
