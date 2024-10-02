import requests
from bs4 import BeautifulSoup
from io import BytesIO
import json
import os
import re


# URL of the webpage
config = dict(
    url = "http://stev.oapd.inaf.it/cgi-bin/cmd"
)


def dedent(text: str) -> str:
    """Remove any common leading whitespace from every line in `text`.

    This can be used to make triple-quoted strings line up with the left
    edge of the display, while still presenting them in the source code
    in indented form.

    Note that tabs and spaces are both treated as whitespace, but they
    are not equal: the lines "  hello" and "\\thello" are
    considered to have no common leading whitespace.

    Entirely blank lines are normalized to a newline character.
    """
    # Look for the longest leading string of spaces and tabs common to
    # all lines.
    _whitespace_only_re = re.compile("^[ \t]+$", re.MULTILINE)
    _leading_whitespace_re = re.compile("(^[ \t]*)(?:[^ \t\n])", re.MULTILINE)

    margin = None
    text = _whitespace_only_re.sub("", text)
    indents = _leading_whitespace_re.findall(text)
    for indent in indents:
        if margin is None:
            margin = indent

        # Current line more deeply indented than previous winner:
        # no change (previous winner is still on top).
        elif indent.startswith(margin):
            pass

        # Current line consistent with and no deeper than previous winner:
        # it's the new winner.
        elif margin.startswith(indent):
            margin = indent

        # Find the largest common whitespace between current line and previous
        # winner.
        else:
            for i, (x, y) in enumerate(zip(margin, indent)):
                if x != y:
                    margin = margin[:i]
                    break

    # sanity check (testing/debugging only)
    if 0 and margin:
        for line in text.split("\n"):
            assert not line or line.startswith(margin), "line = %r, margin = %r" % (
                line,
                margin,
            )

    if margin:
        text = re.sub(r"(?m)^" + margin, "", text)
    return text


def get_file_archive_type(filename: str | BytesIO, stream: bool = False) -> str | None:
    """ Detect the type of a potentially compressed file.

    This function checks the beginning of a file to determine if it is compressed
    using gzip, bzip2, or zip formats. It returns the corresponding file type if
    a compression is detected, otherwise it returns None.

    Args:
        filename (str | BytesIO): The path to the file or a BytesIO stream to check.
        stream (bool): If True, `filename` is treated as a BytesIO stream. If False,
                       `filename` is treated as a file path.

    Returns:
        str | None: The type of compression detected ('gz', 'bz2', 'zip'), or None if
                    no compression is detected.
    """
    magic_dict = { b"\x1f\x8b\x08": "gz", b"\x42\x5a\x68": "bz2", b"\x50\x4b\x03\x04": "zip" }

    max_len = max(len(x) for x in magic_dict)
    if not stream:
        with open(filename, 'rb') as f:
            file_start = f.read(max_len)
    else:
        file_pos = filename.tell()
        file_start = filename.read(max_len)
        filename.seek(file_pos)

    for magic, filetype in magic_dict.items():
        if file_start.startswith(magic):
            return filetype

    return None


def _parse_select_info(forms:BeautifulSoup, name:str, elt_class:str, /) -> dict:
    comps = {}
    for form in forms:
        elements = form.find_all(elt_class)
        for element in elements:
            if element['name'] == name:
                options = element.find_all('option')
                for option in options:
                    key = option['value'].replace('tab_mag_odfnew/tab_mag_', '').replace('.dat', '')
                    if key:
                        comps[key] = (option.text, option['value'])
    return comps
    
def _get_siblings_text(element: BeautifulSoup) -> str:
    """ Get the text from the siblings until another form element is found """
    elements_ = []
    for sibling in element.next_siblings:
        if sibling.text or sibling.name == "br": 
            elements_.append(sibling.text)
        else:
            break
    return " ".join(elements_)

def _parse_radio_info(forms:BeautifulSoup, name:str, elt_class:str, elt_type: str) -> dict:


    comps = {}
    for form in forms:
        elements = form.find_all(elt_class, type=elt_type)
        for element in elements:
            if element['name'] == name:
                text = _get_siblings_text(element)
                comps[name] = comps.get(name, []) + [(text, element['value'])]
    return comps


def _parse_text_info(forms:BeautifulSoup, name:str, elt_class:str, elt_type: str) -> dict:
    comps = {}
    for form in forms:
        elements = form.find_all(elt_class, type=elt_type)
        for element in elements:
            if element['name'] == name:
                text = _get_siblings_text(element)
                comps[name] = comps.get(name, []) + [(text, element['value'])]
    return comps


def _get_photsys_info(forms: BeautifulSoup) -> dict:
    """ Retrieve photometric systems from the form """
    # get photometric systems
    comps = _parse_select_info(forms, "photsys_file", "select")
    # get atmospheres
    comps.update(_parse_radio_info(forms, "photsys_version", "input", "radio"))
    return comps


def _get_model_info(forms: BeautifulSoup) -> dict:
    """ Retrieve model systems from the form """
    comps = _parse_radio_info(forms, "track_parsec", "input", "radio")
    comps.update(_parse_radio_info(forms, "track_omegai", "input", "radio"))
    comps.update(_parse_radio_info(forms, "track_colibri", "input", "radio"))
    comps.update(_parse_text_info(forms, "eta_reimers", "input", "text"))
    comps.update(_parse_text_info(forms, "n_inTPC", "input", "text"))
    return comps


