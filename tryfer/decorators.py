'''
A handy decorator to add zipkin support to methods
'''
from tryfer.trace import Trace, Endpoint, Annotation
from tryfer.tracers import DebugTracer, ZipkinTracer
from socket import gethostname, gethostbyname
from os import environ
import logging
import random
import functools

tracers = [DebugTracer(), ZipkinTracer()]
function_name = lambda: random.choice(['GET', 'POST', 'PUT', 'DELETE', 'HEAD'])


def rpc_zipper(service_name='waldo'):
    def zipper(func):
        parent_trace = None
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            '''
            do what ever we need to setup zipkin and set appropriate headers
            '''
            #first, create a trace using appropriate headers
            if not parent_trace:
                trace = Trace(function_name(),
                            None,
                            None,
                            None,
                            tracers=tracers)
            else:
                trace = parent_trace.child(function_name())
            #ideally, these info  would be extracted from request args.
            #hacky way to determine hostname, port and service_name
            host_name = gethostbyname(gethostname())
            host_port = 80
            service_name = service_name
            endpoint = Endpoint(host_name, host_port, service_name)
            trace.set_endpoint(endpoint)

            #now, log start point
            logging.debug('recording server recv span')
            trace.record(Annotation.server_recv())
            result = func(*args, **kwargs)
            logging.debug('recording server send span')
            trace.record(Annotation.server_send())
            parent_trace = trace
            return result
        return wrapper

    return zipper



def http_zipper(func):
    raise NotImplementedError('not currently supported')
