# Supporting custom framework

Our FL benchmark toolkit is designed to support all types of FL framework. For a customized framework or new frameworks that will be released in the future, here we provide the guide to integrate them and benchmark their performance.

## How to integrate a custom framework

To integrate a custom framework, one should provide a docker image that contains the environment to run the custom framework in the format of `Dockerfile` and also specify the execution entry. For examples, see [Dockerfile](./Dockerfile) and [demo.py](./demo.py). Specifically,
1. The Dockerfile should include the installation procedure for dependencies and also set an `ENTRYPOINT` script which we discuss in the next step.
2. The execution entry is usually a script that describes the complete training procedure.

In the workflow of the evaluation, the toolkit provides the configuration and the data folder before the execution of the execution entry script, then it runs the script, and collects logging results from the logging folder. To match the workflow, the execution entry script should 
1. First read from the configuration file to figure out the experiment details (see [#L8 in demo.py](./demo.py#L8)). The configuration file is placed in `/test/config.json` inside the docker. It includes the information about the evaluation, e.g., what dataset to use, how many epochs to train, the benchmark mode, etc. In local benchmark mode, the configuration file is the same as the configuration file that started the evaluation. And in remote benchmark mode, the configuration file on each node has an extra field `my_host_id` in `bench_param` to distinguish between different nodes. The programmer can also add other parameters in the `training_param` field and it will also be passed into the docker.
2. Then it loads the dataset with our [dataset interface](../1.How_to_set_up_datasets.ipynb). For efficiency, the programmer can assume that the `/data` folder already cached the required datasets (see [#L10 in demo.py](./demo.py#L10)).
3. At the end, it starts the training which generates the log using our [logging module](../logging/). The log should save in the `/test/log` folder inside the docker and the programmer should specify the log dir when initiating the logger (see [#L19 in demo.py](./demo.py#L19)).

In addition to the two files required above, the programmer can also create other files that might help the execution of the custom FL framework and include them in the Dockerfile.

To finish the integration for the custom framework, one should build the docker image. Ideally, the docker image should be named `flbenchmark/custom` with tag `framework-name` (please keep the image name as `flbenchmark/custom` and you can custom the `framework-name`).
```
docker build -t flbenchmark/custom:demo .  # here we use "demo" as the `framework-name`
```

## How to run the integrated custom framework

Once the docker image is created and built/distributed to all evaluation nodes, one can benchmark it with the toolkit.
In local benchmark mode, the evaluation node is the local host. In remote benchmark mode, the evaluation nodes are the hosts specified in `bench_param`.
And one should set the `framework` field in the configuration file as `custom:framework-name` to test the integration.
```
python -m flbenchmark config.json 
```
