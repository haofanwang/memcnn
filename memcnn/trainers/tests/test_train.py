import pytest
from memcnn.train import run_experiment, main
import os
import sys


def test_main(tmp_path):
    sys.argv = ['train.py', 'cifar10', 'resnet34', '--fresh', '--no-cuda', '--workers=0']
    data_dir = str(tmp_path / "tmpdata")
    results_dir = str(tmp_path / "resdir")
    os.makedirs(data_dir)
    os.makedirs(results_dir)
    with pytest.raises(KeyError):
        main(data_dir=data_dir, results_dir=results_dir)


def dummy_dataloaders(*args, **kwargs):
    return None, None


def dummy_trainer(manager, *args, **kwargs):
    manager.save_train_state(2)


class DummyDataset(object):
    def __init__(self, *args, **kwargs):
        pass


content = '{' \
           '    "testsetup":' \
           '    {' \
           '        "data_loader_params": {},' \
           '        "model": "torch.nn.Conv2d",' \
           '        "model_params": {' \
           '            "in_channels":1,' \
           '            "out_channels":1,' \
           '            "kernel_size":1' \
           '        },' \
           '        "optimizer": "torch.optim.SGD",' \
           '        "optimizer_params": {' \
           '            "lr":0.1' \
           '        },' \
           '        "trainer": "memcnn.trainers.tests.test_train.dummy_trainer",' \
           '        "trainer_params":{},' \
           '        "data_loader": "memcnn.trainers.tests.test_train.dummy_dataloaders",' \
           '        "data_loader_params": {"dataset": "memcnn.trainers.tests.test_train.DummyDataset", "workers":0}' \
           '    }' \
           '}'


def test_run_experiment(tmp_path):
    exptags = ['testsetup']
    exp_file2 = str(tmp_path / "exp_file2")
    data_dir = str(tmp_path / "tmpdata")
    results_dir = str(tmp_path / "resdir")
    with open(exp_file2, 'w') as f2:
        f2.write(content)

    start_fresh = True
    use_cuda = False
    workers = None

    with pytest.raises(RuntimeError):
        run_experiment(exptags, data_dir, results_dir, start_fresh, use_cuda, workers, exp_file2)
    os.makedirs(data_dir)
    with pytest.raises(RuntimeError):
        run_experiment(exptags, data_dir, results_dir, start_fresh, use_cuda, workers, exp_file2)
    os.makedirs(results_dir)
    run_experiment(exptags, data_dir, results_dir, start_fresh, use_cuda, workers, exp_file2)
    run_experiment(exptags, data_dir, results_dir, False, use_cuda, workers, exp_file2)