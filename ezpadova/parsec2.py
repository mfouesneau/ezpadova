"""
EZPADOVA -- A python package that allows you to download PADOVA isochrones
directly from their website

This version is compatible with Parsec 2.0 and CMD3.7 website.
This version requires python >= 3.5

:version: 2.0
:author: MF
"""
import sys
if sys.version_info[0] <= 2:
    print("This version requires python 3")

import os
import inspect
import zlib
import re
import json
from io import StringIO, BytesIO
from .simpletable import SimpleTable as Table
from urllib.parse import urlencode
from urllib import request
from urllib.request import urlopen
from html import parser


base_directory = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(base_directory, 'parsec.json'), encoding='utf8') as f:
    _cfg = json.load(f)
    map_carbon_stars = _cfg["map_carbon_stars"]
    map_phot = _cfg["map_phot"]
    map_circum_Mstars = _cfg["map_circum_Mstars"]
    map_interp = _cfg["map_interp"]
    map_circum_Cstars = _cfg["map_circum_Cstars"]
    __def_args__ = _cfg["__def_args__"]
    map_models = _cfg["map_models"]
    map_isoc_val = _cfg["map_isoc_val"]
    webserver = _cfg.get("webserver", 'http://stev.oapd.inaf.it')


def parse_cmd_page() -> parser.HTMLParser:
    """ Parse the html page of parsec """

    class Parser(parser.HTMLParser):
        """ Only cares about select and option values """
        def __init__(self, *args, **kwargs):
            parser.HTMLParser.__init__(self, *args, **kwargs)
            self.data = {}
            self.name = None
            self.lst = []
            self.current = []

        def handle_starttag(self, tag, attrs):
            # print(tag)
            if 'select' in tag:
                self.name = [k[1] for k in attrs if k[0] == 'name'][0]
                # print("SELECT FOUND: ", self.name)
            if 'option' in tag:
                self.current.append(attrs[0][1])

        def handle_endtag(self, tag):
            if 'select' in tag:
                self.data[self.name] = self.lst
                self.name = None
                self.lst = []
            if 'option' in tag:
                self.current = [self.current[0], ''.join(self.current[1:])]
                self.lst.append(self.current)
                self.current = []

        def handle_data(self, data):
            if len(data) < 2:
                return
            if self.name is not None:
                self.current.append(data.replace('\n', ' '))

    data = urlopen(webserver + '/cgi-bin/cmd').read().decode('utf8')
    data = data.replace("option selected value", "option value")
    p = Parser()
    p.feed(data)
    return p




def get_photometry_list() -> dict:
    """ Try to extact photometric options directly from the website

    Directly update the configuration

    Returns
    -------
    map_phot: dict
        dictionary of photometry options and descriptions
    """

    class Parser(parser.HTMLParser):
        """ Only cares about select and option values """
        def __init__(self, *args, **kwargs):
            parser.HTMLParser.__init__(self, *args, **kwargs)
            self.data = {}
            self.name = None
            self.lst = []
            self.current = []

        def handle_starttag(self, tag, attrs):
            # print(tag)
            if 'select' in tag:
                self.name = [k[1] for k in attrs if k[0] == 'name'][0]
                # print("SELECT FOUND: ", self.name)
            if 'option' in tag:
                self.current.append(attrs[0][1])

        def handle_endtag(self, tag):
            if 'select' in tag:
                self.data[self.name] = self.lst
                self.name = None
                self.lst = []
            if 'option' in tag:
                self.current = [self.current[0], ''.join(self.current[1:])]
                self.lst.append(self.current)
                self.current = []

        def handle_data(self, data):
            if len(data) < 2:
                return
            if self.name is not None:
                self.current.append(data.replace('\n', ' '))

    data = urlopen(webserver + '/cgi-bin/cmd').read().decode('utf8')
    data = data.replace("option selected value", "option value")
    p = Parser()
    p.feed(data)
    phot_list = p.data['photsys_file'][1:]   # first one is a list

    final = []
    for key, val in phot_list:
        if len(val) > 0:
            key = key.replace('tab_mag_odfnew/tab_mag_', '').replace('.dat', '')
        final.append((key, val))

    # update the main configuration
    map_phot.update(final)
    return map_phot


# Help messages
# -------------

def help_phot():
    """Prints photometry options and descriptions"""
    for k, v in map_phot.items():
        print('phot "{0}":\n   {1}\n'.format(k, v))


def help_models():
    """Prints model options and descriptions"""
    for k, v in map_models.items():
        print('model "{0}":\n   {1}\n'.format(k, v[1]))


def help_carbon_stars():
    """Prints carbon star model options and descriptions"""
    for k, v in map_carbon_stars.items():
        print('model "{0}":\n   {1}\n'.format(k, v[1]))


def help_circumdust():
    """Prints circumstellar dust model options and descriptions"""
    print('M stars')
    for k, v in map_circum_Mstars.items():
        print('model "{0}":\n   {1}\n'.format(k, v[1]))
    print('C stars')
    for k, v in map_circum_Cstars.items():
        print('model "{0}":\n   {1}\n'.format(k, v[1]))


def file_type(filename, stream=False) -> str:
    """ Detect potential compressed file

    Parameters
    ----------
    filename: str or buffer
        filename or buffer to read from

    stream: bool, optional
        set if the input data is a stream / buffer

    Returns
    -------
    ftype: str or None
        Returns one of 'gz', 'bz2' or 'zip' if a compression is detected, else None.
    """
    magic_dict = { "\x1f\x8b\x08": "gz", "\x42\x5a\x68": "bz2", "\x50\x4b\x03\x04": "zip" }

    max_len = max(len(x) for x in magic_dict)
    if not stream:
        with open(filename) as f:
            file_start = f.read(max_len)
        for magic, filetype in magic_dict.items():
            if file_start.startswith(magic):
                return filetype
    else:
        for magic, filetype in magic_dict.items():
            if filename[:len(magic)] == magic:
                return filetype

    return None


def search_passbands(regex: str = ".*", ignorecase=False) -> dict:
    """Search photometry options given some regular expression"""
    if ignorecase:
        r = re.compile(regex, re.IGNORECASE)
    else:
        r = re.compile(regex)
    return {k: v
            for k, v in map_phot.items()
            if (r.match(k) or r.match(v))}