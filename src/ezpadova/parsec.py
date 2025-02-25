""" Module for querying the CMD website and parsing the results. """
import re
import zlib
from io import BufferedReader, BytesIO
from typing import Tuple, Union
from urllib.request import urlopen

import pandas as pd
import numpy as np
import requests

from .config import configuration, validate_query_parameter
from .tools import get_file_archive_type


def build_query(**kwargs) -> dict:
    """
    Update parameters to match the website requirements.

    This function takes keyword arguments, updates them with default values from
    the configuration, and modifies certain keys to match the expected format
    required by the website.

    Parameters
    ----------
    kwargs : dict
        Arbitrary keyword arguments that will be used to update the default
        configuration values and passed as values to the online form.

    Returns
    -------
    dict
        A dictionary of updated parameters with keys modified to match the
        website's requirements.
    """
    kw = configuration["defaults"].copy()
    kw.update(kwargs)

    # update some keys to match the website requirements
    if not kw["photsys_file"].endswith(".dat"):
        kw["photsys_file"] = f"YBC_tab_mag_odfnew/tab_mag_{kw['photsys_file']}.dat"
    if not kw["imf_file"].endswith(".dat"):
        kw["imf_file"] = f"tab_imf/imf_{kw['imf_file']}.dat"
    return kw


def parse_result(
    data: Union[str, bytes, BufferedReader], comment: str = "#"
) -> pd.DataFrame:
    """
    Parses the input data and returns a pandas DataFrame.

    Parameters:
        data (str | bytes | BufferedReader): The input data to be parsed. It can be a string, bytes, or a BufferedReader object.
        comment (str): The character used to denote comment lines in the input data. Default is '#'.

    Returns:
        pd.DataFrame: A pandas DataFrame containing the parsed data. The DataFrame will have an attribute 'comment' which contains the comment lines from the input data.

    .. note::

        - If the input data is a BufferedReader, it will be read and decoded as 'utf-8'.
        - The function assumes that the header line is the first non-comment line in the input data.
        - The DataFrame is created by reading the input data with pandas.read_csv, using whitespace as the delimiter.
        - The comment lines from the input data are stored in the 'comment' attribute of the DataFrame.

    """

    if isinstance(data, BufferedReader):
        data = data.read()

    split_txt = data.decode("utf-8").split("\n")
    for num, line in enumerate(split_txt):
        if line[0] != comment:
            break
    start = num - 1
    header = split_txt[start].replace("#", "").strip().split()
    df = pd.read_csv(
        BytesIO(data), skiprows=start + 1, sep=r"\s+", names=header, comment="#"
    )
    df.attrs["comment"] = "\n".join(
        k.replace("#", "").strip() for k in split_txt[:start]
    )
    return df


def query(**kwargs) -> bytes:
    """
    Query the CMD webpage with the given parameters.

    This function sends a POST request to the CMD webpage specified in the
    configuration and retrieves the resulting data. The data is then processed
    and returned as bytes. If the server response is incorrect or if there is
    an issue with the data retrieval, a RuntimeError is raised.

    Args:
        **kwargs: Arbitrary keyword arguments to be included in the query.

    Returns:
        bytes: The retrieved data from the CMD webpage.

    Raises:
        RuntimeError: If the server response is incorrect or if there is an
                      issue with data retrieval.
    """
    print(f"Querying {configuration['url']}...")
    kw = build_query(**kwargs)
    req = requests.post(configuration["url"], params=kw, timeout=120, allow_redirects=True)
    if req.status_code != 200:
        raise RuntimeError("Server Response is incorrect")
    else:
        print("Retrieving data...")

    fname = re.compile(r"output\d+").findall(req.text)
    domain = "/".join(configuration["url"].split("/")[:3])
    if len(fname) > 0:
        data_url = f"{domain}/tmp/{fname[0]}.dat"
        print(f"Downloading data...{data_url}")
        bf = urlopen(data_url)
        r = bf.read()
        typ = get_file_archive_type(r, stream=True)
        if typ is not None:
            r = zlib.decompress(bytes(r), 15 + 32)
        return r
    else:
        print("URL:" + configuration["url"] + req.request.path_url + '\n')
        print(req.text)
        raise RuntimeError("Server Response not expected. Error in data retrieval.")


