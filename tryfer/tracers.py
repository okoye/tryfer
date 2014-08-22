import sys
from tryfer.formatters import json_formatter, base64_formatter

class NoopTracer(object):
    '''
    Does absolutely nothing with a supplied traces
    '''

    def __init__(self *args, **kwargs):
        pass

    def record(self, traces):
        pass


class DebugTracer(object):
    '''
    Send annotations to a file like destination in JSON format.

    All traces will be written immediately to the destination.

    @param destination: A file like object to write JSON formatted traces to.
    '''

    def __init__(self, destination=None):
        self.destination = destination or sys.stdout

    def record(self, traces):
        self.destination.write(json_formatter(traces, indent=2))
        self.destination.write('\n')
        self.destination.flush()

class ZipkinTracer(object):
    '''
    Send all annotations to zipkin directly
    '''
    def __init__(self):
        pass #TODO

    def record(self, traces):
        raise NotImplementedError('record is currently unsupported')

