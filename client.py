import sys
sys.path.append('gen-py')

from filesrv import Filesrv
from filesrv.ttypes import Meta

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol


def main():
    # Make socket
    transport = TSocket.TSocket('192.168.2.20', 9090)

    # Buffering is critical. Raw sockets are very slow
    transport = TTransport.TBufferedTransport(transport)

    # Wrap in a protocol
    protocol = TBinaryProtocol.TBinaryProtocol(transport)

    # Create a client to use the protocol encoder
    client = Filesrv.Client(protocol)

    # Connect!
    transport.open()

    #print client.test("hello world!")
    #print client.get("group1/M00/00/00/wKgCFFcOHb2ACJ3oACe08ejnGKc044.apk")

    meta = Meta()
    meta.appid = "com.facebook.katana"
    meta.version_code = 1
    meta.version_name = '1.23.5'
    meta.ext = "apk"

    with open("/home/david/Downloads/vShareMarket_20151120_mobvista_1.apk") as f:
        print client.save(f.read(), meta)

    #print client.remove('group1/M00/00/00/PZvXNFcVjrqAAvUsACe08ejnGKc839.apk')

    # Close!
    transport.close()


if __name__ == "__main__":
    main()
