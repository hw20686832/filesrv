namespace py filesrv

struct Meta {
  1: string appid,
  2: i32 version_code,
  3: string version_name,
  4: string ext
}

service Filesrv {
   string test(1: string words),
   string save(1: required string fileobj, 2: required Meta meta)
}