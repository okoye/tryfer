from scribe import scribe
from thrift.transport import TTransport, TSocket
from thrift.protocol import TBinaryProtocol
from thrift import Thrift


class ScribeWriter(object):
    '''
    A convenience class for writing to scribe
    '''
    def __init__(self, host, port, default_category='zipkin'):
        self.host = host
        self.port = port
        self.category = default_category
        socket = TSocket.TSocket(host=self.host, port=self.port)
        transport = TTransport.TFramedTransport(socket)
        protocol = TBinaryProtocol.TBinaryProtocol(trans=transport,
                                                    strictRead=False,
                                                    strictWrite=False)
        client = scribe.Client(protocol)
        transport.open()
        self.client = client

    def write(self, messages, category=None):
        '''
        @param message: a list of messages to be sent via scribe
        '''
        log_entry = scribe.LogEntry(category or self.category, messages)
        result = self.client.Log(messages=log_entry)
        if result == 0:
            logging.debug('messages sent successfully via scribe')
        else:
            logging.debug('messages not sent successfully via scribe')

