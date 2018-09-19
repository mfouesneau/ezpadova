"""
EZPADOVA -- A python package that allows you to download PADOVA isochrones
directly from their website

:version: 1.1
:author: MF
"""
from __future__ import print_function, unicode_literals, division

import sys
import os
import inspect

if sys.version_info[0] > 2:
    py3k = True
    from urllib.parse import urlencode
    from urllib import request
    from urllib.request import urlopen
    from html import parser
else:
    py3k = False
    from urllib import urlencode
    from urllib2 import urlopen
    import HTMLParser as parser


from io import StringIO, BytesIO
import zlib
import re
import json
from .simpletable import SimpleTable as Table


localpath = '/'.join(os.path.abspath(inspect.getfile(inspect.currentframe())).split('/')[:-1])

with open(localpath + '/parsec.json') as f:
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


def get_photometry_list():
    """ Try to extact photometric options directly from the website

    Directly update the configuration
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


# Help messages
# -------------

def help_phot():
    for k, v in map_phot.items():
        print('phot "{0}":\n   {1}\n'.format(k, v))


def help_models():
    for k, v in map_models.items():
        print('model "{0}":\n   {1}\n'.format(k, v[1]))


def help_carbon_stars():
    for k, v in map_carbon_stars.items():
        print('model "{0}":\n   {1}\n'.format(k, v[1]))


def help_circumdust():
    print('M stars')
    for k, v in map_circum_Mstars.items():
        print('model "{0}":\n   {1}\n'.format(k, v[1]))
    print('C stars')
    for k, v in map_circum_Cstars.items():
        print('model "{0}":\n   {1}\n'.format(k, v[1]))


def file_type(filename, stream=False):
    """ Detect potential compressed file
    Returns the gz, bz2 or zip if a compression is detected, else None.
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


# Build up URL request
# --------------------

def __get_url_args(model=None, carbon=None, interp=None, Mstars=None,
                   Cstars=None, phot=None, **kwargs):
    """ Update options in the URL query using internal shortcuts

    Parameters
    ----------

    model: str
        select the type of model :func:`help_models`

    carbon: str
        carbon stars model :func:`help_carbon_stars`

    interp: str
        interpolation scheme

    Mstars: str
        dust on M stars :func:`help_circumdust`

    Cstars: str
        dust on C stars :func:`help_circumdust`

    phot: str
        photometric set for photometry values :func:`help_phot`

    Returns
    -------
    d: dict
        cgi arguments
    """
    d = __def_args__.copy()

    # overwrite some parameters
    if model is not None:
        d['isoc_kind'] = map_models["%s" % model][0]
        if 'parsec' in model.lower():
            d['output_evstage'] = 1
        else:
            d['output_evstage'] = 0

    if carbon is not None:
        d['kind_cspecmag'] = map_carbon_stars[carbon][0]

    if interp is not None:
        d['kind_interp'] = map_interp[interp]

    if Cstars is not None:
        d['dust_sourceC'] = map_circum_Cstars[Cstars]

    if Mstars is not None:
        d['dust_sourceM'] = map_circum_Mstars[Mstars]

    if phot is not None:
        d['photsys_file'] = 'tab_mag_odfnew/tab_mag_{0}.dat'.format(phot)

    for k, v in kwargs.items():
        if k in d:
            d[k] = v

    return d


class __CMD_Error_Parser(parser.HTMLParser):
    """ find error box in the recent version of CMD website """
    def handle_starttag(self, tag, attrs):
        if (tag == "p") & (dict(attrs).get('class', None) == 'errorwarning'):
            self._record = True
            self.data = []

    def handle_endtag(self, tag):
        if (tag == "p") & getattr(self, '_record', False):
            self._record = False

    def handle_data(self, data):
        if getattr(self, '_record', False):
            self.data.append(data)


def __query_website(d):
    """ Communicate with the CMD website """
    webserver = 'http://stev.oapd.inaf.it'
    print('Interrogating {0}...'.format(webserver))
    # url = webserver + '/cgi-bin/cmd_2.8'
    url = webserver + '/cgi-bin/cmd'
    q = urlencode(d)
    # print('Query content: {0}'.format(q))
    if py3k:
        req = request.Request(url, q.encode('utf8'))
        c = urlopen(req).read().decode('utf8')
    else:
        c = urlopen(url, q).read()
    aa = re.compile('output\d+')
    fname = aa.findall(c)
    if len(fname) > 0:
        url = '{0}/tmp/{1}.dat'.format(webserver, fname[0])
        print('Downloading data...{0}'.format(url))
        bf = urlopen(url)
        r = bf.read()
        typ = file_type(r, stream=True)
        if typ is not None:
            r = zlib.decompress(bytes(r), 15 + 32)
        return r
    else:
        # print(c)
        print(url + q)
        if "errorwarning" in c:
            p = __CMD_Error_Parser()
            p.feed(c)
            print('\n', '\n'.join(p.data).strip())
        raise RuntimeError('Server Response is incorrect')


