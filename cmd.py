"""
EZPADOVA -- A python package that allows you to download PADOVA isochrones
directly from their website

:version: 1.0
:author: MF
"""
from __future__ import print_function, unicode_literals, division

import sys

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
from .simpletable import SimpleTable as Table

# internal parameters
# -------------------

# interpolation
map_interp = {
    'default': 0,
    'improved': 1
}


map_phot = {"2mass_spitzer": " 2MASS + Spitzer (IRAC+MIPS)",
            "2mass_spitzer_wise": " 2MASS + Spitzer (IRAC+MIPS) + WISE",
            "2mass": " 2MASS JHKs",
            "ubvrijhk": "UBVRIJHK (cf. Maiz-Apellaniz 2006 + Bessell 1990)",
            "bessell": "UBVRIJHKLMN (cf. Bessell 1990 + Bessell & Brett 1988)",
            "akari": "AKARI",
            "batc": "BATC",
            "megacam": "CFHT/Megacam u*g'r'i'z'",
            "dcmc": "DCMC",
            "denis": "DENIS",
            "dmc14": "DMC 14 filters",
            "dmc15": "DMC 15 filters",
            "eis": "ESO/EIS (WFI UBVRIZ + SOFI JHK)",
            "wfi": "ESO/WFI",
            "wfi_sofi": "ESO/WFI+SOFI",
            "wfi2": "ESO/WFI2",
            "galex": "GALEX FUV+NUV (Vegamag) + Johnson's UBV",
            "galex_sloan": "GALEX FUV+NUV + SDSS ugriz (all ABmags) ",
            "UVbright": "HST+GALEX+Swift/UVOT UV filters",
            "acs_hrc": "HST/ACS HRC",
            "acs_wfc": "HST/ACS WFC",
            "nicmosab": "HST/NICMOS AB",
            "nicmosst": "HST/NICMOS ST",
            "nicmosvega": "HST/NICMOS vega",
            "stis": "HST/STIS imaging mode",
            "wfc3ir": "HST/WFC3 IR channel (final throughputs)",
            "wfc3uvis1": "HST/WFC3 UVIS channel, chip 1 (final throughputs)",
            "wfc3uvis2": "HST/WFC3 UVIS channel, chip 2 (final throughputs)",
            "wfc3_medium": "HST/WFC3 medium filters (UVIS1+IR, final throughputs)",
            "wfc3": "HST/WFC3 wide filters (UVIS1+IR, final throughputs)",
            "wfpc2": "HST/WFPC2 (Vegamag, cf. Holtzman et al. 1995)",
            "kepler": "Kepler + SDSS griz + DDO51 (in ABmags)",
            "kepler_2mass": "Kepler + SDSS griz + DDO51 (in ABmags) + 2MASS (~Vegamag)",
            "ogle": "OGLE-II",
            "panstarrs1": "Pan-STARRS1",
            "sloan": "SDSS ugriz",
            "sloan_2mass": "SDSS ugriz + 2MASS JHKs",
            "sloan_ukidss": "SDSS ugriz + UKIDSS ZYJHK",
            "swift_uvot": "SWIFT/UVOT UVW2, UVM2, UVW1,u (Vegamag) ",
            "spitzer": "Spitzer IRAC+MIPS",
            "stroemgren": "Stroemgren-Crawford",
            "suprimecam": "Subaru/Suprime-Cam (ABmags)",
            "tycho2": "Tycho VTBT",
            "ukidss": "UKIDSS ZYJHK (Vegamag)",
            "visir": "VISIR",
            "vista": "VISTA ZYJHKs (Vegamag)",
            "washington": "Washington CMT1T2",
            "washington_ddo51": "Washington CMT1T2 + DDO51",
            "ogle_2mass_spitzer": " OGLE + 2MASS + Spitzer (IRAC+MIPS)",
            "2mass_spitzer_wise_washington_ddo51": "2MASS+Spitzer+WISE+Washington+DDO51",
            "megacam_wircam": "CFHT Megacam + Wircam (all ABmags)",
            "wircam": "CFHT Wircam",
            "ciber": "CIBER",
            "decam": "DECAM (ABmags)",
            "decam_vista": "DECAM ugrizY (ABmags) + VISTA ZYJHK_s (Vegamags)",
            "gaia": "Gaia's G, G_BP and G_RP (Vegamags)",
            "wfc3_wideverywide": "HST/WFC3 all W+LP+X filters (UVIS1+IR, final throughputs)",
            "wfc3_verywide": "HST/WFC3 long-pass and extremely wide filters (UVIS1, final throughputs)",
            "wfc3_wide": "HST/WFC3 wide filters (UVIS1+IR, final throughputs)",
            "int_wfc": "INT/WFC (Vegamag)",
            "iphas": "IPHAS",
            "lbt_lbc": "LBT/LBC (Vegamag)",
            "lsst": "LSST ugrizY, March 2012 total filter throughputs (all ABmags)",
            "noao_ctio_mosaic2": "NOAO/CTIO/MOSAIC2 (Vegamag)",
            "TESS_2mass_kepler": "TESS + 2MASS (Vegamags) + Kepler + SDSS griz + DDO51 (in ABmags)",
            "ukidss": "UKIDSS ZYJHK (Vegamag)",
            "vphas": "VPHAS+ (ABmags)",
            "vst_omegacam": "VST/OMEGACAM (ABmag)",
            "vilnius": "Vilnius",
            "jwst_wide": "planned JWST wide filters"
            }


