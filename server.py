import os
import sys
from hashlib import sha1
sys.path.append('gen-py')

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

from filesrv import Filesrv


class FilesrvHandler:
    def __init__(self):
        self.root = "/data0/androidapk"

    def test(self, words):
        return words

    def save(self, fileobj, meta):
        hexs = sha1(meta.appid)
        hexs.update(str(meta.version_code))
        hex_code = hexs.hexdigest()
        dirs = os.path.join(*[hex_code[(i-1)*2:i*2] for i in range(1, 5)])

        filename = "{}.{}".format(hex_code[8:], meta.ext)
        try:
            os.makedirs(os.path.join(self.root, dirs))
        except:
            pass

        filepath = os.path.join(dirs, filename)
        fullpath = os.path.join(self.root, filepath)
        with open(fullpath, 'w') as f:
            f.write(fileobj)

        return filepath


if __name__ == '__main__':
    handler = FilesrvHandler()
    processor = Filesrv.Processor(handler)
    transport = TSocket.TServerSocket(host="0.0.0.0", port=9090)
    tfactory = TTransport.TBufferedTransportFactory()
    pfactory = TBinaryProtocol.TBinaryProtocolFactory()

    server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)

    # You could do one of these for a multithreaded server
    # server = TServer.TThreadedServer(processor, transport, tfactory, pfactory)
    # server = TServer.TThreadPoolServer(processor, transport, tfactory, pfactory)

    print('Starting the server...')
    server.serve()
    print('done.')
