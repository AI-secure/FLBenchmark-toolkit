# Federated Learning Framework Benchmark (UniFed)

**🌟For the benchmark result📊, please check our [website](https://unifedbenchmark.github.io/).👈👈👈**

![image](https://user-images.githubusercontent.com/23360163/174420954-9735b5e8-4f61-45bc-8cee-d878548d1035.png)


# Installation
## Requirements
- Python  
Recommend to use `Python 3.9`. It should also work on `Python>=3.6`, feel free to contact us if you encounter any problems.  
You can set up a sandboxed python environment by conda easily: ```conda create -n flbenchmark python=3.9```  
- Command line tools: ```git```, ```wget```, ```unzip```
- [Docker Engine](https://docs.docker.com/engine/)
- [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html#docker) if you want to use GPU.

## From PyPI
```
pip install flbenchmark
```

## From Source
Run this command in the project's home directory: ```pip install .```  

# Tutorials
There are comprehensive tutorials in the ```tutorials``` directory, and it's recommended to start notebooks in the ```tutorials``` directory.
- [How to start a benchmark with one command](tutorials/benchmark)
- [How to load datasets from our toolkit](tutorials/1.How_to_set_up_datasets.ipynb)
- [How to convert datasets to csv format](tutorials/2.Convert_to_csv.ipynb)
- [How to use our logging system and get the report](tutorials/logging)
- [How to support a custom framework](tutorials/how_to_support_a_custom_framework)

## Quick start
One command to start the evaluation
```
python -m flbenchmark tutorials/benchmark/config.json
```
Note: This command will automatically download the docker images of the corresponding framework from [our repo in Docker Hub](https://hub.docker.com/r/flbenchmark/frameworks/tags).

Here are the details about this configuration file.
```
{
    "framework": "crypten",
    "dataset": "breast_vertical",
    "algorithm": "mpc",
    "model": "mlp_128",
    "bench_param": {
        "mode": "local",
        "device": "cpu"
    },
    "training_param": {
        "epochs": 8,
        "batch_size": 100,
        "learning_rate": 0.1,
        "loss_func": "cross_entropy",
        "optimizer": "sgd",
        "optimizer_param": {
            "momentum": 0.9,
            "dampening": 0,
            "weight_decay": 0,
            "nesterov": false
        }
    }
}
```
There are more example configuration files for different frameworks in [tutorials/benchmark/example-config](tutorials/benchmark/example-config).  
The configuration files for the experiments in the paper are in [paper_experiments](paper_experiments).  
Feel free to open an issue in this repo if you encounter any problems.

# Evaluation Scenarios
## Cross-device horizontal
| Scenario name | Modality | Task type | Performance metrics | Client number | Sample number |
| :---: | :---: | :---: | :---: | ---: | ---: |
| celeba | Image | Binary Classification <br> (Smiling vs. Not smiling) | Accuracy | 894 | 20,028 |
| femnist | Image | Multiclass Classification <br> (62 classes) | Accuracy | 178 | 40,203 |
| reddit | Text | Next-word Prediction | Accuracy | 813 | 27,738 |
## Cross-silo horizontal
| Scenario name | Modality | Task type | Performance metrics | Client number | Sample number |
| :---: | :---: | :---: | :---: | ---: | ---: |
| breast_horizontal | Medical | Binary Classification | AUC | 2 | 569 |
| default_credit_horizontal | Tabular | Binary Classification | AUC | 2 | 22,000 |
| give_credit_horizontal | Tabular | Binary Classification | AUC | 2 | 150,000 |
| student_horizontal | Tabular | Regression <br> (Grade Estimation) | MSE | 2 | 395 |
| vehicle_scale_horizontal | Image | Multiclass Classification <br> (4 classes) | Accuracy | 2 | 846 |
## Cross-silo vertical
| Scenario name | Modality | Task type | Performance metrics | Vertical split details |
| :---: | :---: | :---: | :---: | :--- |
| breast_vertical | Medical | Binary Classification | AUC | A: 10 features 1 label <br> B: 20 features |
| default_credit_vertical | Tabular | Binary Classification | AUC | A: 13 features 1 label <br> B: 10 features |
| dvisits_vertical | Tabular | Regression <br> (Number of consultations Estimation) | MSE | A: 3 features 1 label <br> B: 9 features |
| give_credit_vertical | Tabular | Binary Classification | AUC | A: 5 features 1 label <br> B: 5 features |
| motor_vertical | Sensor data | Regression <br> (Temperature Estimation) | MSE | A: 4 features 1 label <br> B: 7 features |
| student_vertical | Tabular | Regression <br> (Grade Estimation) | MSE | A: 6 features 1 label <br> B: 7 features |
| vehicle_scale_vertical | Image | Multiclass Classification <br> (4 classes) | Accuracy | A: 9 features 1 label <br> B: 9 features |

# Maintenance Plans
- Add more frameworks
  - [x] FedScale
  - [x] FederatedScope
  - [ ] OpenFL
  - [ ] FLSim
  - [ ] Fed-BioMed
  - [ ] OpenFed
- Add more scenarios
  - [ ] larger-scale datasets (e.g. (Tiny)ImageNet) and control the heterogeneity with Dirichlet distribution
  - [ ] speech (e.g. SpeechCommands)
  - [ ] sensor data (e.g. HAR)
  - [ ] recommenders (e.g. TaoBao)
- Add more tasks
  - [ ] personalization


# License
This project is licensed under Apache License Version 2.0. By contributing to the project, you agree to the license and copyright terms therein and release your contribution under these terms.
