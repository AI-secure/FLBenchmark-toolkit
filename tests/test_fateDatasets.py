import flbenchmark.datasets

flbd = flbenchmark.datasets.FLBDatasets('../data')


def test_motor_vertical():
    train_dataset, test_dataset = flbd.fateDatasets('motor_vertical')
    train_dataset_cached, test_dataset_cached = flbd.fateDatasets('motor_vertical')
    assert train_dataset.to_json() == train_dataset_cached.to_json()
    assert [party.to_json() for party in train_dataset.parties] == [party.to_json() for party in train_dataset_cached.parties]
    assert test_dataset == test_dataset_cached == None


def test_breast_vertical():
    train_dataset, test_dataset = flbd.fateDatasets('breast_vertical')
    train_dataset_cached, test_dataset_cached = flbd.fateDatasets('breast_vertical')
    assert train_dataset.to_json() == train_dataset_cached.to_json()
    assert [party.to_json() for party in train_dataset.parties] == [party.to_json() for party in train_dataset_cached.parties]
    assert test_dataset == test_dataset_cached == None


def test_breast_horizontal():
    train_dataset, test_dataset = flbd.fateDatasets('breast_horizontal')
    train_dataset_cached, test_dataset_cached = flbd.fateDatasets('breast_horizontal')
    assert train_dataset.to_json() == train_dataset_cached.to_json()
    assert [party.to_json() for party in train_dataset.parties] == [party.to_json() for party in train_dataset_cached.parties]
    assert test_dataset.to_json() == test_dataset_cached.to_json()
    assert [party.to_json() for party in test_dataset.parties] == [party.to_json() for party in test_dataset_cached.parties]


def test_default_credit_vertical():
    train_dataset, test_dataset = flbd.fateDatasets('default_credit_vertical')
    train_dataset_cached, test_dataset_cached = flbd.fateDatasets('default_credit_vertical')
    assert train_dataset.to_json() == train_dataset_cached.to_json()
    assert [party.to_json() for party in train_dataset.parties] == [party.to_json() for party in train_dataset_cached.parties]
    assert test_dataset == test_dataset_cached == None


def test_default_credit_horizontal():
    train_dataset, test_dataset = flbd.fateDatasets('default_credit_horizontal')
    train_dataset_cached, test_dataset_cached = flbd.fateDatasets('default_credit_horizontal')
    assert train_dataset.to_json() == train_dataset_cached.to_json()
    assert [party.to_json() for party in train_dataset.parties] == [party.to_json() for party in train_dataset_cached.parties]
    assert test_dataset.to_json() == test_dataset_cached.to_json()
    assert [party.to_json() for party in test_dataset.parties] == [party.to_json() for party in test_dataset_cached.parties]


def test_dvisits_vertical():
    train_dataset, test_dataset = flbd.fateDatasets('dvisits_vertical')
    train_dataset_cached, test_dataset_cached = flbd.fateDatasets('dvisits_vertical')
    assert train_dataset.to_json() == train_dataset_cached.to_json()
    assert [party.to_json() for party in train_dataset.parties] == [party.to_json() for party in train_dataset_cached.parties]
    assert test_dataset == test_dataset_cached == None


def test_give_credit_vertical():
    train_dataset, test_dataset = flbd.fateDatasets('give_credit_vertical')
    train_dataset_cached, test_dataset_cached = flbd.fateDatasets('give_credit_vertical')
    assert train_dataset.to_json() == train_dataset_cached.to_json()
    assert [party.to_json() for party in train_dataset.parties] == [party.to_json() for party in train_dataset_cached.parties]
    assert test_dataset.to_json() == test_dataset_cached.to_json()
    assert [party.to_json() for party in test_dataset.parties] == [party.to_json() for party in test_dataset_cached.parties]


def test_give_credit_horizontal():
    train_dataset, test_dataset = flbd.fateDatasets('give_credit_horizontal')
    train_dataset_cached, test_dataset_cached = flbd.fateDatasets('give_credit_horizontal')
    assert train_dataset.to_json() == train_dataset_cached.to_json()
    assert [party.to_json() for party in train_dataset.parties] == [party.to_json() for party in train_dataset_cached.parties]
    assert test_dataset.to_json() == test_dataset_cached.to_json()
    assert [party.to_json() for party in test_dataset.parties] == [party.to_json() for party in test_dataset_cached.parties]


def test_student_vertical():
    train_dataset, test_dataset = flbd.fateDatasets('student_vertical')
    train_dataset_cached, test_dataset_cached = flbd.fateDatasets('student_vertical')
    assert train_dataset.to_json() == train_dataset_cached.to_json()
    assert [party.to_json() for party in train_dataset.parties] == [party.to_json() for party in train_dataset_cached.parties]
    assert test_dataset == test_dataset_cached == None


def test_student_horizontal():
    train_dataset, test_dataset = flbd.fateDatasets('student_horizontal')
    train_dataset_cached, test_dataset_cached = flbd.fateDatasets('student_horizontal')
    assert train_dataset.to_json() == train_dataset_cached.to_json()
    assert [party.to_json() for party in train_dataset.parties] == [party.to_json() for party in train_dataset_cached.parties]
    assert test_dataset.to_json() == test_dataset_cached.to_json()
    assert [party.to_json() for party in test_dataset.parties] == [party.to_json() for party in test_dataset_cached.parties]


def test_vehicle_scale_vertical():
    train_dataset, test_dataset = flbd.fateDatasets('vehicle_scale_vertical')
    train_dataset_cached, test_dataset_cached = flbd.fateDatasets('vehicle_scale_vertical')
    assert train_dataset.to_json() == train_dataset_cached.to_json()
    assert [party.to_json() for party in train_dataset.parties] == [party.to_json() for party in train_dataset_cached.parties]
    assert test_dataset == test_dataset_cached == None


def test_vehicle_scale_horizontal():
    train_dataset, test_dataset = flbd.fateDatasets('vehicle_scale_horizontal')
    train_dataset_cached, test_dataset_cached = flbd.fateDatasets('vehicle_scale_horizontal')
    assert train_dataset.to_json() == train_dataset_cached.to_json()
    assert [party.to_json() for party in train_dataset.parties] == [party.to_json() for party in train_dataset_cached.parties]
    assert test_dataset == test_dataset_cached == None
