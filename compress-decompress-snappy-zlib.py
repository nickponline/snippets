"""
 Compress/decompress file with zlib and snappy
"""

import snappy
import zlib
import base64
import mechanize
import requests
import mechanize

data = file("filename.txt", "rw").read()

r = snappy.compress(data)
snappy.uncompress(r)

r = zlib.compress(data)
zlib.decompress(r)
