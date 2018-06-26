import json
import csv
import argparse


def unfold_list(base_key, l):
    new_dict = dict()
    for i, val in enumerate(l):
        if isinstance(val, dict):
            new_k = base_key + '_' + str(i)
            new_dict.update(unfold(new_k, val))
        else:
            new_dict[base_key] = l
    return new_dict


def unfold(base_key, d):
    new_dict = dict()

    for k in d:
        new_k = base_key + '_' + k
        if isinstance(d[k], dict):
            new_dict.update(unfold(new_k, d[k]))
        elif isinstance(d[k], list):
            new_dict.update(unfold_list(new_k, d[k]))
        else:
            new_dict[new_k] = d[k]
    return new_dict


def json_to_csv(json_path):
    '''
        Turns json file to csv
    '''
    csv_path = json_path[:-4] + 'csv'

    with open(json_path) as f:
        unfolded = []
        header = set()
        items = json.load(f)['items']

        for i in items:
            # unfold row
            row = unfold('item', i)
            unfolded.append(row)

            # Update header
            header.update(list(row.keys()))

    # Write data to csv
    with open(csv_path, 'w') as f:
        header = list(header)
        writer = csv.DictWriter(f, fieldnames=header)

        writer.writeheader()
        writer.writerows(unfolded)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert a europeana \
                                                 json file to csv')
    parser.add_argument('json_path', type=str, help='path to your json file')
    args = parser.parse_args()

    if args.json_path.endswith('.json'):
        json_path = args.json_path
        json_to_csv(json_path)
