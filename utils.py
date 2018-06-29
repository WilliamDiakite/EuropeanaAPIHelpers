import csv


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
    '''
        Quick function to store list of dicts into csv file
    '''
    with open(path, 'w') as f:
        header = get_available_labels(items)
        writer = csv.DictWriter(f, fieldnames=list(header))
        writer.writeheader()
        writer.writerows(items)
