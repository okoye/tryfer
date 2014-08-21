'''
Re-writing trace.py without twisted requirements and some improvements
'''

import math
import time
import uuid

from tryfer._thrift.zipkinCore import constants

def _generate_unique_id():
    '''
    Create a random 64 bit signed integer for use as trace and span IDs.
    '''
    return uuid.uuid1().int >> 64

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
        self._tracers = tracers

