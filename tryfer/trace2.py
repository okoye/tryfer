'''
Re-writing trace.py without twisted requirements and some improvements
'''

import math
import time
import uuid
import random

from tryfer._thrift.zipkinCore import constants
from tryfer.tracer2 import NoopTracer

def _generate_unique_id():
    '''
    Create a random 64 bit signed integer for use as trace and span IDs.
    '''
    #return uuid.uuid1().int >> 64
    return random.randint(0, (2 ** 56) - 1)

class Trace(object):
    '''
    A trace provider which delegates to zero or more tracers and allows
    setting a default endpoint to associate with annotations
    '''


    def __init__(self, name, trace_id=None, span_id=None,
                parent_span_id=None, tracers=None):
        '''
        @param name: string describing the current span
        @param trace_id: 64bit trace id or none
        @param span_id: 64bit span_id or none
        @param parent_span_id: 64bit parent span id or none
        '''
        self.name = name
        self.trace_id = trace_id or _generate_unique_id()
        self.span_id = span_id or _generate_unique_id()
        self.parent_span_id = parent_span_id
        self._tracers = tracers or NoopTracer()
        self._endpoint = None

    def __eq__(self, other):
        if not other:
            return False
        return ((self.trace_id, self.span_id, self.parent_span_id) ==
                (other.trace_id, other.span_id, other.parent_span_id))

    def __ne__(self, other):
        return not self == other

    def child(self, name):
        '''
        create a child instance of this class such that :
        our current trace_id becomes the trace_id of our new class and
        our current span_id becomes the parent_span_id of new class.

        the new instance will have a unique span_id of its own and if set
        the endpoint of the current trace object.

        @param name: string describing the new span represented by the new
        trace object

        @returns trace: a new trace object
        '''
        trace = self.__class__(name, trace_id=self.trace_id,
                                parent_span_id=self.span_id)
        trace.set_endpoint(self._endpoint)
        return trace

    def record(self, *annotations):
        for annotation in annotations:
            if annotation.endpoint is None and self._endpoint is not None:
                annotation.endpoint = self._endpoint

        for tracer in self._tracers:
            tracer.record([(self, annotations)])

    def set_endpoint(self, endpoint):
        '''
        set a default endpoint for current trace. All annotations will
        automatically be set to use it unless they provide their own
        endpoint.
        '''
        self._endpoint = endpoint


class Endpoint(object):

    def __init__(self, ipv4, port, service_name):
        '''
        @param ipv4: string representation of an ipv4 address
        @param port: int port number
        @param service_name: string service name
        '''
        self.ipv4 = ipv4
        self.port = port
        self.service_name = service_name

    def __eq__(self, other):
        if not other:
            return False

        return ((self.ipv4, self.port, self.service_name) ==
                (other.ipv4, other.port, other.service_name))

    def __ne__(self, other):
        return not self == other


class Annotation(object):

    def __init__(self, name, value, annotation_type, endpoint=None):
        '''
        @param name: string name of this annotation
        @param value: A value of the appropriate type
        @param annotation_type: string the expected type of our value
        @param endpoint: an optional endpoint provider to associate with
                        this annotation or none
        '''
        self.name = name
        self.value = value
        self.annotation_type = annotation_type
        self.endpoint = endpoint

    def __eq__(self, other):
        if not other:
            return False
        return ((self.name, self.value, self.annotation_type, self.endpoint) ==
                (other.name, other.value, other.annotation_type, other.endpoint))

    def __ne__(self, other):
        return not self == other

    @classmethod
    def timestamp(cls, name, timestamp=None):
        if timestamp is None:
            timestamp = math.trunc(time.time() * 1000 * 1000)
        return cls(name, timestamp, 'timestamp')

    @classmethod
    def client_send(cls, timestamp=None):
        return cls.timestamp(constants.CLIENT_SEND, timestamp)

    @classmethod
    def client_recv(cls, timestamp=None):
        return cls.timestamp(constants.CLIENT_RECV, timestamp)

    @classmethod
    def server_send(cls, timestamp=None):
        return cls.timestamp(constants.SERVER_SEND, timestamp)

    @classmethod
    def server_recv(cls, timestamp=None):
        return cls.timestamp(constants.SERVER_RECV, timestamp)

    @classmethod
    def string(cls, name, value):
        return cls(name, value, 'string')

    @classmethod
    def bytes(cls, name, value):
        return cls(name, value, 'bytes')
