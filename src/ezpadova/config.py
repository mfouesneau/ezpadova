""" Configuration file for the EzPadova package. 

It provides functions to update the configuration from the CMD webpage and validate query parameters for isochrone generation.
It also contains the default values for the configuration parameters.
"""
import os
from typing import Tuple

import requests
import json
from bs4 import BeautifulSoup

from .tools import dedent


# URL of the webpage
configuration = dict(
    url="https://stev.oapd.inaf.it/cgi-bin/cmd",
    defaults={
        "cmd_version": "3.8",
        "track_omegai": "0.00",
        "track_parsec": "parsec_CAF09_v1.2S",
        "track_colibri": "parsec_CAF09_v1.2S_S_LMC_08_web",
        "track_postagb": "no",
        "n_inTPC": "10",
        "eta_reimers": "0.2",
        "kind_interp": "1",
        "kind_postagb": "-1",
        "photsys_file": "YBC_tab_mag_odfnew/tab_mag_ubvrijhk.dat",
        "photsys_version": "YBCnewVega",
        "dust_sourceM": "dpmod60alox40",
        "dust_sourceC": "AMCSIC15",
        "kind_mag": "2",
        "kind_dust": "0",
        "extinction_av": "0.0",
        "extinction_coeff": "constant",
        "extinction_curve": "cardelli",
        "kind_LPV": "3",
        "imf_file": "tab_imf/imf_kroupa_orig.dat",
        "isoc_isagelog": "0",
        "isoc_agelow": "1.0e9",
        "isoc_ageupp": "1.0e10",
        "isoc_dage": "0.0",
        "isoc_lagelow": "6.6",
        "isoc_lageupp": "10.13",
        "isoc_dlage": "0.0",
        "isoc_ismetlog": "0",
        "isoc_zlow": "0.0152",
        "isoc_zupp": "0.03",
        "isoc_dz": "0.0",
        "isoc_metlow": "-2",
        "isoc_metupp": "0.3",
        "isoc_dmet": "0.0",
        "output_kind": "0",
        "output_evstage": "1",
        "lf_maginf": "-15",
        "lf_magsup": "20",
        "lf_deltamag": "0.5",
        "sim_mtot": "1.0e4",
        "submit_form": "Submit",
    },
)


def reload_configuration():
    """
    Reloads the configuration from a JSON file.

    This function determines the base directory of the current file and constructs
    the path to the configuration file named 'config.json'. If the configuration file
    exists, it loads the configuration from the file and updates the global configuration
    dictionary. If the configuration file does not exist, it calls the `update_config`
    function to create a new configuration and writes it to the 'config.json' file.

    Raises
    ------

    FileNotFoundError: If the configuration file does not exist and `update_config`
                        fails to create a new configuration.

    json.JSONDecodeError: If the configuration file contains invalid JSON.

    """
    base_directory = os.path.dirname(os.path.abspath(__file__))
    config_file = os.path.join(base_directory, "parsec.json")
    documentation_file = os.path.join(base_directory, "parsec.md")
    if os.path.isfile(config_file):
        with open(config_file) as f:
            configuration.update(json.load(f))
    else:
        update_config()
        with open(config_file, "w") as f:
            json.dump(configuration, f, indent=4)
    with open(documentation_file, "w") as f:
        f.write(generate_doc())


def _get_siblings_text(element: BeautifulSoup) -> str:
    """
    Extracts and concatenates the text content from the sibling elements of the given BeautifulSoup element
    until another form element is encountered.

    Parameters
    ----------
    element: BeautifulSoup
        The BeautifulSoup element whose siblings' text content is to be extracted.

    Returns
    -------
    str:
        A single string containing the concatenated text content of the sibling elements.
    """
    elements_ = []
    for sibling in element.next_siblings:
        if sibling.text or sibling.name == "br":
            elements_.append(sibling.text)
        else:
            break
    return " ".join(elements_)


