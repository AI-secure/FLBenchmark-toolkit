from subprocess import DEVNULL
import sys
import json
import os
import subprocess
import time
import copy
import flbenchmark.datasets
import flbenchmark.logging


def remote_run(hostname, remote_bash_cmd):
    local_bash_cmd = 'ssh {} "{}"'.format(hostname, remote_bash_cmd)
    subprocess.run(local_bash_cmd, shell=True, stdout=DEVNULL, check=True)


def remote_push(hostname, local_file, remote_file):
    local_bash_cmd = 'scp {} {}:{}'.format(local_file, hostname, remote_file)
    subprocess.run(local_bash_cmd, shell=True, stdout=DEVNULL, check=True)


def remote_pull(hostname, remote_file, local_file):
    local_bash_cmd = 'scp {}:{} {}'.format(hostname, remote_file, local_file)
    subprocess.run(local_bash_cmd, shell=True, stdout=DEVNULL, check=True)


def start(config_file):
    config = json.load(open(config_file, 'r'))
    id = int(time.time())
    working_dir = os.path.expanduser('~/flbenchmark.working')
    raw_working_dir = '~/flbenchmark.working'
    if not os.path.exists(working_dir):
        os.makedirs(working_dir)
    data_dir = os.path.join(working_dir, 'data')
    raw_data_dir = os.path.join(raw_working_dir, 'data')
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    log_dir = os.path.join(working_dir, str(id), 'log')
    raw_log_dir = os.path.join(raw_working_dir, str(id), 'log')
    os.makedirs(log_dir)
    config_file = os.path.join(working_dir, str(id), 'config.json')
    raw_config_file = os.path.join(raw_working_dir, str(id), 'config.json')
    with open(config_file, 'w') as f:
        f.write(json.dumps(config, indent=4))

    if config['bench_param']['mode'] == 'remote':
        for host in config['bench_param']['hosts']:
            remote_bash_cmd = 'mkdir -p {}'.format(raw_data_dir)
            remote_run(host['hostname'], remote_bash_cmd)
            remote_bash_cmd = 'mkdir -p {}'.format(raw_log_dir)
            remote_run(host['hostname'], remote_bash_cmd)
            remote_config = copy.deepcopy(config)
            remote_config['bench_param']['my_host_id'] = host['id']
            tmp_file = config_file+'.tmp'
            with open(tmp_file, 'w') as f:
                f.write(json.dumps(remote_config, indent=4))
            remote_push(host['hostname'], tmp_file, raw_config_file)
        tmp_file = config_file+'.tmp'
        os.remove(tmp_file)

    if config['bench_param']['mode'] == 'local':
        prepare_dataset(config['dataset'])
        prepare_framework_image(config['framework'])
    elif config['bench_param']['mode'] == 'remote':
        for host in config['bench_param']['hosts']:
            remote_bash_cmd = 'python3 -m flbenchmark prepare_dataset {}'.format(config['dataset'])
            remote_run(host['hostname'], remote_bash_cmd)
            remote_bash_cmd = 'python3 -m flbenchmark prepare_framework_image {}'.format(config['framework'])
            remote_run(host['hostname'], remote_bash_cmd)

    docker_cmd = 'docker run -dit --rm '
    debug_flag = os.environ.get('FLB_DEBUG', 'false').lower() == 'true'
    docker_stats_flag = os.environ.get('FLB_DOCKER_STATS', 'false').lower() == 'true'
    if debug_flag:
        docker_cmd = 'docker run -it --rm '
    if os.environ.get('FLB_GROUP') is None:
        if config['bench_param']['device'] == 'gpu':
            docker_cmd += '--gpus all '
    else:
        group_id = int(os.environ.get('FLB_GROUP'))
        docker_cmd += '--cpuset-cpus {}-{} '.format(group_id*20, (group_id+1)*20-1)
        if config['bench_param']['device'] == 'gpu':
            docker_cmd += '--gpus \'"device={},{}"\' '.format(group_id*2, group_id*2+1)
        print(docker_cmd)

    if config['framework'] == 'crypten':
        if config['bench_param']['mode'] == 'local':
            if config['bench_param']['device'] == 'cpu':
                bash_cmd = docker_cmd+'-v {}:/data -v {}:/test/log -v {}:/test/config.json flbenchmark/frameworks:crypten'.format(
                    raw_data_dir, raw_log_dir, raw_config_file)
            elif config['bench_param']['device'] == 'gpu':
                bash_cmd = docker_cmd+'-v {}:/data -v {}:/test/log -v {}:/test/config.json flbenchmark/frameworks:crypten'.format(
                    raw_data_dir, raw_log_dir, raw_config_file)
            else:
                raise NotImplementedError('Device {} is not supported.'.format(config['bench_param']['device']))
        elif config['bench_param']['mode'] == 'remote':
            for host in config['bench_param']['hosts']:
                if config['bench_param']['device'] == 'cpu':
                    remote_bash_cmd = docker_cmd+'--net=host -v {}:/data -v {}:/test/log -v {}:/test/config.json flbenchmark/frameworks:crypten'.format(
                        raw_data_dir, raw_log_dir, raw_config_file)
                elif config['bench_param']['device'] == 'gpu':
                    remote_bash_cmd = docker_cmd+'--net=host -v {}:/data -v {}:/test/log -v {}:/test/config.json flbenchmark/frameworks:crypten'.format(
                        raw_data_dir, raw_log_dir, raw_config_file)
                else:
                    raise NotImplementedError('Device {} is not supported.'.format(config['bench_param']['device']))
                remote_run(host['hostname'], remote_bash_cmd)
            print('The benchmark has started, and you can use `python -m flbenchmark get_report {}` to query the report.'.format(id))
        else:
            raise NotImplementedError('Mode {} is not supported.'.format(config['bench_param']['mode']))
    elif config['framework'] == 'fate':
        if config['bench_param']['mode'] == 'local':
            if config['bench_param']['device'] == 'cpu':
                bash_cmd = docker_cmd+'-v {}:/data -v {}:/test/log -v {}:/test/config.json flbenchmark/frameworks:fate'.format(
                    raw_data_dir, raw_log_dir, raw_config_file)
            elif config['bench_param']['device'] == 'gpu':
                bash_cmd = docker_cmd+'-v {}:/data -v {}:/test/log -v {}:/test/config.json flbenchmark/frameworks:fate'.format(
                    raw_data_dir, raw_log_dir, raw_config_file)
            else:
                raise NotImplementedError('Device {} is not supported.'.format(config['bench_param']['device']))
        else:
            raise NotImplementedError('Mode {} is not supported.'.format(config['bench_param']['mode']))
    elif config['framework'] == 'flute':
        if config['bench_param']['mode'] == 'local':
            if config['bench_param']['device'] == 'cpu':
                bash_cmd = docker_cmd+'-v {}:/data -v {}:/msrflute/log -v {}:/test/config.json flbenchmark/frameworks:flute'.format(
                    raw_data_dir, raw_log_dir, raw_config_file)
            elif config['bench_param']['device'] == 'gpu':
                bash_cmd = docker_cmd+'-v {}:/data -v {}:/msrflute/log -v {}:/test/config.json flbenchmark/frameworks:flute'.format(
                    raw_data_dir, raw_log_dir, raw_config_file)
            else:
                raise NotImplementedError('Device {} is not supported.'.format(config['bench_param']['device']))
        else:
            raise NotImplementedError('Mode {} is not supported.'.format(config['bench_param']['mode']))
    elif config['framework'] == 'fedlearner':
        if config['bench_param']['mode'] == 'local':
            if config['bench_param']['device'] == 'cpu':
                bash_cmd = docker_cmd+'-v {}:/data -v {}:/test/log -v {}:/test/config.json flbenchmark/frameworks:fedlearner'.format(
                    raw_data_dir, raw_log_dir, raw_config_file)
            elif config['bench_param']['device'] == 'gpu':
                bash_cmd = docker_cmd+'-v {}:/data -v {}:/test/log -v {}:/test/config.json flbenchmark/frameworks:fedlearner'.format(
                    raw_data_dir, raw_log_dir, raw_config_file)
            else:
                raise NotImplementedError('Device {} is not supported.'.format(config['bench_param']['device']))
        else:
            raise NotImplementedError('Mode {} is not supported.'.format(config['bench_param']['mode']))
    elif config['framework'] == 'fedml':
        if config['bench_param']['mode'] == 'local':
            if config['bench_param']['device'] == 'cpu':
                bash_cmd = docker_cmd+'-v {}:/data -v {}:/FedML/log -v {}:/FedML/config.json flbenchmark/frameworks:fedml'.format(
                    raw_data_dir, raw_log_dir, raw_config_file)
            elif config['bench_param']['device'] == 'gpu':
                bash_cmd = docker_cmd+'-v {}:/data -v {}:/FedML/log -v {}:/FedML/config.json flbenchmark/frameworks:fedml'.format(
                    raw_data_dir, raw_log_dir, raw_config_file)
            else:
                raise NotImplementedError('Device {} is not supported.'.format(config['bench_param']['device']))
        else:
            raise NotImplementedError('Mode {} is not supported.'.format(config['bench_param']['mode']))
    elif config['framework'] == 'tff':
        if config['bench_param']['mode'] == 'local':
            if config['bench_param']['device'] == 'cpu':
                bash_cmd = docker_cmd+'-v {}:/data -v {}:/test/log -v {}:/test/config.json flbenchmark/frameworks:tff'.format(
                    raw_data_dir, raw_log_dir, raw_config_file)
            elif config['bench_param']['device'] == 'gpu':
                bash_cmd = docker_cmd+'-v {}:/data -v {}:/test/log -v {}:/test/config.json flbenchmark/frameworks:tff'.format(
                    raw_data_dir, raw_log_dir, raw_config_file)
            else:
                raise NotImplementedError('Device {} is not supported.'.format(config['bench_param']['device']))
        else:
            raise NotImplementedError('Mode {} is not supported.'.format(config['bench_param']['mode']))
    elif config['framework'] == 'flower':
        if config['bench_param']['mode'] == 'local':
            if config['bench_param']['device'] == 'cpu':
                bash_cmd = docker_cmd+'-v {}:/data -v {}:/test/log -v {}:/test/config.json flbenchmark/frameworks:flower'.format(
                    raw_data_dir, raw_log_dir, raw_config_file)
            elif config['bench_param']['device'] == 'gpu':
                bash_cmd = docker_cmd+'-v {}:/data -v {}:/test/log -v {}:/test/config.json flbenchmark/frameworks:flower'.format(
                    raw_data_dir, raw_log_dir, raw_config_file)
            else:
                raise NotImplementedError('Device {} is not supported.'.format(config['bench_param']['device']))
        else:
            raise NotImplementedError('Mode {} is not supported.'.format(config['bench_param']['mode']))
    elif config['framework'] == 'paddlefl':
        if config['bench_param']['mode'] == 'local':
            if config['bench_param']['device'] == 'cpu':
                bash_cmd = docker_cmd+'-v {}:/data -v {}:/test/log -v {}:/test/config.json flbenchmark/frameworks:paddlefl'.format(
                    raw_data_dir, raw_log_dir, raw_config_file)
            elif config['bench_param']['device'] == 'gpu':
                bash_cmd = docker_cmd+'-v {}:/data -v {}:/test/log -v {}:/test/config.json flbenchmark/frameworks:paddlefl'.format(
                    raw_data_dir, raw_log_dir, raw_config_file)
            else:
                raise NotImplementedError('Device {} is not supported.'.format(config['bench_param']['device']))
        else:
            raise NotImplementedError('Mode {} is not supported.'.format(config['bench_param']['mode']))
    elif config['framework'] == 'fedtree':
        if config['bench_param']['mode'] == 'local':
            if config['bench_param']['device'] == 'cpu':
                bash_cmd = docker_cmd+'-v {}:/data -v {}:/test/log -v {}:/test/config.json flbenchmark/frameworks:fedtree'.format(
                    raw_data_dir, raw_log_dir, raw_config_file)
            elif config['bench_param']['device'] == 'gpu':
                bash_cmd = docker_cmd+'-v {}:/data -v {}:/test/log -v {}:/test/config.json flbenchmark/frameworks:fedtree'.format(
                    raw_data_dir, raw_log_dir, raw_config_file)
            else:
                raise NotImplementedError('Device {} is not supported.'.format(config['bench_param']['device']))
        else:
            raise NotImplementedError('Mode {} is not supported.'.format(config['bench_param']['mode']))
    elif config['framework'].startswith('custom:'):
        if config['bench_param']['mode'] == 'local':
            if config['bench_param']['device'] == 'cpu':
                bash_cmd = docker_cmd+'-v {}:/data -v {}:/test/log -v {}:/test/config.json flbenchmark/{}'.format(
                    raw_data_dir, raw_log_dir, raw_config_file, config['framework'])
            elif config['bench_param']['device'] == 'gpu':
                bash_cmd = docker_cmd+'-v {}:/data -v {}:/test/log -v {}:/test/config.json flbenchmark/{}'.format(
                    raw_data_dir, raw_log_dir, raw_config_file, config['framework'])
            else:
                raise NotImplementedError('Device {} is not supported.'.format(config['bench_param']['device']))
        elif config['bench_param']['mode'] == 'remote':
            for host in config['bench_param']['hosts']:
                if config['bench_param']['device'] == 'cpu':
                    remote_bash_cmd = docker_cmd+'--net=host -v {}:/data -v {}:/test/log -v {}:/test/config.json flbenchmark/{}'.format(
                        raw_data_dir, raw_log_dir, raw_config_file, config['framework'])
                elif config['bench_param']['device'] == 'gpu':
                    remote_bash_cmd = docker_cmd+'--net=host -v {}:/data -v {}:/test/log -v {}:/test/config.json flbenchmark/{}'.format(
                        raw_data_dir, raw_log_dir, raw_config_file, config['framework'])
                else:
                    raise NotImplementedError('Device {} is not supported.'.format(config['bench_param']['device']))
                remote_run(host['hostname'], remote_bash_cmd)
            print('The benchmark has started, and you can use `python -m flbenchmark get_report {}` to query the report.'.format(id))
        else:
            raise NotImplementedError('Mode {} is not supported.'.format(config['bench_param']['mode']))
    else:
        raise NotImplementedError('Framework {} is not supported.'.format(config['framework']))

    if config['bench_param']['mode'] == 'local':
        if debug_flag:
            subprocess.run(bash_cmd, shell=True, check=True)
        elif docker_stats_flag:
            docker_run = subprocess.run(bash_cmd, shell=True, check=True, capture_output=True)
            container_id = docker_run.stdout.splitlines()[0].decode()
            monitor_cmd = 'python3 -m flbenchmark monitor_docker_stats {} {}'.format(id, container_id)
            subprocess.Popen(monitor_cmd, shell=True, stdout=DEVNULL, stderr=DEVNULL)
        else:
            subprocess.run(bash_cmd, shell=True, stdout=DEVNULL, check=True)
        print('The benchmark has started, and you can use `python -m flbenchmark get_report {}` to query the report.'.format(id))


