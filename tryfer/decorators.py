'''
A handy decorator to add zipkin support to methods
'''
from tryfer.trace import Trace, Endpoint, Annotation

def rpc_zipper(func):
    def wrapper(*args, **kwargs):
        '''
        do what ever we need to setup zipkin and set appropriate headers
        '''
        #first, create a trace using appropriate headers

        result = func(*args, **kwargs)

        return func(*args, **kwargs)

    return wrapper



def http_zipper(func):
    raise NotImplementedError('not currently supported')
