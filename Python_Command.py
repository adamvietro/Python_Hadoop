# import the python subprocess module
import subprocess
import os
import sys


TEST = True


def command_map_reduce_streaming (hdfs_input, hdfs_output, \
                        sort_type = '', mapper = '"python mapper.py"', reducer = '"python reducer.py"', \
                        files = []):
    ''' This is for running a map reduce command through Python. This can take
    lot of arguements if needed. You will need to specify the hdfs input and
    ouput paths. sort_type, mapper, reducer, and files are optional.

    Args: The input hdfs directory that you want to pull from, the output hdfs
    directory that you want to output to, the type of sort (if not passed it will
    be a standard sort), the mapper script (if not passed it will be "python mapper.py"),
    the reducer (if not passed it will be "python reducer.py"), the files that you want
    passed (if not passed you will upload no files).

    Returns: This will return a string with an error code for the process completed.
    '''
    jar_path = "C:\\Hadoop\\hadoop-2.9.1\\share\\hadoop\\tools\\lib\\hadoop-streaming-2.9.1.jar"
    sub_input = ['hadoop', 'jar', jar_path] 
    if sort_type != '':
        d_sort = 'mapred.text.key.comparator.options=-' + sort_type
        d_ = '-D'
        dir_ = 'mapred.output.key.comparator.class=org.apache.hadoop.mapred.lib.KeyFieldBasedComparator'
        sub_input.append(d_)
        sub_input.append(dir_)
        sub_input.append(d_)
        sub_input.append(d_sort)
    sub_input.append("-mapper")
    sub_input.append(mapper)
    sub_input.append("-reducer")
    sub_input.append(reducer)
    sub_input.append("-input")
    sub_input.append(hdfs_input)
    sub_input.append("-output")
    sub_input.append(hdfs_output)
    if files:
        files_ = '-file'
        sub_input.append(files_)
        len_files = len(files)
        for counter, item in enumerate(files):
            if counter == 0 and len_files > 1:
                sub_input.append(item + ',')
            elif counter < len_files - 1:
                sub_input.append(item + ',')
            else:
                sub_input.append(item)
    if TEST:
        print(sub_input)
    location = os.path.dirname(sys.argv[0])
    message = subprocess.run(['cd', location], shell=True, capture_output=TEST)
    if TEST:
        print(message)
    message = subprocess.run('dir', shell=True, capture_output=TEST)
    if TEST:
        print (message)
    message = subprocess.run(sub_input, shell=True, capture_output=TEST)
    if TEST:
        print (message)
    return message


if __name__ == '__main__':
    if TEST:
        print("Performing Mapreduce...")
    error_map_reduce = command_map_reduce_streaming(sort_type = 'r', hdfs_input = '/test/*',  hdfs_output = '/test/output', files = ['mapper.py', 'reducer.py'])
    if TEST:
        print(error_map_reduce)
    

    
        