def prepare_dataset(dataset_name):
    print('Preparing dataset {}'.format(dataset_name))
    FATE_DATASETS = ['breast_horizontal', 'default_credit_horizontal', 'give_credit_horizontal', 'student_horizontal', 'vehicle_scale_horizontal',
                     'motor_vertical', 'breast_vertical', 'default_credit_vertical', 'dvisits_vertical', 'give_credit_vertical', 'student_vertical', 'vehicle_scale_vertical']
    LEAF_DATASETS = ['celeba', 'femnist', 'reddit', 'sent140', 'shakespeare', 'synthetic']

    raw_data_dir = '~/flbenchmark.working/data'
    flbd = flbenchmark.datasets.FLBDatasets(raw_data_dir)

    if dataset_name in FATE_DATASETS:
        dataset = flbd.fateDatasets(dataset_name)
    elif dataset_name in LEAF_DATASETS:
        dataset = flbd.leafDatasets(dataset_name)
    else:
        raise NotImplementedError('Dataset {} is not supported.'.format(dataset_name))

    if len(dataset[0].parties) > 0:
        pass
    else:
        raise RuntimeError('Failed when preparing dataset {}. Please check the error message.'.format(dataset_name))


def prepare_framework_image(framework_name):
    if framework_name.startswith('custom:'):
        return
    print('Pulling framework image {}'.format(framework_name))
    bash_cmd = 'docker pull flbenchmark/frameworks:{}'.format(framework_name)
    subprocess.run(bash_cmd, shell=True, check=True)


