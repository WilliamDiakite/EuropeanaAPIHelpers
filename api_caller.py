import os
import json
import random

from json_csv_helper import unfold
from data_manipulation import items_to_csv, clean_list, filter_dates, filter, \
    parse_date

labels = ['items_id', 'items_title', 'items_country', 'items_dataProvider',
          'items_type', 'items_edmTimespanLabelLangAware_def',
          'items_dcCreator', 'items_edmPreview']


def create_usr_directory(session):
    '''
        Create a unique user directory to store tmp data and output data
        Needed when multiple request are made at the same time
    '''
    dir_name = str(session)

    dir_path = './tmp/{}/'.format(dir_name)
    if not os.path.isdir(dir_path):
        os.mkdir(dir_path)

    return dir_path


def parse_query(data):
    base = 'https://www.europeana.eu/api/v2/search.json?wskey='

    query = base + str(data['key'])

    # Keywords
    if len(data['keywords']) > 0:
        keywords = data['keywords'].split(' ')
        q1 = '&query=' + '"' + '+'.join(keywords) + '"'
    else:
        q1 = ''

    return query + q1


def execute_query(usr_data, session):

    print('\nEXECUTING API REQUEST\n')

    cursorMark = '*'
    nextCursor = ''
    items = []
    query_status = None
    error = None

    query = parse_query(usr_data)

    # Create temporary dir to store usr data
    dir_path = create_usr_directory(session)

    while(1):
        # Execute command and save data in tmp file
        tmp_path = dir_path + 'tmp.json'

        cmd = 'curl ' + '"' + query + '&rows=100&cursor=' + \
              cursorMark + '"' + ' > ' + tmp_path

        print('\n\n', cmd, '\n')
        os.system(cmd)
        print('\n\n======================================================')

        try:
            # Parse current API response
            with open(tmp_path) as f:

                # Load query result
                data = json.load(f)

                # Display query status and error
                query_status = data.get('success')
                error = data.get('error')
                print(query_status)
                print(error)

                try:
                    # Save current items
                    for i in data['items']:
                        items.append(unfold('items', i))

                    # Retrive next markup
                    nextCursor = data['nextCursor']
                    cursorMark = nextCursor

                except KeyError:
                    os.remove(tmp_path)
                    break
        except json.decoder.JSONDecodeError:
            return {'data': 'None', 'dir': 'None',
                    'query_status': str(query_status), 'error': str(error)}

    # Write true csv
    full_path = dir_path + 'full.csv'
    items_to_csv(items, full_path)

    # Keep dcterms only
    items = [{k: clean_list(i[k]) for k in i if k in labels} for i in items]

    # Filter date
    items = parse_date(items)
    # if dates is not None:
    #     items = filter_dates(items, dates)

    # Test if any result
    print('[ + ] Items found:', len(items))
    if len(items) == 0:
        return {'data': 'None', 'dir': 'None',
                'query_status': str(query_status), 'error': str(error)}

    # Save data to csv
    output_path = dir_path + 'output.csv'
    items_to_csv(items, output_path)

    # Save data to json
    output_path = dir_path + 'output.json'
    with open(output_path, 'w') as f:
        json.dump(items, f)

    return {'data': items, 'dir': str(session),
            'query_status': query_status, 'error': error}
