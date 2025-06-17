import os
import pandas as pd

# Get the current working directory of the python file that is running
CURRENT_DIRECTORY = os.getcwd()


# We know that the data is actually in a 'data' folder. So, we create a path with the current directory and add the data string
DATA_DIRECTORY = os.path.join(CURRENT_DIRECTORY, 'data')

# We then find out the path of all the files in that folder
FILE_PATH_LIST = os.listdir(DATA_DIRECTORY)

print(FILE_PATH_LIST)

IMPORTED_FILES = []

for path in FILE_PATH_LIST:
    csv_file = pd.read_csv(os.path.join(DATA_DIRECTORY, path), encoding='latin-1')
    IMPORTED_FILES.append(csv_file)
