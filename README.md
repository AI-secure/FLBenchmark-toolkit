# Federated Learning Framework Benchmark (UniFed)

**🌟For the benchmark result📊, please check our [website](https://unifedbenchmark.github.io/).👈👈👈**

![image](https://unifedbenchmark.github.io/images/workflow-design.png)


# Installation
## Requirements
- Python  
Recommend to use `Python 3.9`. It should also work on `Python>=3.6`, feel free to contact us if you encounter any problems.  
You can set up a sandboxed python environment by conda easily: ```conda create -n flbenchmark python=3.9```  
- Command line tools: ```git```, ```wget```, ```unzip```
- [Docker Engine](https://docs.docker.com/engine/)
- [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html#docker) if you want to use GPU.

## Install From PyPI
```
pip install flbenchmark colink
```

# Launch a benchmark (manual deployment)
## Set up servers
We highly recommend to use Ubuntu 20.04 LTS.
- Download [install.sh](controller/install.sh) on home directory.
- Change `SERVER_IP="172.16.1.1"` in [install.sh](controller/install.sh) to corresponding server ip.
- Execute [install.sh](controller/install.sh).
- Record all servers' ip and `~/server/host_token.txt` in the following json format.
```json
{
    "test-0": [
        "http://172.31.4.48:80",
        "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwcml2aWxlZ2UiOiJob3N0IiwidXNlcl9pZCI6IjAyMGJhNzkyNzk0ZTlmMWUwZWZmNTEyOGM4NDdjZmE0MmRlNTllY2I1ODM4MzU4MDBmN2QwMzM1Yzg2YWFjZTViOSIsImV4cCI6MTY4OTM0ODAyM30.UP5JUYdbL-MkZDTSVuBHnIHoun1VkfcRgsBLV119v6A"
    ],
    "test-1": [
        "http://172.31.15.143:80",
        "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwcml2aWxlZ2UiOiJob3N0IiwidXNlcl9pZCI6IjAyNzJhNjgxNDg0NDMwNTFmZTI2NDFlYmZiNjM2MDgxODM5YmQ5NDdkZGFhNTcwYjY3MjU0MTI2NjU5YzBmZjVjYSIsImV4cCI6MTY4OTM0ODAzNH0.2HHQYzcMjif0ZkhSyltlOSC1ydsgWS8H_no5wWvohw0"
    ]
}
```

## Set up the framework
- Change the working directory to [exp](exp) for later steps.
- Put the json file about servers from last step to [exp/server_list.json](exp/server_list.json).
- Register users via `python register_users.py` and record the user id for later use.
- Launch corresponding frameworks `./start_po.a unifed.crypten https://github.com/CoLearn-Dev/colink-unifed-crypten.git`.

## Launch a benchmark
- Generate the [exp/config.json](exp/config.json) from [wizard](https://unifed-wizard.colearn.cloud/). Remember to replace the `user_id` with the user id you got from previous steps.
- Launch the benchmark via `python run_task.py`


# Launch a benchmark (auto deployment on AWS with a controller)
## Set up the controller
- Set up a web server(e.g. Apache2, Nginx, PHP built-in web server) with PHP support with files on [controller](controller) folder.
- Change `CONTROLLER_URL="http://172.31.2.2"` in [install_auto.sh](controller/install_auto.sh) to the controller's web url.

## Launch servers
- Launch servers on AWS and set the [user data](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/user-data.html) to the following script. (remember to replace the `http://172.31.2.2` with the controller's web url)
```
#!/bin/bash
sudo -i -u ubuntu << EOF
echo "Hello World" > testfile.txt
wget http://172.31.2.2/install_auto.sh
bash install_auto.sh > user_data.out
EOF
```
- Wait for server setups, when it finished you could see all servers' ip under [controller/servers](controller/servers).
- Get server list via `python get_server_list.py`, and copy the `server_list.json` to [exp](exp) folder.

## Set up the framework
- Change the working directory to [exp](exp) for later steps.
- Register users via `python register_users.py`.
- Launch corresponding frameworks `./start_po.a unifed.flower https://github.com/CoLearn-Dev/colink-unifed-flower.git`.

## Launch a benchmark
- Generate the [exp/config_auto.json](exp/config_auto.json) from [wizard](https://unifed-wizard.colearn.cloud/).
- Launch the benchmark via `python run_task_auto.py`


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

# License
This project is licensed under Apache License Version 2.0. By contributing to the project, you agree to the license and copyright terms therein and release your contribution under these terms.
