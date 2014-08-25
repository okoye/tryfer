'''
A handy decorator to add zipkin support to methods
'''
from tryfer.trace import Trace, Endpoint, Annotation
from tryfer.tracers import DebugTracer, ZipkinTracer
from socket import gethostname
from os import environ

tracers = [DebugTracer()]
if not environ.get('ZIPKIN_DEBUG', None):
    tracers.append(ZipkinTracer()) #assume you want data

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
        trace.record(Annotation.server_recv())
        result = func(*args, **kwargs)
        trace.record(Annotation.server_send())
        return result

    return wrapper



def http_zipper(func):
    raise NotImplementedError('not currently supported')
