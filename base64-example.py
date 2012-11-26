"""
 Base64 encode/decode an image.
"""

import snappy
import zlib
import base64
import mechanize
import requests
import mechanize


jpg_file = "mike_grey.jpg"
jpg_text = base64.encodestring(open(jpg_file,"rb").read())
print jpg_text