def get_isochrones(
    age_yr: Union[Tuple[float, float, float], None] = None,
    Z: Union[Tuple[float, float, float], None] = None,
    logage: Union[Tuple[float, float, float], None] = None,
    MH: Union[Tuple[float, float, float], None] = None,
    default_ranges: bool = False,
    return_df: bool = True,
    **kwargs,
) -> Union[pd.DataFrame, bytes]:
    """
    Retrieve isochrones based on specified parameters.

    Parameters:
        age_yr (Tuple[float, float, float] | None): A triplet of
            numbers representing the lower bound, upper bound, and step size for age
            in years.  Either `age_yr` or `logage` must be provided, but not both.
        Z (Tuple[float, float, float] | None): 
            A triplet of numbers representing the lower bound, upper bound, and step size for metallicity Z.
            Either `Z` or `MH` must be provided, but not both.
        logage (Tuple[float, float, float] | None): 
            A triplet of numbers representing the lower bound, upper bound, and step size for logarithmic age.
            Either `logage` or `age_yr` must be provided, but not both.
        MH (Tuple[float, float, float] | None): 
            A triplet of numbers representing the lower bound, upper bound, and step size for metallicity [M/H].
            Either `MH` or `Z` must be provided, but not both.
        default_ranges (bool, optional):
            If True, use the default parameter ranges. Default is False.
        return_df (bool, optional):
            If True, return the result as a pandas DataFrame. If False, return the raw bytes. Default is True.
        kwargs (dict):
            Additional keyword arguments to pass to the query.

    Returns:
        pd.DataFrame | bytes: The queried isochrones, either as a pandas DataFrame or raw bytes, depending on the value of `return_df`.

    Raises:
        ValueError: If the provided parameters are inconsistent or invalid.
    """

    kw = configuration["defaults"].copy()
    kw.update(kwargs)

    # default_ranges means using the forms default values - no parameters are provided
    if not default_ranges:
        # check parameter consistency
        if age_yr is None and logage is None:
            raise ValueError("Either age_yr or logage must be provided.")
        if age_yr is not None and logage is not None:
            raise ValueError("Only one of age_yr or logage can be provided.")

        if Z is None and MH is None:
            raise ValueError("Either Z or MH must be provided.")
        if Z is not None and MH is not None:
            raise ValueError("Only one of Z or MH can be provided.")

        # check that any of the parameters are None or a triplet of Numbers
        for name, param in zip(
            ("age_yr", "Z", "logage", "MH"), (age_yr, Z, logage, MH)
        ):
            if param is not None:
                if not isinstance(param, (list, tuple)) or len(param) != 3:
                    raise ValueError(
                        f"Parameter {name} must be a triplet of Numbers or None. Found {param} instead."
                    )

        # setup linear age / log age query
        if age_yr is not None:
            kw["isoc_isagelog"] = 0
            for key, val in zip(("isoc_agelow", "isoc_ageupp", "isoc_dage"), age_yr):
                kw[key] = val
        else:
            kw["isoc_isagelog"] = 1
            for key, val in zip(("isoc_lagelow", "isoc_lageupp", "isoc_dlage"), logage):
                kw[key] = val

        # setup metallicity query in Z or [M/H]
        if Z is not None:
            kw["isoc_ismetlog"] = 0
            for key, val in zip(("isoc_zlow", "isoc_zupp", "isoc_dz"), Z):
                kw[key] = val
        else:
            kw["isoc_ismetlog"] = 1
            for key, val in zip(("isoc_metlow", "isoc_metupp", "isoc_dmet"), MH):
                kw[key] = val

    # check parameters validity
    validate_query_parameter(**kw)

    # do the actual query
    res = query(**kw)

    # parse to dataframe if requested (default)
    if return_df:
        return parse_result(res)
    else:
        return res


def resample_evolution_label(data: pd.DataFrame) -> pd.DataFrame:
    """
    Resample the evolution label in the given DataFrame.

    This function processes the input DataFrame by grouping it based on 'logAge' and 'MH' columns,
    and then resamples the 'label' column to add a continuous 'evol' column. The 'evol' column
    represents the evolution field with continuous quantities.

    parameters:
        data (pd.DataFrame): The input DataFrame containing the 'logAge', 'MH', and 'label' columns.

    Returns:
        pd.DataFrame: The DataFrame with the added 'evol' column containing continuous quantities.
    """

    def _resample_one_isochrone(current: pd.DataFrame) -> pd.DataFrame:
        """
        Add `evol` as an evolution field which expands the label into continuous quantities.
        """
        current["evol"] = 0.0
        for label in set(current["label"].values):
            sub = current[current.label == label]
            delta = 1.0 / len(sub)
            evol = label + np.arange(0, 1 - 0.5 * delta, delta)
            current.loc[current.label == label, "evol"] = evol
        return current

    iso_ = [
        _resample_one_isochrone(k[1]).reset_index()
        for k in data.groupby(["logAge", "MH"])
    ]
    new_data = pd.concat(iso_, axis=0)
    if "index" in new_data.columns:
        new_data.drop("index", axis=1, inplace=True)
    return new_data