'''
a basic application showing how to use tryfer to send information
to zipkin in without twisted
'''
import logging
import requests
from random import random, randint
from time import sleep
#from tryfer.decorators import rpc_zipper
from tryfer.decorators import ZipkinDecorator

class BasicSearch(object):
    '''
    A simple REPL program
    '''
    def __init__(self):
        self.base_string = 'https://www.google.com/search?q='
        self.prompt = 'search> '
        self.stop_string = 'exit;'

    def search(self):
        exit = 'to stop, type %s'%self.stop_string
        stop = False
        while not stop:
            command = raw_input(self.prompt)
            if self._should_stop(command):
                stop = True
            else:
                self._search(int(command))
                logging.info('logged query to zipkin')

    def _search(self, count):
        for iteration in xrange(count):
            self._dist_search()

    @ZipkinDecorator(service_name='distributed-service-simulator')
    def _dist_search(self, n=0, current=0):
        '''
        attempts to simulate a distributed system call by
        calling itself recursively.
        '''
        if n == 0: #first call, generate a new seed and call yourself.
            self._dist_search(n=randint(1, 20), current=1)
        else:
            self._work() #simulate latency of doing some work
            if current < n:
                self._dist_search(n=n, current=current+1)
            else:
                return

            #now, simulate working on returned result
            self._work()
            return

    def _work(self):
        '''
        sleep for some time to simulate latency
        '''
        sleep(random())

    def _should_stop(self, query):
        return self.stop_string == query.strip()

def main():
    logging.basicConfig(level=logging.DEBUG)
    bs = BasicSearch()
    bs.search()

if __name__ == '__main__':
    main()