def _parse_select_info(
    forms: BeautifulSoup, name: str, elt_class: str, /
) -> Tuple[dict, dict]:
    """
    Parses the provided BeautifulSoup forms to extract information about select elements.

    Parameters
    ----------
    forms: BeautifulSoup
        The BeautifulSoup object containing the forms to parse.
    name: str
        The name attribute of the select element to look for.
    elt_class: str
        The class of the elements to find within the forms.

    Returns
    -------
    Tuple[dict, dict]:
        A tuple containing two dictionaries:
        - The first dictionary has option values as keys and tuples containing the option text and option value as values.
        - The second dictionary has the name of the select element as the key and the selected option value as the value.
    """
    comps = {}
    selected = None
    for form in forms:
        elements = form.find_all(elt_class)
        for element in elements:
            if element["name"] == name:
                options = element.find_all("option")
                for option in options:
                    key = option["value"]
                    if key:
                        if option.get("selected", False) is not False:
                            selected = key
                        comps[key] = (option.text.strip(), option["value"])
    return comps, {name: selected}


def _parse_radio_info(
    forms: BeautifulSoup, name: str, elt_class: str, elt_type: str
) -> Tuple[dict, dict]:
    """
    Parses radio button information from HTML forms.

    Parameters
    ----------
    forms: BeautifulSoup
        Parsed HTML forms.
    name: str
        The name attribute of the radio buttons to parse.
    elt_class: str
        The class of the elements to find.
    elt_type: str
        The type of the elements to find (e.g., 'radio').

    Returns
    -------
    Tuple[dict, dict]:
        A tuple containing:
        - A dictionary with the name as the key and a list of tuples (text, value) as the value.
        - A dictionary with the name as the key and the selected value as the value.

    """
    comps = {}
    selected = None
    for form in forms:
        elements = form.find_all(elt_class, type=elt_type)
        for element in elements:
            if element["name"] == name:
                text = _get_siblings_text(element)
                if element.get("checked", False) is not False:
                    selected = element["value"]
                comps[name] = comps.get(name, []) + [(text.strip(), element["value"])]
    return comps, {name: selected}


def _parse_text_info(
    forms: BeautifulSoup, name: str, elt_class: str, elt_type: str
) -> Tuple[dict, dict]:
    """
    Parses text information from HTML forms.

    Parameters
    ----------
    forms : BeautifulSoup
        The BeautifulSoup object containing the HTML forms to parse.
    name : str
        The name attribute to search for within the form elements.
    elt_class : str
        The class of the elements to find within the forms.
    elt_type : str
        The type attribute of the elements to find within the forms.

    Returns
    -------
    Tuple[dict, dict]
        A tuple containing two dictionaries:
        - comps: A dictionary where the key is the name and the value is a list of tuples,
                 each containing the text and value of the element.
        - defaults: A dictionary where the key is the name and the value is the default value of the element.
    """
    comps = {}
    defaults = {}
    for form in forms:
        elements = form.find_all(elt_class, type=elt_type)
        for element in elements:
            if element["name"] == name:
                text = _get_siblings_text(element)
                comps[name] = comps.get(name, []) + [(text, element["value"])]
                defaults[name] = element["value"]
    return comps, defaults


def _get_photsys_info(forms: BeautifulSoup) -> Tuple[dict, dict]:
    """
    Retrieve photometric systems and their default values from the form.

    This function extracts photometric system information from the provided
    BeautifulSoup form object. It processes both select and radio input types
    to gather the necessary data.

    Parameters
    ----------
    forms : BeautifulSoup
        A BeautifulSoup object representing the form containing photometric system information.

    Returns
    -------
    Tuple[dict, dict]
        A tuple containing two dictionaries:
        - The first dictionary contains the photometric systems.
        - The second dictionary contains their default values.
    """
    # get photometric systems
    comps_raw, defaults = _parse_select_info(forms, "photsys_file", "select")
    comps = {}
    defaults_ = {}
    for key, value in comps_raw.items():
        key = key.replace("tab_mag_odfnew/tab_mag_", "").replace(".dat", "")
        if key:
            comps[key] = value
    for key, value in defaults.items():
        value = value.replace("tab_mag_odfnew/tab_mag_", "").replace(".dat", "")
        if key:
            defaults_[key] = value

    # get atmospheres
    new_values, new_defaults = _parse_radio_info(
        forms, "photsys_version", "input", "radio"
    )
    comps.update(new_values)
    defaults_.update(new_defaults)
    return comps, defaults_