def help_phot():
    for k, v in map_phot.items():
        print('phot "{0}":\n   {1}\n'.format(k, v))

# available tracks
map_models = {
    'parsec12s_r14': ('parsec_CAF09_v1.2S_NOV13', 'PARSEC version 1.2S Bressan et al. (2012), Tang et al. (2014),  Chen et al. (2014) with COLIBRI TP-AGB Marigo et al. (2013), Rosenfield et al. (2014, 2016)'),
    'parsec12s': ('parsec_CAF09_v1.2S', 'PARSEC version 1.2S,  Bressan et al. (2012), Tang et al. (2014),  Chen et al. (2014)'),
    'parsec11': ('parsec_CAF09_v1.1', 'PARSEC version 1.1, With revised diffusion+overshooting in low-mass stars, and improvements in interpolation scheme.'),
    'parsec10': ('parsec_CAF09_v1.0', 'PARSEC version 1.0'),
    '2010': ('gi10a',  'Marigo et al. (2008) with the Girardi et al. (2010) Case A correction for low-mass, low-metallicity AGB tracks'),
    '2010b': ('gi10b',  'Marigo et al. (2008) with the Girardi et al. (2010) Case B correction for low-mass, low-metallicity AGB tracks'),
    '2008': ('ma08',   'Marigo et al. (2008): Girardi et al. (2000) up to early-AGB + detailed TP-AGB from Marigo & Girardi (2007) (for M <= 7 Msun) + Bertelli et al. (1994) (for M > 7 Msun) + additional Z=0.0001 and Z=0.001 tracks.'),
    '2002': ('gi2000', 'Basic set of Girardi et al. (2002) : Girardi et al. (2000) + simplified TP-AGB (for M <= 7 Msun) + Bertelli et al. (1994) (for M > 7 Msun) + additional Z=0.0001 and Z=0.001 tracks.')
}


def help_models():
    for k, v in map_models.items():
        print('model "{0}":\n   {1}\n'.format(k, v[1]))


map_carbon_stars = {
    'loidl': ('loidl01', 'Loidl et al. (2001) (as in Marigo et al. (2008) and Girardi et al. (2008))' ),
    'aringer': ('aringer09', "Aringer et al. (2009) (Note: The interpolation scheme has been slightly improved w.r.t. to the paper's Fig. 19.")
}


def help_carbon_stars():
    for k, v in map_carbon_stars.items():
        print('model "{0}":\n   {1}\n'.format(k, v[1]))

