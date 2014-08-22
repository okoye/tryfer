'''
A handy decorator to add zipkin support to methods
'''

def http_zipper(func):
    def wrapper(*args, **kwargs):
        '''
        do what ever we need to setup zipkin and set appropriate headers
        '''
        print 'TODO'
        return func(*args, **kwargs)

    return wrapper
