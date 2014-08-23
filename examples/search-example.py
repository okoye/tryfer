'''
a basic application showing how to use tryfer to send information
to zipkin in without twisted
'''
import requests
from tryfer.decorators import http_zipper

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
            search_string = raw_input(self.prompt)
            if self._should_stop(search_string):
                stop = True
            else:
                self._search(search_string)
                print 'logged query to zipkin'

    @http_zipper
    def _search(self, query):
        query = ''.join([self.base_string, query])
        r = requests.get(query)
        return r

    def _should_stop(self, query):
        return self.stop_string == query.strip()

def main():
    bs = BasicSearch()
    bs.search()

if __name__ == '__main__':
    main()