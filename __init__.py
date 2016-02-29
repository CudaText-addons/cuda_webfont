import os
import json
import webbrowser
from cudatext import *
from .remote import *
from .dl import *

SPEC = [
  '* Refresh font list',
  '* Download font',
  '* Open site',
  ]
SPEC_REFRESH = 0
SPEC_DOWNLOAD = 1
SPEC_SITE = 2  

def get_dict(refresh):  
    fn = get_fonts_file(refresh)
    if not fn:
        msg_box('Cannot download font list', MB_OK)
        return

    j = json.loads(open(fn).read())
    if not j:
        msg_box('Cannot parse font list', MB_OK)
        return
        
    j = sorted(j, key = lambda item: item['name'])
    return j

def do_menu(j, specials):  
    names = [item['name'] for item in j]
    if specials:
        names = SPEC + names
    names = '\n'.join(names)
    return dlg_menu(MENU_LIST, names)

class Command:
    def run(self):
        j = get_dict(False)
        if not j: return
        index = do_menu(j, True)   
        if index is None: return

        while index<len(SPEC):        
            if index==SPEC_REFRESH:
                j = get_dict(True)
                if not j: return
                index = do_menu(j, True)
                if index is None: return
                
            elif index==SPEC_DOWNLOAD:
                index = do_menu(j, False)
                if index is None: return
                url = j[index]['pack_url']
                do_download(url)                
                return
                
            elif index==SPEC_SITE:
                webbrowser.open_new_tab(URL_SITE)
                msg_status('Opened fonts site')
                return
        index -= len(SPEC)
                                       
        text_i = j[index]['import']
        text_c = j[index]['comments']
        eol = '\n'
        #text_c = text_c.replace('\n', eol)
        
        #if ed.get_prop(PROP_TAB_SPACES):
        #    indent = ed.get_prop(PROP_TAB_SIZE) * ' '
        #    text_c = text_c.replace('\t', indent)
        text_c = text_c.replace('\t', '  ')
        
        text = text_i + eol + text_c
        
        x0, y0, x1, y1 = ed.get_carets()[0]
        ed.insert(x0, y0, text)
        msg_status('Inserted font "%s"' % j[index]['name'])
