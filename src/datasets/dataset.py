import json
import os
from typing import List


class Party:
    def __init__(self,
                 name: str,
                 column_name: List[str],
                 records: List[List],  # List[List[str/int/list]]
                 # FIXME group_id? hierarchies are dropped by leaf in split_data.py, unknown reasons
                 ):
        self.name = name
        self.column_name = column_name
        self.records = records

    def to_json(self):
        return json.dumps(self, indent=4, default=lambda x: x.__dict__)


class Dataset:
    def __init__(self,
                 name: str,
                 type: int,  # horizontal(0) / vertical(1)
                 label_name: str,
                 parties: List[Party],  # convert to List[party.name] before save to json file
                 options: dict = None,  # options
                 ):
        self.name = name
        self.type = type
        self.label_name = label_name
        self.parties = parties
        self.options = options

    def to_json(self):
        dataset_to_json = Dataset(self.name, self.type, self.label_name, [party.name for party in self.parties], self.options)
        return json.dumps(dataset_to_json, indent=4, default=lambda x: x.__dict__)


def load_from_json(in_dir):
    if not os.path.exists(in_dir):
        return None
    with open(os.path.join(in_dir, '_main.json'), 'r') as infile:
        dataset = json.load(infile)
    parties = []
    for party_name in dataset['parties']:
        with open(os.path.join(in_dir, party_name+'.json'), 'r') as infile:
            party = json.load(infile)
            parties.append(Party(party['name'], party['column_name'], party['records']))
    return Dataset(dataset['name'], dataset['type'], dataset['label_name'], parties, dataset['options'])


def save_to_json(dataset, out_dir):
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    with open(os.path.join(out_dir, '_main.json'), 'w') as outfile:
        outfile.write(dataset.to_json())
    for party in dataset.parties:
        with open(os.path.join(out_dir, party.name+'.json'), 'w') as outfile:
            outfile.write(party.to_json())