def _get_mdust(forms: BeautifulSoup) -> dict:
    """ Retrieve dust for M stars """
    # get photometric systems
    comps = _parse_radio_info(forms, "dust_sourceM", "input", "radio")
    return comps

def _get_cdust(forms: BeautifulSoup) -> dict:
    """ Retrieve dust for C stars """
    # get photometric systems
    comps = _parse_radio_info(forms, "dust_sourceC", "input", "radio")
    return comps

def _get_extinction(forms: BeautifulSoup) -> dict:
    comps = _parse_text_info(forms, "extinction_av", "input", "text")
    comps.update(_parse_radio_info(forms, "extinction_coeff", "input", "radio"))
    comps.update(_parse_radio_info(forms, "extinction_curve", "input", "radio"))
    return comps

def _get_imf(forms: BeautifulSoup) -> dict:
    comps = _parse_select_info(forms, "imf_file", "select")
    cleaned = {}
    for key, value in comps.items():
        key_ = key.replace('tab_imf/imf_', '').replace('.dat', '')
        cleaned[key_] = value
    return cleaned

def _get_page_info():
    """ Retrieve information directly from the CMD webpage """

    # Fetch the content
    response = requests.get(config["url"])
    html_content = response.text

    # Parse the HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all forms and their options
    forms = soup.find_all('form')

    # get photometric systems
    config["photsys_file"] = _get_photsys_info(forms)

    # get track flavor
    config["track_parsec"] = _get_model_info(forms)

    # Circumstellar dust flavors
    config["dust_sourceM"] = _get_mdust(forms)["dust_sourceM"]
    config["dust_sourceC"] = _get_cdust(forms)["dust_sourceC"]

    # Extinction
    config["extinction"] = _get_extinction(forms)

    # LPVs
    config["lpvs"] = _parse_radio_info(forms, "kind_LPV", "input", "radio")

    #IMF
    config["imf"] = _get_imf(forms)

def generate_doc():
    """ Generate the documentation from the config variable  """
    
    text = """ 
    # EzPadova configuration file

    _This file contains the configuration for the EzPadova package. It is generated automatically by the package and should not be modified manually._
    
    All detailed description of the parameters can be found on the [CMD webpage](http://stev.oapd.inaf.it/cgi-bin/cmd).

    ## Track flavors `track_parsec`

    {track_info}

    ### Track Rotation `track_omegai`

    _only available for PARSEC 2.0_

    {track_omegai}

    ### Track COLIBRI `track_colibri`
    
    _only available for PARSEC 1.2S_

    {track_colibri}

    ### additional parameters

    {track_other}

    ## Photometric systems `photsys_file`

    {photsys_info}

    ## Stellar Atmospheres `photsys_version`

    {photsys_version}

    ## Circumstellar dust flavors    

    ### Dust for M stars `dust_sourceM`

    {dust_sourceM}

    ### Dust for C stars `dust_sourceC`

    {dust_sourceC}

    ## Extinction

    {extinction}

    ## LPVs `kind_LPV`

    {lpvs}

    ## IMF `imf_file`

    {imf}


    """

    track_info = "| value | description |\n| --- | --- |\n"
    for label, value in config["track_parsec"]["track_parsec"]:
        track_info += f"| {value} | {label} |\n"
    
    track_omegai = "| value | description |\n| --- | --- |\n"
    for label, value in config["track_parsec"]["track_omegai"]:
        track_omegai += f"| {value} | {label} |\n"
    
    track_colibri = "| value | description |\n| --- | --- |\n"
    for label, value in config["track_parsec"]["track_colibri"]:
        track_colibri += f"| {value} | {label} |\n"

    photsys_info = "| value | description |\n| --- | --- |\n"
    for value, details in config["photsys_file"].items():
        if value not in ("photsys_version", ):
            photsys_info += f"| {value} | {details[0]} |\n"

    photsys_version = "| value | description |\n| --- | --- |\n"
    for details, value in config["photsys_file"]['photsys_version']:
        photsys_version += f"| {value} | {details} |\n" 
    
    dust_sourceM = "| value | description |\n| --- | --- |\n"
    for details, value in config["dust_sourceM"]:
        dust_sourceM += f"| {value} | {details} |\n"

    dust_sourceC = "| value | description |\n| --- | --- |\n"
    for details, value in config["dust_sourceC"]:
        dust_sourceC += f"| {value} | {details} |\n"

    track_other = "| parameter | value | description |\n| --- | --- | --- |\n"
    for details, value  in config["track_parsec"]["eta_reimers"]:
        track_other += f"| `eta_reimers` | {value} | {details} |\n"
    for details, value in config["track_parsec"]["n_inTPC"]:
        track_other += f"| `n_inTPC` | {value} | {details} |\n"

    extinction = "| parameter | value | description |\n| --- | --- | --- |\n"
    for key, value  in config["extinction"].items():
        for details, value in value:
            extinction += f"| `{key}` | {value} | {details} |\n"

    lpvs = "| value | description |\n| --- | --- |\n"
    for details, value in config["lpvs"]['kind_LPV']:
        lpvs += f"| {value} | {details} |\n"

    imf = "| value | description | filename |\n| --- | --- | --- |\n"
    for key, (details, value) in config["imf"].items():
        imf += f"| {key} | {details} | {value} |\n"

    text = dedent(text).format(**locals())

    with open("config.md", "w") as f:
        f.write(text)


def update_config():
    """ Update the configuration of the package from parsing the website"""
    _get_page_info()


if __name__ == "__main__":
    update_config()
    generate_doc()