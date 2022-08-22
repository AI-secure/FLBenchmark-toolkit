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
- [How to support a custom framework](tutorials/how_to_support_a_custom_framework)
- [How to load datasets from our toolkit](tutorials/1.How_to_set_up_datasets.ipynb)
- [How to convert datasets to csv format](tutorials/2.Convert_to_csv.ipynb)
- [How to use our logging system and get the report](tutorials/logging)

## Quick start
One command to start the evaluation
```
python -m flbenchmark tutorials/benchmark/config.json
```
Note: This command will automatically download the docker images of the corresponding framework from [our repo in Docker Hub](https://hub.docker.com/r/flbenchmark/frameworks/tags).

Here is one example of the configuration file. You can change the configuration file to evaluate different frameworks with different datasets, algorithms, model, training parameters, etc.
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

# Supported frameworks
| Framework | Version (Git Commit Hash) | Docker Image |
| :---: | :---: | :---: |
| FATE | [018d051f06298cd01aec957d569ff5760ff0070e](https://github.com/FederatedAI/FATE/tree/018d051f06298cd01aec957d569ff5760ff0070e) | [flbenchmark/frameworks:fate](https://hub.docker.com/layers/frameworks/flbenchmark/frameworks/fate/images/sha256-954ae2bd23bcfd5323dee47b086764c25b5abc0a699b13bd90d92d4e3852a426) |
| FedML | [2ee0517a7fa9ec7d6a5521fbae3e17011683eecd](https://github.com/FedML-AI/FedML/tree/2ee0517a7fa9ec7d6a5521fbae3e17011683eecd) | [flbenchmark/frameworks:fedml](https://hub.docker.com/layers/frameworks/flbenchmark/frameworks/fedml/images/sha256-51e25eb32ac4ca5d18c2dcd34849b16339984f6a644255c2d4c31d959e4c071a) |
| PaddleFL | [e949f194aec03d1d2e26530f6bf6f4e83026eb2d](https://github.com/PaddlePaddle/PaddleFL/tree/e949f194aec03d1d2e26530f6bf6f4e83026eb2d) | [flbenchmark/frameworks:paddlefl](https://hub.docker.com/layers/frameworks/flbenchmark/frameworks/paddlefl/images/sha256-aadbf2ed4aa6f21921ee0229f9865fcbd7791cfe22fa7c68e484aa2f0163d5d0) |
| Fedlearner | [981ba5ad72bd6103251ec270525b52145e477df0](https://github.com/bytedance/fedlearner/tree/981ba5ad72bd6103251ec270525b52145e477df0) | [flbenchmark/frameworks:fedlearner](https://hub.docker.com/layers/frameworks/flbenchmark/frameworks/fedlearner/images/sha256-bfd38847d19343a5c5b15c62be453d8f5f7f03ca4a632f82862426f4aab643f2) |
| TFF | [a98b5ed6894c536549da06b4cc7ed116105dfe65](https://github.com/tensorflow/federated/tree/a98b5ed6894c536549da06b4cc7ed116105dfe65) | [flbenchmark/frameworks:tff](https://hub.docker.com/layers/frameworks/flbenchmark/frameworks/tff/images/sha256-c50866bc92ab595b9ea14215d7a0704d890591846f4d293acd9e377cc6d4f5ff) |
| Flower | [0b9a05386e2111a9b14c19d4d6ede8f34a3ed4a2](https://github.com/adap/flower/tree/0b9a05386e2111a9b14c19d4d6ede8f34a3ed4a2) | [flbenchmark/frameworks:flower](https://hub.docker.com/layers/frameworks/flbenchmark/frameworks/flower/images/sha256-e39aecb85315f3a4131b3240c6264eeb0ddec58e26af812f3060e5409915ba6c) |
| FLUTE | [b0ee9cc995622ca5b98202a6c40824612854875e](https://github.com/microsoft/msrflute/tree/b0ee9cc995622ca5b98202a6c40824612854875e) | [flbenchmark/frameworks:flute](https://hub.docker.com/layers/frameworks/flbenchmark/frameworks/flute/images/sha256-3c302d8afbfe3ebac9a81e49b99287cabbe65a0e8e4f8befc6184a8540087769) |
| CrypTen | [49f2fb2cdad8c7620b4db62fda0d18553f0836c0](https://github.com/facebookresearch/CrypTen/tree/49f2fb2cdad8c7620b4db62fda0d18553f0836c0) | [flbenchmark/frameworks:crypten](https://hub.docker.com/layers/frameworks/flbenchmark/frameworks/crypten/images/sha256-50b603e3ec2874cfdfdfe5bade12af6c60038e7e577fac4e3fb295a876c4afb5) |
| FedTree | [d9c0b0896343938e75563d1a8f8f632bd12ecc82](https://github.com/Xtra-Computing/FedTree/tree/d9c0b0896343938e75563d1a8f8f632bd12ecc82) | [flbenchmark/frameworks:fedtree](https://hub.docker.com/layers/frameworks/flbenchmark/frameworks/fedtree/images/sha256-94fa3085a8e5c97c1e60359aa105fa27ee57573278fecaa3b76df21cbaba436f) |
| FederatedScope | [5b2bb38675f3ab91b6282e0efb158a28ce6aa16d](https://github.com/alibaba/FederatedScope/tree/5b2bb38675f3ab91b6282e0efb158a28ce6aa16d) | [flbenchmark/frameworks:federatedscope](https://hub.docker.com/layers/frameworks/flbenchmark/frameworks/federatedscope/images/sha256-026f4ec1e9600df1e347422aeeed796b5ea7e34df38666a7198e0f44ef8d7fab) |
| FedScale | [97e05670a12da75cec2212b6b6f2c967842a733b](https://github.com/SymbioticLab/FedScale/tree/97e05670a12da75cec2212b6b6f2c967842a733b) | [flbenchmark/frameworks:fedscale](https://hub.docker.com/layers/frameworks/flbenchmark/frameworks/fedscale/images/sha256-4c320e3deec043cbd85c70ead42e728a36eafb9c68d3e17b4884e7712dd55fad) |

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
