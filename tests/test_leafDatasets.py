import flbenchmark.datasets

flbd = flbenchmark.datasets.FLBDatasets('../data')


def test_sent140():
    train_dataset, test_dataset = flbd.leafDatasets('sent140', keep_leaf=True)
    train_dataset_cached, test_dataset_cached = flbd.leafDatasets('sent140', keep_leaf=True)
    assert train_dataset.to_json() == train_dataset_cached.to_json()
    assert [party.to_json() for party in train_dataset.parties] == [party.to_json() for party in train_dataset_cached.parties]
    assert test_dataset.to_json() == test_dataset_cached.to_json()
    assert [party.to_json() for party in test_dataset.parties] == [party.to_json() for party in test_dataset_cached.parties]


def test_celeba():
    train_dataset, test_dataset = flbd.leafDatasets('celeba', keep_leaf=True)
    train_dataset_cached, test_dataset_cached = flbd.leafDatasets('celeba', keep_leaf=True)
    assert train_dataset.to_json() == train_dataset_cached.to_json()
    assert [party.to_json() for party in train_dataset.parties] == [party.to_json() for party in train_dataset_cached.parties]
    assert test_dataset.to_json() == test_dataset_cached.to_json()
    assert [party.to_json() for party in test_dataset.parties] == [party.to_json() for party in test_dataset_cached.parties]


def test_reddit():
    train_dataset, test_dataset, val_dataset = flbd.leafDatasets('reddit', keep_leaf=True)
    train_dataset_cached, test_dataset_cached, val_dataset_cached = flbd.leafDatasets('reddit', keep_leaf=True)
    assert train_dataset.to_json() == train_dataset_cached.to_json()
    assert [party.to_json() for party in train_dataset.parties] == [party.to_json() for party in train_dataset_cached.parties]
    assert test_dataset.to_json() == test_dataset_cached.to_json()
    assert [party.to_json() for party in test_dataset.parties] == [party.to_json() for party in test_dataset_cached.parties]
    assert val_dataset.to_json() == val_dataset_cached.to_json()
    assert [party.to_json() for party in val_dataset.parties] == [party.to_json() for party in val_dataset_cached.parties]


def test_synthetic():
    train_dataset, test_dataset = flbd.leafDatasets('synthetic', keep_leaf=True)
    train_dataset_cached, test_dataset_cached = flbd.leafDatasets('synthetic', keep_leaf=True)
    assert train_dataset.to_json() == train_dataset_cached.to_json()
    assert [party.to_json() for party in train_dataset.parties] == [party.to_json() for party in train_dataset_cached.parties]
    assert test_dataset.to_json() == test_dataset_cached.to_json()
    assert [party.to_json() for party in test_dataset.parties] == [party.to_json() for party in test_dataset_cached.parties]


def test_shakespeare():
    train_dataset, test_dataset = flbd.leafDatasets('shakespeare', keep_leaf=True)
    train_dataset_cached, test_dataset_cached = flbd.leafDatasets('shakespeare', keep_leaf=True)
    assert train_dataset.to_json() == train_dataset_cached.to_json()
    assert [party.to_json() for party in train_dataset.parties] == [party.to_json() for party in train_dataset_cached.parties]
    assert test_dataset.to_json() == test_dataset_cached.to_json()
    assert [party.to_json() for party in test_dataset.parties] == [party.to_json() for party in test_dataset_cached.parties]


def test_femnist():
    train_dataset, test_dataset = flbd.leafDatasets('femnist', keep_leaf=True)
    train_dataset_cached, test_dataset_cached = flbd.leafDatasets('femnist', keep_leaf=True)
    assert train_dataset.to_json() == train_dataset_cached.to_json()
    assert [party.to_json() for party in train_dataset.parties] == [party.to_json() for party in train_dataset_cached.parties]
    assert test_dataset.to_json() == test_dataset_cached.to_json()
    assert [party.to_json() for party in test_dataset.parties] == [party.to_json() for party in test_dataset_cached.parties]
