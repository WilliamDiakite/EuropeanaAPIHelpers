import re
import csv
import copy


def clean_list(value):
    if isinstance(value, list):
        return ' '.join(value)
    else:
        return value


def get_available_labels(items):
    '''
        Look at every items available labels
        Return:
            labels: list of available labels
    '''
    labels = []
    for i in items:
        for k in i:
            labels.append(k)

    return list(set(labels))


def items_to_csv(items, path):
    with open(path, 'w') as f:
        header = get_available_labels(items)
        writer = csv.DictWriter(f, fieldnames=list(header))
        writer.writeheader()
        writer.writerows(items)


def filter(items, filters):
    '''
        Filter output (with author name, venue, etc.)

        Parameters
            - items: list of dicts
            - filters: dict of filter
        Return
            - new_items: filtered dataset (items)
    '''
    new_items = [copy.deepcopy(i) for i in items]
    to_remove = []
    for i in range(len(items)):
        for f in filters:
            if len(filters[f]) > 0 and filters[f] != items[i][f]:
                to_remove.append(items[i])

    for i in to_remove:
        new_items.remove(i)

    return new_items


def parse_date(items):
    new_items = []

    for i in items:
        try:
            date = i['items_edmTimespanLabelLangAware_def']
            date = date.split(' ')[0]
        except KeyError:
            date = '-1'

        new_item = copy.deepcopy(i)
        new_item.update({'items_edmTimespanLabelLangAware_def': date})
        new_items.append(new_item)
    return new_items


def filter_dates(items, dates):
    new_items = [copy.deepcopy(i) for i in items]
    to_remove = []

    date_from = int(dates[0])
    date_to = int(dates[1])

    for i in items:
        c_date = i['items_edmTimespanLabelLangAware_def']

        if str(c_date)[-1] == 's':
            ''' ie. 1960s '''
            c_date = int(re.search(r'\d+', c_date).group())

        if str(c_date)[-2:] == '..':
            ''' ie. 20.. '''
            c_date = c_date[:-2] + '00'
            c_date = int(c_date)
            if c_date < date_from or c_date > date_to:
                to_remove.append(i)

        elif c_date == -1:
            to_remove.append(i)

        else:
            if isinstance(c_date, str):
                c_date = int(re.search(r'\d+', c_date).group())
            if c_date < date_from or c_date > date_to:
                to_remove.append(i)

    for i in to_remove:
        new_items.remove(i)

    return new_items
