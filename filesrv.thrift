namespace py filesrv

struct Meta {
  1: required string appid,
  2: i32 version_code,
  3: string version_name,
  4: string file_type = 'package',
  5: string ext = 'apk',
  6: i32 seq = 0
}

service Filesrv {
   string test(1: string words),
   string save(1: required string fileobj, 2: required Meta meta),
   string save2fdfs(1: required string filebuff, 2: required Meta meta),
   Meta get(1: required string fileid),
   string remove(1: required string fileid)
}