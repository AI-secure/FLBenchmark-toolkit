from typing import Dict


class Log:
    def __init__(self,
                 event: str,
                 action: str,
                 timestamp: float,
                 metrics: Dict = {},
                 ):
        self.event = event
        self.action = action
        self.timestamp = timestamp
        self.metrics = metrics


class Event:
    def __init__(self,
                 event: str,
                 start_timestamp: float,
                 end_timestamp: float,
                 time: float,
                 metrics: Dict = {},
                 ):
        self.event = event
        self.start_timestamp = start_timestamp
        self.end_timestamp = end_timestamp
        self.time = time
        self.metrics = metrics