# circumstellar dust
map_circum_Mstars = {
    'nodustM': ('no dust', ''),
    'sil': ('Silicates', 'Bressan et al. (1998)'),
    'AlOx': ('100% AlOx', 'Groenewegen (2006)'),
    'dpmod60alox40': ('60% Silicate + 40% AlOx', 'Groenewegen (2006)'),
    'dpmod': ('100% Silicate', 'Groenewegen (2006)')
}

map_circum_Cstars = {
    'nodustC': ('no dust', ''),
    'gra': ('Graphites', 'Bressan et al. (1998)'),
    'AMC': ('100% AMC', 'Groenewegen (2006)'),
    'AMCSIC15': ('85% AMC + 15% SiC', 'Groenewegen (2006)' )
}


def help_circumdust():
    print('M stars')
    for k, v in map_circum_Mstars.items():
        print('model "{0}":\n   {1}\n'.format(k, v[1]))
    print('C stars')
    for k, v in map_circum_Cstars.items():
        print('model "{0}":\n   {1}\n'.format(k, v[1]))


map_isoc_val = {
    0: ('Single isochrone', ''),
    1: ('Sequence of isochrones at constant Z', ''),
    2: ('Sequence of isochrones at constant t (variable Z)', 'Groenewegen (2006)')
}


__def_args__ = {'binary_frac': 0.3,
                'binary_kind': 1,
                'binary_mrinf': 0.7,
                'binary_mrsup': 1,
                'cmd_version': 2.3,
                'dust_source': 'nodust',
                'dust_sourceC': 'AMCSIC15',
                'dust_sourceM': 'dpmod60alox40',
                'eta_reimers': 0.2,
                'extinction_av': 0,
                'icm_lim': 4,
                'imf_file': 'tab_imf/imf_chabrier_lognormal.dat',
                'isoc_age': 1e7,
                'isoc_age0': 12.7e9,
                'isoc_dlage': 0.05,
                'isoc_dz': 0.0001,
                'isoc_kind': 'parsec_CAF09_v1.2S',
                'isoc_lage0': 6.6,
                'isoc_lage1': 10.13,
                'isoc_val': 0,
                'isoc_z0': 0.0001,
                'isoc_z1': 0.03,
                'isoc_zeta': 0.02,
                'isoc_zeta0': 0.008,
                'kind_cspecmag': 'aringer09',
                'kind_dust': 0,
                'kind_interp': 1,
                'kind_mag': 2,
                'kind_postagb': -1,
                'kind_pulsecycle': 0,
                'kind_tpagb': 3,
                'lf_deltamag': 0.2,
                'lf_maginf': 20,
                'lf_magsup': -20,
                'mag_lim': 26,
                'mag_res': 0.1,
                'output_evstage': 0,
                'output_gzip': 0,
                'output_kind': 0,
                'photsys_file': 'tab_mag_odfnew/tab_mag_bessell.dat',
                'photsys_version': 'yang',
                'submit_form': 'Submit'}


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


def __get_url_args(model=None, carbon=None, interp=None, Mstars=None,
                   Cstars=None, dust=None, phot=None, **kwargs):
    """ Update options in the URL query using internal shortcuts

    Parameters
    ----------

    model: str
        select the type of model :func:`help_models`

    carbon: str
        carbon stars model :func:`help_carbon_stars`

    interp: str
        interpolation scheme

    dust: str
        circumstellar dust prescription :func:`help_circumdust`

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

    if dust is not None:
        d['dust_source'] = map_circum_Mstars[dust]

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
        url = '{0}/~lgirardi/tmp/{1}.dat'.format(webserver, fname[0])
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
    tab = Table(bf, dtype='tsv', names=True, comments='#')
    if dic is not None:
        for k, v in dic.items():
            tab.header[k] = v

    # make some aliases
    aliases = (('logA', 'logageyr'),
               ('logL', 'logLLo'),
               ('logT', 'logTe'),
               ('logg', 'logG'))

    for a, b in aliases:
        tab.set_alias(a, b)

    return tab


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

    dust: str
        circumstellar dust prescription :func:`help_circumdust`

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

    dust: str
        circumstellar dust prescription :func:`help_circumdust`

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

    dust: str
        circumstellar dust prescription :func:`help_circumdust`

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
