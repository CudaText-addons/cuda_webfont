import os
import urllib.request
import tempfile
from cudatext import *

URL_LIST = 'https://fontstorage.com/api/list.json'
URL_SITE = 'https://fontstorage.com/'
TEMP_FN = 'cudatext_webfont.json'
 
def get_url(url, fn):
    if os.path.isfile(fn):
        os.remove(fn)
    urllib.request.urlretrieve(url, fn)
 
def get_fonts_file(refresh):
    fn = os.path.join(tempfile.gettempdir(), TEMP_FN)
    if not refresh and os.path.isfile(fn):
        return fn
        
    msg_status('Downloading font list...')
    get_url(URL_LIST, fn)
    msg_status('')
    if os.path.isfile(fn):
        return fn
