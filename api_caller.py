import os
import json
import random
import requests
import dicttoxml

from urllib.parse import quote
from json_csv_helper import unfold
from data_cleaning import clean_list, parse_date, \
    parse_user_dates, add_missing_columns
from utils import items_to_csv


labels = ['items_id', 'items_title', 'items_country', 'items_dataProvider',
          'items_type', 'items_edmTimespanLabelLangAware_def',
          'items_dcCreator', 'items_edmPreview']


def create_usr_directory(root):
    '''
        Create a unique user directory to store tmp data and output data
        Needed when multiple request are made at the same time
    '''
    dir_name = random.randint(100000, 300000)

    dir_path = root + '/public/{}/'.format(dir_name)
    if not os.path.isdir(dir_path):
        os.mkdir(dir_path)
        print('Creating {}'.format(dir_path))

    return dir_path, dir_name


def parse_query(usr_data):

    if all(x == '' for x in usr_data.values()):
        return None

    keywords, creator, places = '', '', ''

    if usr_data['keywords'] != '':
        keywords = '"' + quote(usr_data['keywords'], safe='') + '"'
    if usr_data['creator'] != '':
        creator = '+who:' + '"' + quote(usr_data['creator'], safe='') + '"'
    if usr_data.get('places') != '' and usr_data.get('places') is not None:
        places = '+where:' + '"' + quote(usr_data['places'], safe='') + '"'

    time = '+timestamp_created:[{}-01-01T00:00:0.000Z+TO+{}-01-01T00:00:00.000Z]'.format(
        usr_data['from'], usr_data['to'])

    query = 'https://www.europeana.eu/api/v2/search.json?wskey={}&rows=100&query={}{}{}{}&cursor='.format(
        usr_data['key'], keywords, creator, places, time)

    return query


def execute_query(usr_data):

    print('USER DATA')
    print(usr_data)

    cursorMark = '*'
    nextCursor = ''
    items = []
    query_status = None
    error = None

    usr_data.update(parse_user_dates(usr_data))
    query = parse_query(usr_data)
    print('Base query:', query)

    print('\nEXECUTING API REQUEST\n')

    # Create temporary dir to store usr data
    dir_path, dir_name = create_usr_directory(usr_data['root'])
    print('JUST CREATED: {}'.format(dir_name))

    while(1):
        q = query + cursorMark

        # Load query result
        data = requests.get(q).json()

        # Display query status and error
        query_status = data.get('success')
        error = data.get('error')
        print('Query status: {}'.format(query_status))
        print('Error: {}'.format(error))
        print('Current cursor: {}'.format(cursorMark))

        # Save current items
        if data.get('items') is not None:
            for i in data['items']:
                items.append(unfold('items', i))
        else:
            print('NO ITEMS IN DATA')
            print(data)
            break

        # Retrive next cursor
        if data.get('nextCursor') is None:
            break
        else:
            nextCursor = quote(data['nextCursor'], safe='')
            cursorMark = nextCursor

        print('Next cursor: {}'.format(data['nextCursor']))
        print('Query: ', q, '\n')
        print('\n================================================\n\n')

    # Add missing values
    items = add_missing_columns(items)

    # Keep dcterms only and rename
    items = [{k: clean_list(i[k]) for k in i if k in labels} for i in items]

    # Filter date
    items = parse_date(items)
    new_it = []
    for i in range(len(items)):
        if items[i]['items_edmTimespanLabelLangAware_def'] >= usr_data['from'] and \
                items[i]['items_edmTimespanLabelLangAware_def'] <= usr_data['to']:
            new_it.append(items[i])
    items = new_it

    if len(usr_data['type']) > 0:
        items = [i for i in items if i['items_type'] in usr_data['type']]

    # Test if any result
    print('[ + ] After filtering, items found:', len(items))
    if len(items) == 0:
        return {'data': None, 'dir': dir_name,
                'query_status': query_status, 'error': str(error)}

    # Save data to csv
    output_path = dir_path + 'output.csv'
    items_to_csv(items, output_path)

    # Save data to json
    output_path = dir_path + 'output.json'
    with open(output_path, 'w') as f:
        json.dump(items, f)

    # Save data to xml
    output_path = dir_path + 'output.xml'
    with open(output_path, 'wb') as f:
        f.write(dicttoxml.dicttoxml(items))

    return {'data': items, 'dir': dir_name,
            'query_status': query_status, 'error': error}
