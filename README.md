# Federated Learning Framework Benchmark (flbenchmark)

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

## Quick start
One command to start the evaluation
```
python -m flbenchmark tutorials/benchmark/config.json
```
There are the example configuration files for different frameworks in the ```tutorials/benchmark/example-config``` directory, feel free to open an issue in this repo if you encounter any problems.

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
