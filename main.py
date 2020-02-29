from Import_PoE_API     import  load_url, load_JSON, get_PoE_stash, get_next_stash, \
                                get_next_id, get_api_stash_items                    \
                        as      load_url, load_JSON, get_PoE_stash, get_next_stash, \
                                get_next_id, get_api_stash_items                        
from Python_Hadoop      import  hdfs_upload as hdfs_upload
from Python_Hadoop      import  hdfs_mkdir as hdfs_mkdir
from Python_Hadoop      import  hdfs_download as hdfs_download
from Python_Hadoop      import  hdfs_delete as hdfs_delete
from Python_Local_File  import  create_file, open_file_rel, open_file, delete_file  \
                        as      create_file, open_file_rel, open_file, delete_file
from Python_Command     import  command_map_reduce_streaming                        \
                        as      command_map_reduce
from hdfs               import  InsecureClient
import sys
import json
import os


if __name__ == '__main__':
    location = os.path.dirname(sys.argv[0])
    part_location = location +'\\Data\\part-00000'
    data_location = location + '\\Data'
    config = open('config.txt')
    for line in config:
        sys_, amount = line.split('\t')
        if sys_ == "NUMBER_OF_TABS":
            NUMBER_OF_TABS = int(amount)
        if sys_ == "NUMBER_OF_ITEMS":
            NUMBER_OF_ITEMS = int(amount)
    config.close()
    PRINT_BOOL = True
    item_list = []
    next_id = ''
    user_input = ''
    continue_ = True

    while user_input == '' and (user_input != 'whole' or  user_input != 'raw'or \
                                user_input != 'upload' or user_input != 'mapreduce' or \
                                user_input != 'download' or user_input != 'open'):
        user_input = input("Where to start?:\n\
        Whole Program, whole:\n\
        Create raw_text.txt, raw:\n\
        Upload to the HDFS cilent, upload:\n\
        MapReduce step, mapreduce:\n\
        Download the file from HDFS, download:\n\
        Open the local HDFS file: open\n\
        ")
        
    client = InsecureClient('http://localhost:50070')
    if user_input == 'raw' or user_input == 'whole':
        if PRINT_BOOL:
            print ("Getting stash")
        user_input = 'whole'
        stash = get_PoE_stash()
        for x in range (NUMBER_OF_TABS):
            get_api_stash_items(stash, item_list)
            next_id = get_next_id(stash)
            stash = get_next_stash(next_id)
        with open("raw_data.txt", 'w') as outfile:
            for counter, line in enumerate(item_list):
                if line["name"] != '':
                    write_line = str(counter) + '\t' + line["name"] + '\t' + str(line["level"]) + '\n'
                    outfile.write(write_line)
        

    if user_input == 'upload' or user_input == 'whole':
        if PRINT_BOOL:
            print ("Uploading")
        user_input = 'whole'
        hdfs_mkdir(client, '/home/PoE')
        hdfs_upload(client, '/home/PoE', 'raw_data.txt',False)


    if user_input == 'mapreduce' or user_input == 'whole':
        if PRINT_BOOL:
            print ("MapReduce")
        user_input = 'whole'
        command_map_reduce(sort_type = 'r', hdfs_input = '/home/PoE*',\
                           hdfs_output = '/home/PoE/Output',\
                           files = ['mapper.py', 'reducer.py'])


    if user_input == 'download' or user_input == 'whole':
        if PRINT_BOOL:
            print ("Downloading")
        user_input = 'whole'
        try:
            hdfs_download(client, "/home/PoE/Output/part-00000", part_location, False)
        except ValueError:
            print ("Download failed")
            hdfs_delete(client, "/home/PoE/raw_data.txt", True, False)
        

    if user_input == 'open' or user_input == 'whole':
        if PRINT_BOOL:
            print ("Opening")
        map_reduce_item = open(part_location)

        for line in map_reduce_item:
            line.strip()
            item , ilvl = line.split('\t')
            if len(item) < 10:
                print("Name:{},\t\t\t\tItem Level: {}".format(item,ilvl))
            elif len(item) < 18:
                print("Name:{},\t\t\tItem Level: {}".format(item,ilvl))
            elif len(item) < 26:
                print("Name:{},\t\tItem Level: {}".format(item,ilvl))
            elif len(item) < 34:
                print("Name:{},\tItem Level: {}".format(item,ilvl))
            else:
                print("Name:{},Item Level: {}".format(item,ilvl))

        map_reduce_item.close()
        hdfs_delete(client, "/home/PoE/Output/_SUCCESS", False, False)
        hdfs_delete(client, "/home/PoE/Output/part-00000", False, False)
        hdfs_delete(client, "/home/PoE/Output/", False, False)

        
        user_input = input("Clear the local output? yes/no:")
        if user_input == 'yes':
            delete_file("part-00000", data_location)

        user_input = input("Clear the HDFS input? yes/no:")
        if user_input == 'yes':
            hdfs_delete(client, "/home/PoE/raw_data.txt", False, False)
                  
    
    
        
