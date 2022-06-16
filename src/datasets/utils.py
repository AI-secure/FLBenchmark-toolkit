import os
import pandas as pd


def convert_to_csv(dataset, out_dir):
    out_dir = os.path.expanduser(out_dir)
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    with open(os.path.join(out_dir, '_main.json'), 'w') as outfile:
        outfile.write(dataset.to_json())
    for party in dataset.parties:
        df = pd.DataFrame(party.records, columns=party.column_name)
        df.to_csv(os.path.join(out_dir, party.name+'.csv'), index=False)
