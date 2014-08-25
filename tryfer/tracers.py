import sys
import logging
from tryfer.formatters import json_formatter, base64_thrift_formatter
from tryfer.writer import ScribeWriter

class NoopTracer(object):
    '''
    Does absolutely nothing with a supplied traces
    '''

    def __init__(self, *args, **kwargs):
        '''
        Noop operator that does nothing

        @param callback: a function that should be called with arguments during record
        '''
        self.callback = kwargs.get('callback', lambda x: None)

    def record(self, traces):
        self.callback(traces)



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
    Send all annotations to zipkin directly via scribe
    '''
    def __init__(self, host='localhost', port=9410, category='zipkin'):
        self._host = host
        self._port = port
        self._category = category
        self._writer = ScribeWriter(self._host, self._port,
                                    default_category=self._category)

    def record(self, traces):
        '''
        Write data via scribe
        '''
        logging.debug('sending info to scribe or zipkin directly')
        for trace, annotations in traces:
            self._writer.write(base64_thrift_formatter(trace, annotations))