def _get_model_info(forms: BeautifulSoup) -> Tuple[dict, dict]:
    """
    Retrieve model systems from the form.

    This function parses the provided BeautifulSoup form object to extract
    model system information. It collects radio button and text input values
    from specific form fields and aggregates them into two dictionaries:
    one for the component values and one for the default values.

    Parameters
    ----------
    forms : BeautifulSoup
        The BeautifulSoup object representing the form to be parsed.

    Returns
    -------
    Tuple[dict, dict]
        A tuple containing two dictionaries:
        - comps: A dictionary with the component values.
        - defaults: A dictionary with the default values.
    """
    comps, defaults = _parse_radio_info(forms, "track_parsec", "input", "radio")
    parsed = [
        _parse_text_info(forms, "track_omegai", "input", "text"),
        _parse_radio_info(forms, "track_colibri", "input", "radio"),
        _parse_text_info(forms, "eta_reimers", "input", "text"),
        _parse_text_info(forms, "n_inTPC", "input", "text"),
    ]

    for new_values, new_defaults in parsed:
        comps.update(new_values)
        defaults.update(new_defaults)

    return comps, defaults


def _get_mdust(forms: BeautifulSoup) -> Tuple[dict, dict]:
    """
    Retrieve dust information for M stars.

    This function parses the provided BeautifulSoup form to extract
    the dust source information for M stars. It returns a tuple
    containing two dictionaries: one with the components and one
    with the default values.

    Parameters
    ----------
    forms : BeautifulSoup
        The BeautifulSoup object containing the form data to be parsed.

    Returns
    -------
    Tuple[dict, dict]
        A tuple containing two dictionaries:
        - The first dictionary contains the components of the dust source for M stars.
        - The second dictionary contains the default values for the dust source for M stars.
    """
    comps, defaults = _parse_radio_info(forms, "dust_sourceM", "input", "radio")
    return comps["dust_sourceM"], defaults


def _get_cdust(forms: BeautifulSoup) -> Tuple[dict, dict]:
    """
    Retrieve dust information for C stars.

    This function parses the provided BeautifulSoup form to extract
    the dust source information for C stars.

    Parameters
    ----------
    forms : BeautifulSoup
        The BeautifulSoup object containing the form data.

    Returns
    -------
    Tuple[dict, dict]
        A tuple containing two dictionaries:
        - The first dictionary contains the components of the dust source for C stars.
        - The second dictionary contains the default values for the dust source for C stars.

    """
    comps, defaults = _parse_radio_info(forms, "dust_sourceC", "input", "radio")
    return comps["dust_sourceC"], defaults


def _get_extinction(forms: BeautifulSoup) -> Tuple[dict, dict]:
    """
    Extracts extinction information from the provided BeautifulSoup form.

    Parameters
    ----------
    forms : BeautifulSoup
        A BeautifulSoup object containing the form data.

    Returns
    -------
    Tuple[dict, dict]
        A tuple containing two dictionaries:
        - The first dictionary contains the extracted extinction components.
        - The second dictionary contains the default values for the extinction components.

    """
    elements = [
        _parse_text_info(forms, "extinction_av", "input", "text"),
        _parse_radio_info(forms, "extinction_coeff", "input", "radio"),
        _parse_radio_info(forms, "extinction_curve", "input", "radio"),
    ]
    comps = {}
    defaults = {}
    for new_values, new_defaults in elements:
        comps.update(new_values)
        defaults.update(new_defaults)
    return comps, defaults


