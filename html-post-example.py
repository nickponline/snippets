"""
 POST to HTML form and read response.
"""

import snappy
import zlib
import base64
import mechanize
import requests
import mechanize

url = "http://www.google.com/"
br = mechanize.Browser()
br.set_handle_robots(False) # ignore robots file
br.open(url)
br.select_form(name="q") # form name
br["q"] = jpg_text # field
res = br.submit()
content = res.read()
print content



