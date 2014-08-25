'''
A handy decorator to add zipkin support to methods
'''
from tryfer.trace import Trace, Endpoint, Annotation
from tryfer.tracers import DebugTracer, ZipkinTracer
from socket import gethostname
from os import environ
import logging

tracers = [DebugTracer(), ZipkinTracer()]

def rpc_zipper(func):
    def wrapper(*args, **kwargs):
        '''
        do what ever we need to setup zipkin and set appropriate headers
        '''
        #first, create a trace using appropriate headers
        trace = Trace('search',
                        None,
                        None,
                        None,
                        tracers=tracers)
        #ideally, these info  would be extracted from request args.
        #hacky way to determine hostname, port and service_name
        host_name = gethostname()
        host_port = 80
        service_name = 'waldo-search'
        endpoint = Endpoint(host_name, host_port, service_name)
        trace.set_endpoint(endpoint)

        #now, log start point
        logging.debug('recording server recv span')
        trace.record(Annotation.server_recv())
        result = func(*args, **kwargs)
        logging.debug('recording server send span')
        trace.record(Annotation.server_send())
        return result

    return wrapper



def http_zipper(func):
    raise NotImplementedError('not currently supported')
