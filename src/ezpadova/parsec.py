import re
import zlib
from io import BufferedReader, BytesIO
from typing import Tuple, Union
from urllib.request import urlopen

import pandas as pd
import requests

from .config import configuration, validate_query_parameter
from .tools import get_file_archive_type


def build_query(**kwargs) -> dict:
    """
    Update parameters to match the website requirements.

    This function takes keyword arguments, updates them with default values from
    the configuration, and modifies certain keys to match the expected format
    required by the website.

    Parameters:
    **kwargs: Arbitrary keyword arguments that will be used to update the default
              configuration values and passed as values to the online form.

    Returns:
    dict: A dictionary of updated parameters with keys modified to match the
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

    Notes:
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
    req = requests.post(configuration["url"], data=kw, timeout=60, allow_redirects=True)
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
        print(configuration["url"], query)
        print(req.text)
        raise RuntimeError("Server Response is incorrect")


def get_isochrones(
    age_yr: Union[Tuple[float, float, float], None] = None,
    Z: Union[Tuple[float, float, float], None] = None,
    logage: Union[Tuple[float, float, float], None] = None,
    MH: Union[Tuple[float, float, float], None] = None,
    default_ranges: bool = False,
    return_df: bool = True,
    **kwargs,
) -> Union[pd.DataFrame, bytes]:
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


if __name__ == "__main__":
    df = get_isochrones(default_ranges=True)
    print(df)
    print(df.attrs["comment"])
