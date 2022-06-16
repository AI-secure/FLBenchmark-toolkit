import os
import json
from collections import defaultdict
from .dataset import Dataset, Party
import base64
import subprocess

LEAF_SOURCE_CODE = 'https://github.com/stneng/leaf.git'
LEAF_SOURCE_CODE_COMMIT = '891b7e3627a1782dc7eee1e6747d7c0ce5c075e0'
DEFAULT_ARGS = {
    'celeba': '-s niid --sf 0.1 -k 5 -t sample --smplseed 1234567890 --spltseed 1234567890',
    'femnist': '-s niid --sf 0.05 -k 100 -t sample --smplseed 1234567890 --spltseed 1234567890',
    'reddit': '',
    'sent140': '--sf 0.5 -k 100 -s niid -t sample --smplseed 1234567890 --spltseed 1234567890',
    'shakespeare': '-s niid --sf 0.05 -k 64 -tf 0.9 -t sample --smplseed 1234567890 --spltseed 1234567890',
    'synthetic': '-s niid --sf 1.0 -k 5 -t sample --tf 0.6 --smplseed 1234567890 --spltseed 1234567890',
}


def read_dir(data_dir):
    # https://github.com/TalwalkarLab/leaf/blob/09ec454a5675e32e1f0546b456b77857fdece018/models/utils/model_utils.py#L29
    clients = []
    groups = []
    data = defaultdict(lambda: None)

    files = os.listdir(data_dir)
    files = [f for f in files if f.endswith('.json')]
    for f in files:
        file_path = os.path.join(data_dir, f)
        with open(file_path, 'r') as inf:
            cdata = json.load(inf)
        clients.extend(cdata['users'])
        if 'hierarchies' in cdata:
            groups.extend(cdata['hierarchies'])
        data.update(cdata['user_data'])

    clients = list(sorted(data.keys()))
    return clients, groups, data


def read_data(train_data_dir, test_data_dir):
    # https://github.com/TalwalkarLab/leaf/blob/09ec454a5675e32e1f0546b456b77857fdece018/models/utils/model_utils.py#L49
    train_clients, train_groups, train_data = read_dir(train_data_dir)
    test_clients, test_groups, test_data = read_dir(test_data_dir)

    assert train_clients == test_clients
    assert train_groups == test_groups

    return train_clients, train_groups, train_data, test_data


def download_leaf(leaf_dir):
    if os.path.exists(leaf_dir):
        return
    bash_cmd = 'git clone '+LEAF_SOURCE_CODE+' '+leaf_dir
    subprocess.run(bash_cmd, shell=True, check=True)
    bash_cmd = 'git checkout '+LEAF_SOURCE_CODE_COMMIT
    subprocess.run(bash_cmd, shell=True, cwd=leaf_dir, check=True)


def get_leaf_args(dataset):
    return DEFAULT_ARGS[dataset]


def preprocess_leaf(dataset, leaf_dir, args):
    bash_dir = os.path.join(leaf_dir, 'data', dataset)
    if dataset == 'synthetic':
        subprocess.run('python3 main.py -num-tasks 1000 -num-classes 5 -num-dim 60', shell=True, cwd=bash_dir, check=True)
    bash_cmd = 'bash preprocess.sh'+' '+args
    print(bash_cmd)
    subprocess.run(bash_cmd, shell=True, cwd=bash_dir, check=True)


def encode_image(leaf_dir, img_name):
    with open(os.path.join(leaf_dir, 'data', 'celeba', 'data', 'raw', 'img_align_celeba', img_name), 'rb') as f:
        b64 = base64.b64encode(f.read())
    return b64.decode('utf-8')


def convert_leaf(dataset, leaf_dir, args):
    train_data_dir = os.path.join(leaf_dir, 'data', dataset, 'data', 'train')
    test_data_dir = os.path.join(leaf_dir, 'data', dataset, 'data', 'test')
    users, groups, train_data, test_data = read_data(train_data_dir, test_data_dir)
    if dataset == 'reddit':
        _, _, val_data = read_dir(os.path.join(leaf_dir, 'data', dataset, 'data', 'val'))
    train_parties = []
    test_parties = []
    val_parties = []
    for user in users:
        train_num_records = len(train_data[user]['y'])
        if dataset in ['shakespeare', 'reddit', 'celeba']:
            train_num_columns = 2
        else:
            train_num_columns = len(train_data[user]['x'][0])+1
        train_column_name = ['y']+['x'+str(i) for i in range(train_num_columns-1)]
        if dataset in ['shakespeare', 'reddit']:
            train_records = [[train_data[user]['y'][i], train_data[user]['x'][i]] for i in range(train_num_records)]
        elif dataset == 'celeba':
            train_records = [[train_data[user]['y'][i], encode_image(
                leaf_dir, train_data[user]['x'][i])] for i in range(train_num_records)]
        else:
            train_records = [[train_data[user]['y'][i]]+train_data[user]['x'][i] for i in range(train_num_records)]
        train_parties.append(Party(user, train_column_name, train_records))

        test_num_records = len(test_data[user]['y'])
        if dataset in ['shakespeare', 'reddit', 'celeba']:
            test_num_columns = 2
        else:
            test_num_columns = len(test_data[user]['x'][0])+1
        test_column_name = ['y']+['x'+str(i) for i in range(test_num_columns-1)]
        if dataset in ['shakespeare', 'reddit']:
            test_records = [[test_data[user]['y'][i], test_data[user]['x'][i]] for i in range(test_num_records)]
        elif dataset == 'celeba':
            test_records = [[test_data[user]['y'][i], encode_image(
                leaf_dir, test_data[user]['x'][i])] for i in range(test_num_records)]
        else:
            test_records = [[test_data[user]['y'][i]]+test_data[user]['x'][i] for i in range(test_num_records)]
        test_parties.append(Party(user, test_column_name, test_records))

        if dataset == 'reddit':
            val_num_records = len(val_data[user]['y'])
            val_num_columns = 2
            val_column_name = ['y']+['x'+str(i) for i in range(val_num_columns-1)]
            val_records = [[val_data[user]['y'][i], val_data[user]['x'][i]] for i in range(val_num_records)]
            val_parties.append(Party(user, val_column_name, val_records))

    if dataset == 'reddit':
        train_dataset = Dataset(dataset, 0, 'y', train_parties, {'leaf_args': args})
        test_dataset = Dataset(dataset, 0, 'y', test_parties, {'leaf_args': args})
        val_dataset = Dataset(dataset, 0, 'y', val_parties, {'leaf_args': args})
        return train_dataset, test_dataset, val_dataset
    else:
        train_dataset = Dataset(dataset, 0, 'y', train_parties, {'leaf_args': args})
        test_dataset = Dataset(dataset, 0, 'y', test_parties, {'leaf_args': args})
        return train_dataset, test_dataset
