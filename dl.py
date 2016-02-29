import os
import zipfile
import tempfile
from .remote import *
from cudatext import *

def do_unzip(fn_zip, folder):
    zf = zipfile.ZipFile(fn_zip)  
    zf.extractall(folder)  

def find_css_in_zip(fn_zip):
    zf = zipfile.ZipFile(fn_zip)  
    l = [info.filename for info in zf.filelist if info.filename.endswith('.css')]
    if l:
        return l[0]
    
def do_download(url):
    fn_zip = os.path.join(tempfile.gettempdir(), 'cudatext_webfont.zip')
    fn_editor = ed.get_filename()
    dir_editor = os.path.dirname(fn_editor)
    eol = '\n'
     
    get_url(url, fn_zip)
    if not os.path.isfile(fn_zip):
        msg_status('Cannot download zip')
        return
    
    fn_css = find_css_in_zip(fn_zip)    
    if not fn_css:
        msg_status('Cannot find css file')
        return

    fn_target = dlg_file(False, fn_css, dir_editor, '*.css|*.css|')
    if not fn_target: return
    dir_target = os.path.dirname(fn_target)
    fn_target = os.path.join(dir_target, fn_css)
    
    do_unzip(fn_zip, dir_target)
    os.remove(fn_zip)
    
    path = os.path.relpath(fn_target, dir_editor).replace('\\', '/')
    
    x0, y0, x1, y1 = ed.get_carets()[0]                                        
    ed.insert(x0, y0, ('@import "%s";' + eol) % path)
    msg_status('Downloaded font')
