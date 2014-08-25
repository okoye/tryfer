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

    def write(self, messages):
        '''
        @param message: a list of messages to be sent via scribe
        '''
        result = self.client.Log(messages=messages)
        if result == 0:
            logging.debug('messages sent successfully via scribe')
        else:
            logging.debug('messages not sent successfully via scribe')

def write(message):
    '''
    a convenience method to write to scribe.

    @param message: a list of messages ready to send via scribe
    '''
    socket = TSocket.TSo
