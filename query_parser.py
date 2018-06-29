from urllib.parse import quote


def parse_query(usr_data):

    if all(x == '' for x in usr_data.values()):
        return None

    if usr_data['keywords'] != '':
        keywords = quote(usr_data['keywords'], safe='')
    if usr_data['creator'] != '':
        creator = '+who:' + quote(usr_data['creator'])
    if usr_data['places'] != '':
        places = '+where:' + quote(usr_data['places'])

    time = '+timestamp_created:[{}-01-01T00:00:0.000Z+TO+{}-01-01T00:00:00.000Z]'.format(
        usr_data['from'], usr_data['to'])

    query = 'https://www.europeana.eu/api/v2/search.json?wskey={}&rows=100' + \
        '&query={}{}{}{}'.format(usr_data['key'], keywords, creator, places, time)

    return query
