import os
import shutil
from .dataset import save_to_json, load_from_json
from .leaf import download_leaf, get_leaf_args, preprocess_leaf, convert_leaf
from .fate import download_convert_fate


class FLBDatasets:
    def __init__(self,
                 dir: str = None,
                 ):
        if dir is None:
            self.dir = './data'
        else:
            self.dir = os.path.expanduser(dir)

    def leafDatasets(self,
                     dataset: str,
                     leaf_dir: str = None,
                     leaf_args: str = None,
                     keep_leaf: bool = False
                     ):
        if leaf_args is None:
            leaf_args = get_leaf_args(dataset)
        if os.path.exists(os.path.join(self.dir, dataset)):
            train_dataset = load_from_json(os.path.join(self.dir, dataset, 'train'))
            test_dataset = load_from_json(os.path.join(self.dir, dataset, 'test'))
            if train_dataset.options['leaf_args'] != leaf_args or test_dataset.options['leaf_args'] != leaf_args:
                raise RuntimeError('specified arguments are different from the cache, please delete the cache and run again.')
            if dataset == 'reddit':
                val_dataset = load_from_json(os.path.join(self.dir, dataset, 'val'))
                return train_dataset, test_dataset, val_dataset
            return train_dataset, test_dataset
        if leaf_dir is None:
            leaf_dir = os.path.join(self.dir, '_leaf')
        else:
            leaf_dir = os.path.expanduser(leaf_dir)
        download_leaf(leaf_dir)
        preprocess_leaf(dataset, leaf_dir, leaf_args)
        if dataset == 'reddit':
            train_dataset, test_dataset, val_dataset = convert_leaf(dataset, leaf_dir, leaf_args)
            save_to_json(train_dataset, os.path.join(self.dir, dataset, 'train'))
            save_to_json(test_dataset, os.path.join(self.dir, dataset, 'test'))
            save_to_json(val_dataset, os.path.join(self.dir, dataset, 'val'))
            if not keep_leaf:
                shutil.rmtree(leaf_dir)
            return train_dataset, test_dataset, val_dataset
        train_dataset, test_dataset = convert_leaf(dataset, leaf_dir, leaf_args)
        save_to_json(train_dataset, os.path.join(self.dir, dataset, 'train'))
        save_to_json(test_dataset, os.path.join(self.dir, dataset, 'test'))
        if not keep_leaf:
            shutil.rmtree(leaf_dir)
        return train_dataset, test_dataset

    def fateDatasets(self,
                     dataset: str
                     ):
        if os.path.exists(os.path.join(self.dir, dataset)):
            train_dataset = load_from_json(os.path.join(self.dir, dataset, 'train'))
            test_dataset = load_from_json(os.path.join(self.dir, dataset, 'test'))
            return train_dataset, test_dataset
        train_dataset, test_dataset = download_convert_fate(dataset)
        save_to_json(train_dataset, os.path.join(self.dir, dataset, 'train'))
        if test_dataset is not None:
            save_to_json(test_dataset, os.path.join(self.dir, dataset, 'test'))
        return train_dataset, test_dataset
