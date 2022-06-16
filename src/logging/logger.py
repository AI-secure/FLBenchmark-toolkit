import os
import time
import json
from typing import List
from .common import Log


class LoggerContext:
    def __init__(self, logger, event: str):
        self.logger = logger
        self.event = event
        self.metrics = {}

    def __enter__(self):
        self.logger.logs.append(Log(self.event, 'start', time.time()))
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.logger.logs.append(Log(self.event, 'end', time.time(), self.metrics))
        self.logger.flush_check()
        if self.logger.force_flush:
            self.logger.flush()

    def report_metric(self, key, value):
        if self.metrics.get(key) is not None:
            raise RuntimeError('You can not report the same metric twice.')
        self.metrics[key] = value


def Singleton(object):
    _instance = {}

    def _singleton(*args, **kargs):
        if object not in _instance:
            _instance[object] = object(*args, **kargs)
        elif len(args) > 0 or len(kargs) > 0:
            print("Warning: the logger is already initialized, so the initialization parameters here will be ignored.")
        return _instance[object]

    return _singleton


@Singleton
class Logger:
    def __new__(cls, *agrs, **kwds):
        return BasicLogger(*agrs, **kwds)


class BasicLogger:
    def __init__(self,
                 id: int = -1,
                 agent_type: str = "",
                 dir: str = None,
                 ):
        self.id = id
        self.agent_type = agent_type
        if dir is None:
            self.dir = './log'
        else:
            self.dir = os.path.expanduser(dir)
        if not os.path.exists(self.dir):
            os.makedirs(self.dir)
        self.logs = [{"flbenchmark": "start", "timestamp": time.time(), "agent_type": self.agent_type}]
        self.training_round_auto_increment = 0
        self.computation_auto_increment = 0
        self.communication_auto_increment = 0
        self.training_round_current_event = None
        self.computation_current_event = None
        self.communication_current_event = None
        # clear the log file
        log_file = os.path.join(self.dir, '{}.log'.format(self.id))
        open(log_file, 'w').close()
        self.flush()
        # force flush
        self.force_flush = os.getenv('FLBENCHMARK_LOGGING_FORCE_FLUSH', 'false').lower() == 'true'

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.end()

    def flush_check(self):
        if len(self.logs) >= 64:
            self.flush()

    def flush(self):
        log_file = os.path.join(self.dir, '{}.log'.format(self.id))
        logs = []
        for log in self.logs:
            logs.append(json.dumps(log, default=lambda x: x.__dict__)+'\n')
        with open(log_file, 'a') as f:
            f.writelines(logs)
        self.logs.clear()

    def end(self):
        self.logs.append({"flbenchmark": "end", "timestamp": time.time()})
        self.flush()

    def preprocess_data(self) -> LoggerContext:
        return LoggerContext(self, 'preprocess_data')

    def preprocess_data_start(self):
        self.logs.append(Log('preprocess_data', 'start', time.time()))

    def preprocess_data_end(self, metrics={}):
        self.logs.append(Log('preprocess_data', 'end', time.time(), metrics))
        self.flush_check()

    def training(self) -> LoggerContext:
        return LoggerContext(self, 'training')

    def training_start(self):
        self.logs.append(Log('training', 'start', time.time()))

    def training_end(self, metrics={}):
        self.logs.append(Log('training', 'end', time.time(), metrics))
        self.flush_check()

    def training_round(self, id: int = None) -> LoggerContext:
        if id is None:
            id = self.training_round_auto_increment
            self.training_round_auto_increment += 1
        return LoggerContext(self, 'training.{}'.format(id))

    def training_round_start(self, id: int = None):
        if self.training_round_current_event is not None:
            raise RuntimeError('Please end this event first.')
        if id is None:
            id = self.training_round_auto_increment
            self.training_round_auto_increment += 1
        self.training_round_current_event = 'training.{}'.format(id)
        self.logs.append(Log(self.training_round_current_event, 'start', time.time()))

    def training_round_end(self, metrics={}):
        if self.training_round_current_event is None:
            raise RuntimeError('Please start this event first.')
        self.logs.append(Log(self.training_round_current_event, 'end', time.time(), metrics))
        self.flush_check()
        self.training_round_current_event = None

    def computation(self, id: int = None) -> LoggerContext:
        if id is None:
            id = self.computation_auto_increment
            self.computation_auto_increment += 1
        return LoggerContext(self, 'computation.{}'.format(id))

    def computation_start(self, id: int = None):
        if self.computation_current_event is not None:
            raise RuntimeError('Please end this event first.')
        if id is None:
            id = self.computation_auto_increment
            self.computation_auto_increment += 1
        self.computation_current_event = 'computation.{}'.format(id)
        self.logs.append(Log(self.computation_current_event, 'start', time.time()))

    def computation_end(self, metrics={}):
        if self.computation_current_event is None:
            raise RuntimeError('Please start this event first.')
        self.logs.append(Log(self.computation_current_event, 'end', time.time(), metrics))
        self.flush_check()
        self.computation_current_event = None

    def communication(self, target_id: int, id: int = None) -> LoggerContext:
        if id is None:
            id = self.communication_auto_increment
            self.communication_auto_increment += 1
        return LoggerContext(self, 'communication.{}.{}'.format(target_id, id))

    def communication_start(self, target_id: int, id: int = None):
        if self.communication_current_event is not None:
            raise RuntimeError('Please end this event first.')
        if id is None:
            id = self.communication_auto_increment
            self.communication_auto_increment += 1
        self.communication_current_event = 'communication.{}.{}'.format(target_id, id)
        self.logs.append(Log(self.communication_current_event, 'start', time.time()))

    def communication_end(self, metrics={}):
        if self.communication_current_event is None:
            raise RuntimeError('Please start this event first.')
        self.logs.append(Log(self.communication_current_event, 'end', time.time(), metrics))
        self.flush_check()
        self.communication_current_event = None

    def model_evaluation(self) -> LoggerContext:
        return LoggerContext(self, 'model_evaluation')

    def model_evaluation_start(self):
        self.logs.append(Log('model_evaluation', 'start', time.time()))

    def model_evaluation_end(self, metrics={}):
        self.logs.append(Log('model_evaluation', 'end', time.time(), metrics))
        self.flush_check()

    def custom_event(self, event: str) -> LoggerContext:
        return LoggerContext(self, 'custom.{}'.format(event))

    def custom_event_start(self, event: str):
        self.logs.append(Log('custom.{}'.format(event), 'start', time.time()))

    def custom_event_end(self, event: str, metrics={}):
        self.logs.append(Log('custom.{}'.format(event), 'end', time.time(), metrics))
        self.flush_check()
