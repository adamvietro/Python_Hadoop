from urllib.request import urlopen, Request
import json
import sys


def load_url (url):
    ''' This will take an input of a http and create a false header to get
        around the Forbiddin error and load the API.

        Args: A HTTP.

        Returns: An API.
    '''    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
    reg_url = url
    req = Request(url=reg_url, headers=headers) 
    html = urlopen(req).read()
    return html


def load_JSON (site):
    ''' This will take an API and turn it into a JSON.

    Args: An API.

    Returns: A JSON object.
    '''   
    data = json.loads(site)
    return data

    
def print_characters (object):
    ''' This will take a JSON object from the Exile API pertaining to the characters a profile has and print the Name, Class,
        Class ID, Experience, League, and Level.

        Args: A JSON obejct

        Returns: Null
    '''   
    print("name: {}".format(object['name']))
    print("class: {}".format(object['class']))
    print("class ID: {}".format(object['classId']))
    print("experience: {}".format(object['experience']))
    print("league: {}".format(object['league']))
    print("level: {}\n\n".format(object['level']))


def print_items (object):
    ''' This will take a JSON object pertaining to a characters items and print the stats and other information about the items.

        Args: A JSON object.

        Returns: Null.
    '''
    for item in object["items"]:
        if "name" in item:
            print("Name: {}".format(item["name"]))
        if "ilvl" in item:
            print("Item Level: {}".format(item["ilvl"]))
        if "properties" in item:
            print("Properties")
            for properties in item["properties"]:
                print("{}: {}".format(properties["name"], properties["values"]))
        if "implicitMods" in item:
            print("Implicit Mods")
            for properties in item["implicitMods"]:
                print(properties)
        if "explicitMods" in item:
            print("Explicit Mods")
            for properties in item["explicitMods"]:
                print(properties)
        print('\n')

def get_characters (object):
    ''' This will take a JSON pertaining to an PoE account and return the characters names.

        Args: A JSON object.

        Retruns: A list of all character names.
    '''    
    char_list = []
    for char in object:
        character = char["name"]
        new_character = []
        flag = True
        for letter in character:# This is a check of special characters in a \
                                #characters name.
            if letter == "á":
                new_character.append('%C3%A1')
                flag = False
            else:
                new_character.append(letter)
        if flag:
            char_list.append(character)
        else:
            redo = ''.join(new_character)
            char_list.append(redo)
    return char_list


def create_item_url (account, character):
    ''' This will input values in a string that will bring up the items from characters in a valid PoE account.

        Args: A Valid PoE account and a Character in that account.

        Returns: the url for the items for that character.
    '''
    return ("https://www.pathofexile.com/character-window/get-items?accountName={}&character={}".format(account, character))


def create_account_url (account):
    ''' This will input values into a string that will bring up the characters from a PoE account given.

        Args: A valid PoE account name.

        Retruns: The url for a list of characters from PoE account.
    '''
    return ("https://www.pathofexile.com/character-window/get-characters?accountName={}".format(account))


def get_PoE_stash ():
    ''' This is used to get the first of the public PoE tabs, every other call depends on this
        one.

        Args: Null

        Returns: The JSON object for the first PoE Tab.
    '''
    stash_api = load_url("https://www.pathofexile.com/api/public-stash-tabs?id=0")
    return load_JSON(stash_api)


def get_next_stash (next_id):
    ''' This is used to get the next tab of the public PoE tab, this requires the next id
        that a previous call will generate

        Args: The next id in string format

        Returns: The stash in JSON format.
    '''
    stash_api = load_url("https://www.pathofexile.com/api/public-stash-tabs?id={}".format(next_id))
    return load_JSON(stash_api)
    
def get_next_id (object):
    ''' This pulls the next change id out of the JSON object from the PoE public api.

        Args: a JSON object from the public API.

        Returns: The next change id needed for a other get.
    '''
    return object['next_change_id']

def get_api_stash_items (object, item_list):
    ''' This will create and append a list with all the items within a JSON object obtained
        from the public PoE tab.

        Args: A JSON object and the item list that will be passed to the function.

        Returns: Null
    '''
    for stash in object['stashes']:
        for item in stash['items']:
            new_item = {"name":item['name'], "level":item['ilvl']}
            item_list.append(new_item)


def find_highest_ilvl_items (item_list, number_of_items):
    ''' This will go through a list of dicts with item name and ilvl. It will go through the
        list and give the highest ilvl items up to the amount given.

        Args: A list of dicts with name and ilvl as IDs, and the number of items to return.

        Returns: A list of dicts with the highest ilvl items.
    '''
    highest_items = []
    for x in range (number_of_items):
        dict_location = 0
        enumerator = 0
        highest_ilvl = 0
        item_name = ''
        for object_dict in item_list:
            if object_dict["level"] > highest_ilvl and object_dict['name'] != '':
                highest_ilvl = object_dict["level"]
                item_name = object_dict['name']
                dict_location = enumerator
            enumerator += 1
        highest_items.append({'name':item_name, 'level':highest_ilvl})
        del item_list[dict_location]
    return highest_items
                
            
def get_number_of_tabs():
    ''' This is a simple user interface to get an PoE account name from a user .

    Args: Null.

    Returns: Number of tabs in integer format.
    '''
    account_name = input("Please provide the number of tabs to get: ")
    return int(account_name)


def get_number_of_items():
    ''' This is a simple user interface to get the number of itsm .

    Args: Null.

    Returns: Number of items in integer format.
    '''
    account_name = input("Please provide the number of top items wanted: ")
    return int(account_name)
    

if __name__ == '__main__':
    number_of_tabs = get_number_of_tabs()
    number_of_items = get_number_of_items()
    item_list = []
    next_id = ''
    stash = get_PoE_stash()
    for x in range (number_of_tabs):
        get_api_stash_items(stash, item_list)
        next_id = get_next_id(stash)
        stash = get_next_stash(next_id)
    highest_items = find_highest_ilvl_items(item_list, number_of_items)
    for item in highest_items:
        if len(item['name']) <= 4:
            print("Name: {},\t\t\t Item Level: {}".format(item['name'],item['level']))
        elif len(item['name']) <= 8:
            print("Name: {},\t\t Item Level: {}".format(item['name'],item['level']))
        else:
            print("Name: {},\t Item Level: {}".format(item['name'],item['level']))
    
    
    

