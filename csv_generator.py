import os
import pandas as pd

# Get the current working directory of the python file that is running
CURRENT_DIRECTORY = os.getcwd()


# We know that the data is actually in a 'data' folder. So, we create a path with the current directory and add the data string
DATA_DIRECTORY = os.path.join(CURRENT_DIRECTORY, 'data')

# We then find out the path of all the files in that folder
FILE_PATH_LIST = os.listdir(DATA_DIRECTORY)


for path in FILE_PATH_LIST:
    full_path = os.path.join(DATA_DIRECTORY, path)
    
    # Read the original ; separated file
    with open(full_path, 'r', encoding='latin-1') as f:
        content = f.read()
    
    # Replace ; with ,
    converted_content = content.replace(';', ',')
    
    # Create a new file name with _converted.csv
    base_name = os.path.splitext(path)[0]
    new_csv_path = os.path.join(DATA_DIRECTORY, base_name + '_converted.csv')
    
    # Write the converted content
    with open(new_csv_path, 'w', encoding='utf-8') as f:
        f.write(converted_content)
