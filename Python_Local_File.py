import os
import sys
import json

def create_file (file_name, data):
    ''' This is used to creat a local file with the data sent to the function
        with the name given as well.

        Args: A file name and the data to be writen to the file.

        Return: Null.
    '''
    with open(file_name, 'w') as outfile:
        json.dump(data, outfile)

def open_file_rel (file_name):
    ''' This is used to open a file in the directory that the python script is
        being called from.

        Args: Simply a file name.

        Return: The open file.
        '''
    return open(file_name)

def open_file (file_name, location):
    ''' This is used to open a file within your computer, it requires a location
        and a file name.

        Args: A file name and the path.

        Returns: The open file.
        '''
    full_path = os.path.join(location, file_name)
    return open(full_path)

def delete_file(file_name, location):
    ''' This is used to delete a local file.

    Args: A file name and the path to it.

    Returns: Null
    '''
    path = os.path.join(location,file_name)
    os.remove(path)
    
