import os
import json
import numpy as np
from .common import Log, Event


def get_report(log_dir: str):
    log_dir = os.path.expanduser(log_dir)
    log_files = {}
    for file in os.listdir(log_dir):
        if file.endswith('.log'):
            if not os.path.splitext(file)[0].isdigit():
                print('The benchmark is not finished or the log files are broken.')
                exit(0)
            id = int(os.path.splitext(file)[0])
            log_files[id] = os.path.join(log_dir, file)
    all_agents = list(log_files.keys())
    if len(all_agents) == 0:
        print('The benchmark is not finished or the log files are broken.')
        exit(0)

    # Check logs
    for id, file in log_files.items():
        with open(file, 'r') as f:
            lines = f.readlines()
        try:
            log = json.loads(lines[-1])
        except:
            print('The benchmark is not finished or the log files are broken.')
            exit(0)
        if log.get('flbenchmark') is None or log['flbenchmark'] != 'end':
            print('The benchmark is not finished or the log files are broken.')
            exit(0)

    print('Agents: {}'.format(all_agents))
    # Generate report
    agents = {}
    general_events = {}
    training_rounds = {}
    computations = {}
    communications = {}
    custom_events = {}
    for id, file in log_files.items():
        with open(file, 'r') as f:
            lines = f.readlines()
        logs = {}
        events = {}
        for line in lines:
            log = json.loads(line)
            if log.get('flbenchmark') is not None:
                if log['flbenchmark'] == 'start':
                    if agents.get(log['agent_type']) is None:
                        agents[log['agent_type']] = []
                    agents[log['agent_type']].append(id)
                continue
            log = Log(log['event'], log['action'], log['timestamp'], log['metrics'])
            start_log = logs.get(log.event)
            if start_log is None:
                logs[log.event] = log
            elif start_log.action != 'start':
                raise RuntimeError('Invalid Log.')
            else:
                event = Event(log.event, start_log.timestamp, log.timestamp, log.timestamp-start_log.timestamp, log.metrics)
                events[event.event] = event
                logs[log.event] = log
        last_computation = None
        calc_waiting = False
        for key, event in sorted(events.items(), key=lambda x: x[1].start_timestamp):
            x = key.split('.')
            if len(x) == 1:
                pass
            else:
                if x[0] == 'computation':
                    last_computation = event
                elif x[0] == 'communication':
                    if last_computation is not None and last_computation.start_timestamp <= event.start_timestamp and event.end_timestamp <= last_computation.end_timestamp:
                        calc_waiting = False
                        last_computation.time -= event.time
                else:
                    pass

        training_rounds[id] = []
        computations[id] = []
        general_events[id] = {}
        custom_events[id] = {}
        for key, event in sorted(events.items(), key=lambda x: x[1].start_timestamp):
            x = key.split('.')
            if len(x) == 1:
                general_events[id][event.event] = event
            else:
                if x[0] == 'training':
                    training_rounds[id].append(event)
                elif x[0] == 'computation':
                    computations[id].append(event)
                elif x[0] == 'communication':
                    if communications.get((id, int(x[1]))) is None:
                        communications[(id, int(x[1]))] = []
                    communications[(id, int(x[1]))].append(event)
                elif x[0] == 'custom':
                    custom_events[id][event.event] = event
                else:
                    raise RuntimeError('Invalid Event.')

    debug_flag = os.environ.get('FLB_DEBUG', 'false').lower() == 'true'
    tot_communication_rounds = 0
    tot_communication_bytes = 0
    report_list = []
    for type, agents_list in agents.items():
        for id in agents_list:
            print('{} {}:'.format(type, id))
            agent_report = {'agent_id': id, 'agent_type': type, 'reports': []}
            if type in ['client', 'aggregator']:
                # preprocess_data
                if 'preprocess_data' in general_events[id]:
                    print('preprocess_data: {:.6f}s'.format(general_events[id]['preprocess_data'].time))
                    agent_report['reports'].append(
                        {'type': 'preprocess_data', 'time': general_events[id]['preprocess_data'].time})
                # training
                if 'training' in general_events[id]:
                    print('Total training time: {:.6f}s'.format(general_events[id]['training'].time))
                    agent_report['reports'].append(
                        {'type': 'total_training_time', 'time': general_events[id]['training'].time})
                    waiting_time = general_events[id]['training'].time
                    have_waiting_time = True
                else:
                    waiting_time = 0
                    have_waiting_time = False
                # training_round
                if len(training_rounds[id]) > 0:
                    if 'client_num' not in training_rounds[id][0].metrics:
                        print('Training rounds: {}, time: {:.6f}s(avg)'.format(
                            len(training_rounds[id]), np.average([i.time for i in training_rounds[id]])))
                    else:
                        print('Training rounds: {}, time: {:.6f}s(avg), client number in each round: {}'.format(len(training_rounds[id]), np.average(
                            [i.time for i in training_rounds[id]]), [i.metrics.get('client_num', 'n/a') for i in training_rounds[id]]))
                    agent_report['reports'].append({'type': 'training_rounds', 'events': [
                        {'time': i.time, 'client_num': i.metrics.get('client_num', None)} for i in training_rounds[id]]})
                    if not have_waiting_time:
                        waiting_time = np.sum([i.time for i in training_rounds[id]])
                        have_waiting_time = True
                # computation
                if len(computations[id]) > 0:
                    if computations[id][0].metrics.get('flop', -1) != -1:
                        print('Computation costs: {}(rounds), time: {:.6f}s(avg), flops: {}(avg)'.format(len(computations[id]), np.average(
                            [i.time for i in computations[id]]), np.average([i.metrics.get('flop', -1) for i in computations[id]])))
                    else:
                        print('Computation costs: {}(rounds), time: {:.6f}s(avg)'.format(len(computations[id]), np.average(
                            [i.time for i in computations[id]])))
                    agent_report['reports'].append({'type': 'computation_costs', 'events': [
                        {'time': i.time, 'flop': i.metrics.get('flop', None)} for i in computations[id]]})
                    waiting_time -= np.sum([i.time for i in computations[id]])
                else:
                    calc_waiting = False
                # communication
                agent_tot_communication_rounds = 0
                agent_tot_communication_bytes = 0
                if communications.get((id, -1)) is not None:
                    print('Communication costs:')
                    communication = communications.get((id, -1))
                    print('  {}(rounds), time: {:.6f}s(avg), bytes: {}(avg) {}(total)'.format(len(communication), np.average([i.time for i in communication]), np.average(
                        [i.metrics.get('byte', -1) for i in communication]), np.sum([i.metrics.get('byte', 0) for i in communication])))
                    comm_report = {'type': 'communication_costs', 'events': [
                        {'time': i.time, 'byte': i.metrics.get('byte', None)} for i in communication]}
                    waiting_time -= np.sum([i.time for i in communication])
                    agent_report['reports'].append(comm_report)
                    agent_tot_communication_rounds += len(communication)
                    agent_tot_communication_bytes += np.sum([i.metrics.get('byte', 0) for i in communication])
                else:
                    have_communication = False
                    for target in all_agents:
                        if communications.get((id, target)) is not None:
                            have_communication = True
                            break
                    if have_communication:
                        print('Communication costs:')
                        comm_report = {'type': 'communication_costs', 'targets': {}}
                        for target in all_agents:
                            if communications.get((id, target)) is not None:
                                print('  Target id: {}'.format(target))
                                communication_transmit = communications.get((id, target))
                                communication_receive = communications.get((target, id))
                                print('    Transmit: {}(rounds), time: {:.6f}s(avg), bytes: {}(avg) {}(total)'.format(len(communication_transmit), np.average([i.time for i in communication_transmit]), np.average(
                                    [i.metrics.get('byte', -1) for i in communication_transmit]), np.sum([i.metrics.get('byte', 0) for i in communication_transmit])))
                                print('    Receive: {}(rounds), time: {:.6f}s(avg), bytes: {}(avg) {}(total)'.format(len(communication_receive), np.average([i.time for i in communication_receive]), np.average(
                                    [i.metrics.get('byte', -1) for i in communication_receive]), np.sum([i.metrics.get('byte', 0) for i in communication_receive])))
                                comm_report['targets'][target] = {'transmit_events': [{'time': i.time, 'byte': i.metrics.get('byte', None)} for i in communication_transmit],
                                                                  'receive_events': [{'time': i.time, 'byte': i.metrics.get('byte', None)} for i in communication_receive]}
                                waiting_time -= np.sum([i.time for i in communication_transmit]) + \
                                    np.sum([i.time for i in communication_receive])
                                agent_tot_communication_rounds += len(communication_transmit)+len(communication_receive)
                                agent_tot_communication_bytes += np.sum([i.metrics.get('byte', 0) for i in communication_transmit]) + \
                                    np.sum([i.metrics.get('byte', 0) for i in communication_receive])
                        agent_report['reports'].append(comm_report)
                    else:
                        calc_waiting = False
                # total_waiting_time_in_training
                if calc_waiting and have_waiting_time:
                    print('Total waiting time in training: {:.6f}s'.format(waiting_time))
                    agent_report['reports'].append(
                        {'type': 'total_waiting_time_in_training', 'time': waiting_time})
                # model_evaluation
                if 'model_evaluation' in general_events[id]:
                    print('Model evaluation: time: {:.6f}s, metrics: {}'.format(
                        general_events[id]['model_evaluation'].time, general_events[id]['model_evaluation'].metrics))
                    agent_report['reports'].append(
                        {'type': 'model_evaluation', 'time': general_events[id]['model_evaluation'].time, 'metrics': general_events[id]['model_evaluation'].metrics})
                # end
                if debug_flag:
                    print("agent_tot_communication_rounds: ", agent_tot_communication_rounds)
                    print("agent_tot_communication_bytes: ", agent_tot_communication_bytes)
                tot_communication_rounds += agent_tot_communication_rounds
                tot_communication_bytes += agent_tot_communication_bytes
            else:
                raise ValueError('Invalid agent type')
            print('\n\n')
            report_list.append(agent_report)
    if debug_flag:
        print("tot_communication_rounds: ", tot_communication_rounds)
        print("tot_communication_bytes: ", tot_communication_bytes)

    with open(os.path.join(log_dir, 'report.json'), 'w') as outfile:
        outfile.write(json.dumps(report_list, indent=4))
    print('The report in json format is here: {}'.format(os.path.join(log_dir, 'report.json')))
    print('View the original log for more details: {}'.format(log_dir))