def _get_imf(forms: BeautifulSoup) -> Tuple[dict, dict]:
    """
    Extracts and cleans IMF (Initial Mass Function) information from the provided BeautifulSoup form data.

    Parameters
    ----------
    forms : BeautifulSoup
        A BeautifulSoup object containing the form data to parse.

    Returns
    -------
    Tuple[dict, dict]
        A tuple containing two dictionaries:
        - The first dictionary contains cleaned IMF component information with keys modified to remove 'tab_imf/imf_' and '.dat'.
        - The second dictionary contains cleaned default IMF values with keys modified to remove 'tab_imf/imf_' and '.dat'.
    """
    comps, defaults = _parse_select_info(forms, "imf_file", "select")
    cleaned = {}
    defaults_ = {}
    for key, value in comps.items():
        key_ = key.replace("tab_imf/imf_", "").replace(".dat", "")
        cleaned[key_] = value
    for key, value in defaults.items():
        value = value.replace("tab_imf/imf_", "").replace(".dat", "")
        defaults_[key] = value
    return cleaned, defaults_


def _get_age(forms: BeautifulSoup) -> Tuple[dict, dict]:
    """
    Extracts age-related information from a BeautifulSoup form.

    This function parses various age-related fields from the provided BeautifulSoup form object.
    It collects values and default values from radio and text input elements.

    Parameters
    ----------
    forms : BeautifulSoup
        The BeautifulSoup object containing the form to parse.

    Returns
    -------
    Tuple[dict, dict]
        A tuple containing two dictionaries:
        - The first dictionary contains the parsed values.
        - The second dictionary contains the default values.
    """
    _parse_text_info(forms, "isoc_isagelog", "input", "radio")
    elements = [
        _parse_radio_info(forms, "isoc_isagelog", "input", "radio"),
        _parse_text_info(forms, "isoc_agelow", "input", "text"),
        _parse_text_info(forms, "isoc_ageupp", "input", "text"),
        _parse_text_info(forms, "isoc_dage", "input", "text"),
        _parse_text_info(forms, "isoc_lagelow", "input", "text"),
        _parse_text_info(forms, "isoc_lageupp", "input", "text"),
        _parse_text_info(forms, "isoc_dlage", "input", "text"),
    ]
    comps = {}
    defaults = {}
    for new_values, new_defaults in elements:
        comps.update(new_values)
        defaults.update(new_defaults)

    return comps, defaults


def _get_met(forms: BeautifulSoup) -> Tuple[dict, dict]:
    """
    Extracts and parses metallicity-related information from the given BeautifulSoup form.

    Parameters
    ----------
    forms : BeautifulSoup
        A BeautifulSoup object containing the form data to be parsed.

    Returns
    -------
    Tuple[dict, dict]
        A tuple containing two dictionaries:
        - The first dictionary contains the parsed values for each metallicity-related field.
        - The second dictionary contains the default values for each metallicity-related field.
    """
    elements = [
        _parse_radio_info(forms, "isoc_ismetlog", "input", "radio"),
        _parse_text_info(forms, "isoc_zlow", "input", "text"),
        _parse_text_info(forms, "isoc_zupp", "input", "text"),
        _parse_text_info(forms, "isoc_dz", "input", "text"),
        _parse_text_info(forms, "isoc_metlow", "input", "text"),
        _parse_text_info(forms, "isoc_metupp", "input", "text"),
        _parse_text_info(forms, "isoc_dmet", "input", "text"),
    ]
    comps = {}
    defaults = {}
    for new_values, new_defaults in elements:
        comps.update(new_values)
        defaults.update(new_defaults)
    return comps, defaults