def get_report(id):
    working_dir = os.path.expanduser('~/flbenchmark.working')
    raw_working_dir = '~/flbenchmark.working'
    log_dir = os.path.join(working_dir, id, 'log')
    raw_log_dir = os.path.join(raw_working_dir, str(id), 'log')
    config_file = os.path.join(working_dir, str(id), 'config.json')
    config = json.load(open(config_file, 'r'))
    if config['bench_param']['mode'] == 'remote':
        for host in config['bench_param']['hosts']:
            raw_log_file = os.path.join(raw_log_dir, str(host['id'])+'.log')
            remote_pull(host['hostname'], raw_log_file, log_dir)
    flbenchmark.logging.get_report(log_dir)


def monitor_docker_stats(id, container_id):
    memory_stats_file = '/sys/fs/cgroup/memory/docker/{}/memory.usage_in_bytes'.format(container_id)
    working_dir = os.path.expanduser('~/flbenchmark.working')
    log_file = os.path.join(working_dir, id, 'stats.log')
    while True:
        if os.path.exists(memory_stats_file):
            memory_usage_in_bytes = int(open(memory_stats_file, 'r').read())
            logs = []
            logs.append(json.dumps({"memory_usage_in_bytes": memory_usage_in_bytes, "timestamp": time.time()}, default=lambda x: x.__dict__)+'\n')
            with open(log_file, 'a') as f:
                f.writelines(logs)
        else:
            return
        time.sleep(1.0)


if __name__ == '__main__':
    if len(sys.argv) >= 2:
        if sys.argv[1] == 'prepare_dataset':
            prepare_dataset(sys.argv[2])
            exit(0)
        elif sys.argv[1] == 'prepare_framework_image':
            prepare_framework_image(sys.argv[2])
            exit(0)
        elif sys.argv[1] == 'get_report':
            get_report(sys.argv[2])
            exit(0)
        elif sys.argv[1] == 'monitor_docker_stats':
            monitor_docker_stats(sys.argv[2], sys.argv[3])
            exit(0)
        else:
            config_file = sys.argv[1]
    else:
        config_file = './config.json'
    start(config_file)