def __convert_to_Table(resp, dic=None):
    """ Make a table from the string response content of the website """

    def find_data(txt, comment='#'):
        for num, line in enumerate(txt.split('\n')):
            if line[0] != comment:
                return num

    _r = resp.decode('utf8')
    start = find_data(_r) - 1
    _r = '\n'.join(_r.split('\n')[start:])[1:].encode('utf8')
    bf = BytesIO(_r)
    tab = Table(bf, dtype='tsv', comment='#')
    if dic is not None:
        for k, v in dic.items():
            tab.header[k] = v

    # make some aliases
    aliases = (('logA', 'logageyr'),
               ('logA', 'log(age/yr)'),
               ('logL', 'logLLo'),
               ('logL', 'logL/Lo'),
               ('logT', 'logTe'),
               ('logg', 'logG'))

    for a, b in aliases:
        try:
            tab.set_alias(a, b)
        except KeyError:
            pass
            # print('Error setting alias {0}->{1}'.format(a, b))


    return tab


# Convenient Functions
# --------------------

def get_one_isochrone(age, metal, ret_table=True, **kwargs):
    """ get one isochrone at a given time and Z

    Parameters
    ----------

    age: float
        age of the isochrone (in yr)

    metal: float
        metalicity of the isochrone

    ret_table: bool
        if set, return a eztable.Table object of the data

    model: str
        select the type of model :func:`help_models`

    carbon: str
        carbon stars model :func:`help_carbon_stars`

    interp: str
        interpolation scheme

    Mstars: str
        dust on M stars :func:`help_circumdust`

    Cstars: str
        dust on C stars :func:`help_circumdust`

    phot: str
        photometric set for photometry values :func:`help_phot`

    Returns
    -------
    r: Table or str
        if ret_table is set, return a eztable.Table object of the data
        else return the string content of the data
    """
    d = __get_url_args(**kwargs)
    d['isoc_val'] = 0
    d['isoc_age'] = age
    d['isoc_zeta'] = metal

    r = __query_website(d)
    if ret_table is True:
        return __convert_to_Table(r, d)
    else:
        return r


def get_Z_isochrones(z0, z1, dz, age, ret_table=True, **kwargs):
    """ get a sequence of isochrones at constant time but variable Z

    Parameters
    ----------
    z0: float
        minimal value of Z

    z11: float
        maximal value of Z

    dz: float
        step in Z

    age: float
        age of the sequence (in yr)

    ret_table: bool
        if set, return a eztable.Table object of the data

    model: str
        select the type of model :func:`help_models`

    carbon: str
        carbon stars model :func:`help_carbon_stars`

    interp: str
        interpolation scheme

    Mstars: str
        dust on M stars :func:`help_circumdust`

    Cstars: str
        dust on C stars :func:`help_circumdust`

    phot: str
        photometric set for photometry values :func:`help_phot`

    Returns
    -------
    r: Table or str
        if ret_table is set, return a eztable.Table object of the data
        else return the string content of the data
    """
    d = __get_url_args(**kwargs)
    d['isoc_val'] = 2
    d['isoc_age0'] = age
    d['isoc_z0'] = z0
    d['isoc_z1'] = z1
    d['isoc_dz'] = dz

    r = __query_website(d)
    if ret_table is True:
        return __convert_to_Table(r, d)
    else:
        return r


def get_t_isochrones(logt0, logt1, dlogt, metal, ret_table=True, **kwargs):
    """ get a sequence of isochrones at constant Z

    Parameters
    ----------
    logt0: float
        minimal value of log(t/yr)

    logt1: float
        maximal value of log(t/yr)

    dlogt: float
        step in log(t/yr) for the sequence

    metal: float
        metallicity value to use (Zsun=0.019)

    ret_table: bool
        if set, return a eztable.Table object of the data

    model: str
        select the type of model :func:`help_models`

    carbon: str
        carbon stars model :func:`help_carbon_stars`

    interp: str
        interpolation scheme

    Mstars: str
        dust on M stars :func:`help_circumdust`

    Cstars: str
        dust on C stars :func:`help_circumdust`

    phot: str
        photometric set for photometry values :func:`help_phot`

    Returns
    -------
    r: Table or str
        if ret_table is set, return a eztable.Table object of the data
        else return the string content of the data
    """
    d = __get_url_args(**kwargs)
    d['isoc_val'] = 1
    d['isoc_zeta0'] = metal
    d['isoc_lage0'] = logt0
    d['isoc_lage1'] = logt1
    d['isoc_dlage'] = dlogt

    r = __query_website(d)
    if ret_table is True:
        return __convert_to_Table(r, d)
    else:
        return r

get_photometry_list()
