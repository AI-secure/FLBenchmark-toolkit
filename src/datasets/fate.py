import pandas as pd
from .dataset import Dataset, Party

FATE_DATA_URL = 'https://raw.githubusercontent.com/FederatedAI/FATE/12c25950633fdcc151b671760ff2529320a5ee79/examples/data/'
FATE_DATASETS = {
    'motor_vertical': [Dataset('motor_vertical', 1, 'motor_speed', ['motor_hetero_guest', 'motor_hetero_host'], {'unique_id': 'idx'}), None],
    'breast_vertical': [Dataset('breast_vertical', 1, 'y', ['breast_hetero_guest', 'breast_hetero_host'], {'unique_id': 'id'}), None],
    'breast_horizontal': [Dataset('breast_horizontal', 0, 'y', ['breast_homo_guest', 'breast_homo_host']),
                          Dataset('breast_horizontal', 0, 'y', ['breast_homo_test'])],
    'default_credit_vertical': [Dataset('default_credit_vertical', 1, 'y', ['default_credit_hetero_guest', 'default_credit_hetero_host'], {'unique_id': 'id'}), None],
    'default_credit_horizontal': [Dataset('default_credit_horizontal', 0, 'y', ['default_credit_homo_guest', 'default_credit_homo_host_1']),
                                  Dataset('default_credit_horizontal', 0, 'y', ['default_credit_homo_test'])],
    'dvisits_vertical': [Dataset('dvisits_vertical', 1, 'doctorco', ['dvisits_hetero_guest', 'dvisits_hetero_host'], {'unique_id': 'id'}), None],
    'give_credit_vertical': [Dataset('give_credit_vertical', 1, 'y', ['give_credit_hetero_guest', 'give_credit_hetero_host'], {'unique_id': 'id'}),
                             Dataset('give_credit_vertical', 1, 'y', ['give_credit_hetero_test', 'give_credit_hetero_host'], {'unique_id': 'id'})],
    'give_credit_horizontal': [Dataset('give_credit_horizontal', 0, 'y', ['give_credit_homo_guest', 'give_credit_homo_host']),
                               Dataset('give_credit_horizontal', 0, 'y', ['give_credit_homo_test'])],
    'student_vertical': [Dataset('student_vertical', 1, 'y', ['student_hetero_guest', 'student_hetero_host'], {'unique_id': 'id'}), None],
    'student_horizontal': [Dataset('student_horizontal', 0, 'y', ['student_homo_guest', 'student_homo_host']),
                           Dataset('student_horizontal', 0, 'y', ['student_homo_test'])],
    'vehicle_scale_vertical': [Dataset('vehicle_scale_vertical', 1, 'y', ['vehicle_scale_hetero_guest', 'vehicle_scale_hetero_host'], {'unique_id': 'id'}), None],
    'vehicle_scale_horizontal': [Dataset('vehicle_scale_horizontal', 0, 'y', ['vehicle_scale_homo_guest', 'vehicle_scale_homo_host']), None],
}


def download_convert_fate(fate_dataset_name):
    train_parties = []
    train_dataset = FATE_DATASETS[fate_dataset_name][0]
    for party_name in train_dataset.parties:
        df = pd.read_csv(FATE_DATA_URL+party_name+'.csv')
        n, m = df.shape
        values = [[df.iat[i, j].item() for j in range(m)] for i in range(n)]
        train_parties.append(Party(party_name, df.columns.tolist(), values))
    if fate_dataset_name == 'give_credit_vertical':
        train_parties[1].records = train_parties[1].records[:120000]
    train_dataset = Dataset(train_dataset.name, train_dataset.type, train_dataset.label_name, train_parties, train_dataset.options)

    if FATE_DATASETS[fate_dataset_name][1] is None:
        return train_dataset, None
    test_parties = []
    test_dataset = FATE_DATASETS[fate_dataset_name][1]
    for party_name in test_dataset.parties:
        df = pd.read_csv(FATE_DATA_URL+party_name+'.csv')
        n, m = df.shape
        values = [[df.iat[i, j].item() for j in range(m)] for i in range(n)]
        test_parties.append(Party(party_name, df.columns.tolist(), values))
    if fate_dataset_name == 'give_credit_vertical':
        test_parties[1].records = test_parties[1].records[120000:]
        test_parties[0].name = 'give_credit_hetero_guest'
    test_dataset = Dataset(test_dataset.name, test_dataset.type, test_dataset.label_name, test_parties, test_dataset.options)
    return train_dataset, test_dataset