def _get_page_info():
    """Retrieve information directly from the CMD webpage and update `config`"""

    # Fetch the content
    response = requests.get(configuration["url"])
    html_content = response.text

    # Parse the HTML
    soup = BeautifulSoup(html_content, "html.parser")

    # Find all forms and their options
    forms = soup.find_all("form")

    elements = [
        # get photometric systems
        ("photsys_file", _get_photsys_info(forms)),
        # get track flavor
        ("track_parsec", _get_model_info(forms)),
        # get track flavor
        ("track_parsec", _get_model_info(forms)),
        # Circumstellar dust flavors
        ("dust_sourceM", _get_mdust(forms)),
        ("dust_sourceC", _get_cdust(forms)),
        # Extinction
        ("extinction", _get_extinction(forms)),
        # LPVs
        ("lpvs", _parse_radio_info(forms, "kind_LPV", "input", "radio")),
        # IMF
        ("imf_file", _get_imf(forms)),
        # Age
        ("isoc_isagelog", _get_age(forms)),
        ("isoc_ismetlog", _get_met(forms)),
    ]

    # configuration["defaults"] = {}
    for key, (comps_, defaults_) in elements:
        configuration[key] = comps_
        # config['defaults'].update(defaults_)


def generate_doc() -> str:
    """
    Generate the documentation from the config variable.

    Returns
    -------
    str
        The generated documentation in markdown format.
    """

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

    ## Default values

    {defaults}

    """

    track_info = "| value | description |\n| --- | --- |\n"
    for label, value in configuration["track_parsec"]["track_parsec"]:
        track_info += f"| {value} | {label} |\n"

    track_omegai = "| value | description |\n| --- | --- |\n"
    for label, value in configuration["track_parsec"]["track_omegai"]:
        track_omegai += f"| {value} | {label} |\n"

    track_colibri = "| value | description |\n| --- | --- |\n"
    for label, value in configuration["track_parsec"]["track_colibri"]:
        track_colibri += f"| {value} | {label} |\n"

    photsys_info = "| value | description |\n| --- | --- |\n"
    for value, details in configuration["photsys_file"].items():
        if value not in ("photsys_version",):
            photsys_info += f"| {value} | {details[0]} |\n"

    photsys_version = "| value | description |\n| --- | --- |\n"
    for details, value in configuration["photsys_file"]["photsys_version"]:
        photsys_version += f"| {value} | {details} |\n"

    dust_sourceM = "| value | description |\n| --- | --- |\n"
    for details, value in configuration["dust_sourceM"]:
        dust_sourceM += f"| {value} | {details} |\n"

    dust_sourceC = "| value | description |\n| --- | --- |\n"
    for details, value in configuration["dust_sourceC"]:
        dust_sourceC += f"| {value} | {details} |\n"

    track_other = "| parameter | value | description |\n| --- | --- | --- |\n"
    for details, value in configuration["track_parsec"]["eta_reimers"]:
        track_other += f"| `eta_reimers` | {value} | {details} |\n"
    for details, value in configuration["track_parsec"]["n_inTPC"]:
        track_other += f"| `n_inTPC` | {value} | {details} |\n"

    extinction = "| parameter | value | description |\n| --- | --- | --- |\n"
    for key, value in configuration["extinction"].items():
        for details, value in value:
            extinction += f"| `{key}` | {value} | {details} |\n"

    lpvs = "| value | description |\n| --- | --- |\n"
    for details, value in configuration["lpvs"]["kind_LPV"]:
        lpvs += f"| {value} | {details} |\n"

    imf = "| value | description | filename |\n| --- | --- | --- |\n"
    for key, (details, value) in configuration["imf_file"].items():
        imf += f"| {key} | {details} | {value} |\n"

    defaults = "| parameter | value |\n| --- | --- |\n"
    for key, value in configuration["defaults"].items():
        defaults += f"| `{key}` | {value} |\n"

    text = dedent(text).format(**locals())

    return text


def update_config():
    """Update the configuration of the package from parsing the website"""
    _get_page_info()


def validate_query_parameter(**kw):
    """
    Validates the query parameters for isochrone generation.

    Parameters:
        kw (dict): A dictionary of keyword arguments containing the following keys

            - isoc_agelow : float, Lower age limit.
            - isoc_ageupp : float, Upper age limit.
            - isoc_lagelow : float, Lower log age limit.
            - isoc_lageupp : float, Upper log age limit.
            - isoc_zlow : float, Lower metallicity (Z) limit.
            - isoc_zupp : float, Upper metallicity (Z) limit.
            - isoc_metlow : float, Lower [M/H] limit.
            - isoc_metupp : float, Upper [M/H] limit.
            - photsys_file : str, Photometric system file.
            - imf_file : str, Initial Mass Function (IMF) file.
            - track_parsec : str, PARSEC track identifier.
            - track_omegai : float, Initial rotation velocity.
            - track_colibri : str, COLIBRI track identifier.
            - dust_sourceC : str, Dust source for carbon stars.
            - dust_sourceM : str, Dust source for M-type stars.
            - extinction_coeff : str, Extinction coefficient.
            - extinction_curve : str, Extinction curve.
            - kind_LPV : str, Long Period Variable (LPV) kind.
            - photsys_version : str, Photometric system version.

    Raises:
        ValueError: If any of the parameters are invalid or out of the expected range.
    """
    # check parameters validity
    acceptable_age = [1, 1e12]
    acceptable_lage = [0, 12]

    if float(kw["isoc_agelow"]) > float(kw["isoc_ageupp"]):
        raise ValueError(
            f'Lower age must be less than upper age. Got {kw["isoc_agelow"]} and {kw["isoc_ageupp"]} instead.'
        )
    if float(kw["isoc_lagelow"]) > float(kw["isoc_lageupp"]):
        raise ValueError(
            f'Lower log age must be less than upper log age. Got {kw["isoc_lagelow"]} and {kw["isoc_lageupp"]} instead.'
        )

    if not acceptable_age[0] <= float(kw["isoc_agelow"]) <= acceptable_age[1]:
        raise ValueError(
            f'Lower age must be between {acceptable_age[0]} and {acceptable_age[1]}. Got {kw["isoc_agelow"]} instead.'
        )
    if not acceptable_age[0] <= float(kw["isoc_ageupp"]) <= acceptable_age[1]:
        raise ValueError(
            f'Upper age must be between {acceptable_age[0]} and {acceptable_age[1]}. Got {kw["isoc_ageupp"]} instead.'
        )
    if not acceptable_lage[0] <= float(kw["isoc_lagelow"]) <= acceptable_lage[1]:
        raise ValueError(
            f'Lower log age must be between {acceptable_lage[0]} and {acceptable_lage[1]}. Got {kw["isoc_lagelow"]} instead.'
        )
    if not acceptable_lage[0] <= float(kw["isoc_lageupp"]) <= acceptable_lage[1]:
        raise ValueError(
            f'Upper log age must be between {acceptable_lage[0]} and {acceptable_lage[1]}. Got {kw["isoc_lageupp"]} instead.'
        )

    acceptable_Z = [1e-8, 1.0]
    acceptable_met = [-8, 1]
    if float(kw["isoc_zlow"]) > float(kw["isoc_zupp"]):
        raise ValueError(
            f'Lower Z must be less than upper Z. Got {kw["isoc_zlow"]} and {kw["isoc_zupp"]} instead.'
        )
    if float(kw["isoc_metlow"]) > float(kw["isoc_metupp"]):
        raise ValueError(
            f'Lower [M/H] must be less than upper [M/H]. Got {kw["isoc_metlow"]} and {kw["isoc_metupp"]} instead.'
        )
    if not acceptable_Z[0] <= float(kw["isoc_zlow"]) <= acceptable_Z[1]:
        raise ValueError(
            f'Lower Z must be between {acceptable_Z[0]} and {acceptable_Z[1]}. Got {kw["isoc_zlow"]} instead.'
        )
    if not acceptable_Z[0] <= float(kw["isoc_zupp"]) <= acceptable_Z[1]:
        raise ValueError(
            f'Upper Z must be between {acceptable_Z[0]} and {acceptable_Z[1]}. Got {kw["isoc_zupp"]} instead.'
        )
    if not acceptable_met[0] <= float(kw["isoc_metlow"]) <= acceptable_met[1]:
        raise ValueError(
            f'Lower [M/H] must be between {acceptable_met[0]} and {acceptable_met[1]}. Got {kw["isoc_metlow"]} instead.'
        )
    if not acceptable_met[0] <= float(kw["isoc_metupp"]) <= acceptable_met[1]:
        raise ValueError(
            f'Upper [M/H] must be between {acceptable_met[0]} and {acceptable_met[1]}. Got {kw["isoc_metupp"]} instead.'
        )

    if (
        float(kw["isoc_dage"]) < 0
        or float(kw["isoc_dlage"]) < 0
        or float(kw["isoc_dz"]) < 0
        or float(kw["isoc_dmet"]) < 0
    ):
        raise ValueError(
            "Age, log age, Z, and [M/H] step sizes must be positive or null."
        )

    if len(configuration) <= 2:
        reload_configuration()

    if kw["photsys_file"] not in configuration["photsys_file"] and not kw[
        "photsys_file"
    ].endswith(".dat"):
        raise ValueError(f'Invalid photometric system file: {kw["photsys_file"]}')

    if kw["imf_file"] not in configuration["imf_file"] and not kw["imf_file"].endswith(
        ".dat"
    ):
        raise ValueError(f'Invalid IMF file: {kw["imf_file"]}')

    track_parsec = [k[1] for k in configuration["track_parsec"]["track_parsec"]]
    if kw["track_parsec"] not in track_parsec:
        raise ValueError(f'Invalid isochrone kind: {kw["track_parsec"]}')

    if not 0 <= float(kw["track_omegai"]) <= 0.99:
        raise ValueError(
            f'Invalid initial rotation velocity. Must be between 0 and 0.99. Found {kw["track_omegai"]} instead.'
        )

    track_colibri = [k[1] for k in configuration["track_parsec"]["track_colibri"]]
    if kw["track_colibri"] not in track_colibri:
        raise ValueError(f'Invalid isochrone kind: {kw["track_colibri"]}')

    dust_sourceC = [k[1] for k in configuration["dust_sourceC"]]
    if kw["dust_sourceC"] not in dust_sourceC:
        raise ValueError(f'Invalid dust source: {kw["dust_sourceC"]}')

    dust_sourceM = [k[1] for k in configuration["dust_sourceM"]]
    if kw["dust_sourceM"] not in dust_sourceM:
        raise ValueError(f'Invalid dust source: {kw["dust_sourceM"]}')

    extinction_coef = [k[1] for k in configuration["extinction"]["extinction_coeff"]]
    if kw["extinction_coeff"] not in extinction_coef:
        raise ValueError(f'Invalid extinction coefficient: {kw["extinction_coeff"]}')

    extinction_curve = [k[1] for k in configuration["extinction"]["extinction_curve"]]
    if kw["extinction_curve"] not in extinction_curve:
        raise ValueError(f'Invalid extinction curve: {kw["extinction_curve"]}')

    kind_LPV = [k[1] for k in configuration["lpvs"]["kind_LPV"]]
    if kw["kind_LPV"] not in kind_LPV:
        raise ValueError(f'Invalid LPV kind: {kw["kind_LPV"]}')

    photsys_version = [k[1] for k in configuration["photsys_file"]["photsys_version"]]
    if kw["photsys_version"] not in photsys_version:
        raise ValueError(f'Invalid photometric system version: {kw["photsys_version"]}')
