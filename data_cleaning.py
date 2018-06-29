import re
import copy


labels = ['items_id', 'items_title', 'items_country', 'items_dataProvider',
          'items_type', 'items_edmTimespanLabelLangAware_def',
          'items_dcCreator', 'items_edmPreview']


# new_labels = {
#     'items_dataProvider': 'provider_name',
#     'items_country': 'provider_country',
#     'items_dcCreator': 'creator',
#     'items_edmPreview': 'preview',
#     'items_type': 'type',
#     'items_title': 'title',
#     'items_id': 'id',
#     'items_edmTimespanLabelLangAware_def': 'creation_date'
# }

def add_missing_columns(items):
    new_items = copy.deepcopy(items)

    for i in range(len(items)):
        c_labels = set(items[i].keys())
        missing = set(labels).difference(c_labels)

        for m in missing:
            new_items[i].update({m: ''})

    return new_items


def clean_list(value):
    '''
        When multiple values in on row, join
    '''
    if isinstance(value, list):
        return ' '.join(value)
    else:
        return value


def parse_date(items):
    '''
        Keep element that looks like a date
    '''
    new_items = copy.deepcopy(items)
    for i in range(len(items)):
        ints = re.findall('\d+', items[i]['items_edmTimespanLabelLangAware_def'])
        if len(ints) > 0:
            try:
                date = max(ints, key=len)
                date = int(date)
            except Exception:
                date = -1
        else:
            date = -1

        new_items[i]['items_edmTimespanLabelLangAware_def'] = date

    return new_items


def parse_user_dates(usr_data):
    '''
        Parse user date inputs

        Return false if problem during parsing,
        else return parsed values
    '''
    if usr_data['from'] == '':
        usr_from = 0
    else:
        try:
            usr_from = int(usr_data['from'])
        except Exception:
            usr_from = 0

    if usr_data['to'] == '' or not isinstance(usr_data['to'], int):
        usr_to = 3000
    else:
        try:
            usr_to = int(usr_data['to'])
        except Exception:
            usr_to = 0

    return {'from': usr_from, 'to': usr_to}
