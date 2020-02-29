from hdfs import InsecureClient


def hdfs_delete(client, path_to_delete, recurse, print_bool):
    ''' This is used for deleting a file or folder.

    Args: The client, the path to the file or folder, and whether or not you want recursive, and
    whether you want a print status.

    Returns: Null.
    '''
    client.delete(path_to_delete, recursive=recurse, skip_trash=True)
    if print_bool:
        print ("{} has been deleted".format(path_to_delete))
        

def hdfs_download(client, hdfs_path, local_path, print_bool):
    ''' This is used to

    Args: The client, the path to the hdfs file or folder, and the local path where
    you want to download to, and whether or not you want a print status.

    Returns: Null.
    '''
    print_str = client.download(hdfs_path, local_path)
    if print_bool:
        print (print_str)
    

def hdfs_list(client, hdfs_path):
    ''' This is used for printing the current state of the files and folders on
    the hdfs server.

    Args: The client, and the hdfs path you want to see the information for

    Returns: Null.
    '''
    for x in client.list(hdfs_path, status=False):
        print (x)


def hdfs_upload(client, hdfs_path, local_path, print_bool):
    ''' This is used to upload a file to the hdfs server.

    Args: The client, the hdfs path that you want to upload to, the local path to the file or folder you want
    uploaded, and whether or not you want a print status.

    Return: Null.
    '''
    remote_path = client.upload(hdfs_path, local_path, n_threads=1, temp_dir=None, chunk_size=65536, progress=None, cleanup=True)
    if print_bool:
        print ("Uploaded to {}".format(remote_path))


def hdfs_mkdir(client, hdfs_path):
    ''' This is used to create a dir on the hdfs server.

    Args: The client, and the path you want created.

    Return: Null.
    '''
    client.makedirs(hdfs_path, permission=None)


def hdfs_get(client, hdfs_path, local_path, print_bool):
    ''' This is used to read a file from the hdfs server.

    Args: The client, and the path to the hdfs file, and the local path where you want to download
    to.

    Return: Null.
    '''
    local_path = client.download(hdfs_path, local_path, overwrite=True, n_threads=1, temp_dir=None)
    if print_bool:
        print (local_path)
        
if __name__ == '__main__':
    client = InsecureClient('http://localhost:50070')

    print ("current top level")
    hdfs_list(client, '/')
    print("")

    print ("creating /PoE")
    hdfs_mkdir(client, '/PoE')
    print ("current top level")
    hdfs_list(client, '/')
    print("")

    print ("uploading Char_Items.txt")
    hdfs_upload(client, '/PoE', 'Char_Items.txt',False)          
    print ("current top level")
    hdfs_list(client, '/')
    hdfs_list(client, '/PoE')
    print("")

    print("downloading Char_Items")
    hdfs_get(client, '/PoE/Char_Items.txt', '/Users/Vinny-Lap/Dropbox/Python/PoE-Hadoop/tmp', False)
    print('')

        
    print ("deleting '/PoE'")
    hdfs_delete(client, '/PoE', True, False)
    print ("current top level")
    hdfs_list(client, '/')
    print("")



