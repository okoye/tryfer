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
http_method = lambda: random.choice(['GET', 'POST', 'PUT', 'DELETE', 'HEAD'])


def rpc_zipper(service_name='waldo'):
    parent_trace = None
    def zipper(func):
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

class ZipkinDecorator(object):
    def __init__(self, service_name='waldo'):
        self.parent_trace = None

    def _sn(self):
        '''shorthand for random service name generator'''
        return self._random_service_generator()

    def _hn(self):
        '''shorthand for host name generator'''
        return self._random_host_generator()

    def __call__(self, func):
        def wrapped_decorator(*args, **kwargs):
            '''
            do what ever we need to setup zipkin and set appropriate state info
            '''
            if not self.parent_trace:
                trace = Trace(http_method(), None, None, None, tracers=tracers)
            else:
                trace = self.parent_trace.child(http_method())
            host_name = self._hn()
            host_port = 80
            endpoint = Endpoint(host_name, host_port, self._sn())
            trace.set_endpoint(endpoint)

            #now log start point
            logging.debug('recording server recv span')
            trace.record(Annotation.server_recv())
            func(*args, **kwargs)
            logging.debug('recording server send span')
            trace.record(Annotation.server_send())
            self.parent_trace = trace
        return wrapped_decorator

    def _random_host_generator(self):
        octet = lambda: random.randint(2, 254)
        return '%s.%s.%s.%s'%(octet(), octet(), octet(), octet())

    def _random_service_generator(self):
        adjectives = ['funny', 'mad', 'crazy', 'happy', 'dumb', 'sweet', 'sour', 'small',
                'big']
        nouns = ['marie_curie', 'newton', 'einstein', 'leibniz', 'sagan', 'gauss']
        return '%s_%s'%(random.choice(adjectives), random.choice(nouns))


def http_zipper(func):
    raise NotImplementedError('not currently supported')
