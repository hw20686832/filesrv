import os
import sys
import json
from hashlib import sha1, md5
sys.path.append('gen-py')

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer
from fdfs_client.client import Fdfs_client

from filesrv import Filesrv
from filesrv.ttypes import Meta


class FilesrvHandler(object):
    def __init__(self):
        self.secret_code = "sW$^dffGad3e3h8fh7gc~t7 `7 t"
        self.root = "/data0/androidapk/"
        self.client = Fdfs_client('/etc/fdfs/client.conf')

    def test(self, words):
        return words

    def save(self, fileobj, meta):
        try:
            result = {}
            hexs = sha1(meta.appid)
            #hexs.update(str(meta.version_code))
            hexs.update(self.secret_code)
            hexs.update(str(meta.seq))
            hex_code = hexs.hexdigest()
            dirs = os.path.join(meta.file_type, *[hex_code[(i-1)*2:i*2] for i in range(1, 5)])

            filename = "{}.{}".format(hex_code[8:], meta.ext)
            filepath = os.path.join(dirs, filename)
            fullpath = os.path.join(self.root, filepath)
            try:
                os.makedirs(os.path.join(self.root, dirs))
            except:
                pass
            with open(fullpath, 'w') as f:
                f.write(fileobj)

            result["md5"] = md5(fileobj).hexdigest()
            result["path"] = filepath
        except Exception as e:
            result = {"error": str(e)}

        return json.dumps(result)

    def save2fdfs(self, filebuff, meta):
        meta_dict = {
            "appid": meta.appid,
            "version_code": meta.version_code,
            "version_name": meta.version_name,
            "file_type": meta.file_type,
            "ext": meta.ext,
            "seq": meta.seq
        }
        rs = self.client.upload_by_buffer(filebuff, meta.ext, meta_dict=meta_dict)
        result = {
            "md5": md5(filebuff).hexdigest(),
            "path": rs["Remote file_id"],
            "size": rs["Uploaded size"]
        }

        return json.dumps(result)

    def save_media2fdfs(self, filebuff, ext):
        rs = self.client.upload_by_buffer(filebuff, ext)
        result = {
            "md5": md5(filebuff).hexdigest(),
            "path": rs["Remote file_id"],
            "size": rs["Uploaded size"]
        }

        return json.dumps(result)

    def save_media(self, filebuff, ext):
        meta = Meta(
            appid="appvv.com",
            file_type="media",
            ext=ext
        )
        return self.save(filebuff, meta)


    def get(self, fileid):
        try:
            meta = self.client.get_meta_data(fileid)
            return Meta(
                appid=meta['appid'],
                version_code=int(meta['version_code']),
                version_name=meta['version_name'],
                file_type=meta['file_type'],
                ext=meta['ext'],
                seq=int(meta['seq'])
            )
        except Exception as e:
            return str(e)

    def remove(self, fileid):
        rs = self.client.delete_file(fileid)
        return json.dumps({'appid': rs[1]})


if __name__ == '__main__':
    handler = FilesrvHandler()
    processor = Filesrv.Processor(handler)
    transport = TSocket.TServerSocket(host="0.0.0.0", port=9090)
    tfactory = TTransport.TBufferedTransportFactory()
    pfactory = TBinaryProtocol.TBinaryProtocolFactory()

    #server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)

    # You could do one of these for a multithreaded server
    # server = TServer.TThreadedServer(processor, transport, tfactory, pfactory)
    server = TServer.TThreadPoolServer(processor, transport, tfactory, pfactory)

    print('Starting the server...')
    server.serve()
    print('done.')
