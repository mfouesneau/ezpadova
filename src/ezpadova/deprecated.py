"""Deprecated functions from previous version that are kept here for backward compatibility."""

from typing import Union
from .parsec import get_isochrones
from .tools import deprecated_replacedby
import pandas as pd


@deprecated_replacedby("get_isochrones")
def get_one_isochrone(
    age_yr=None, Z=None, logage=None, MH=None, ret_table=True, **kwargs
) -> Union[pd.DataFrame, bytes]:
    """
    Get one isochrone at a given time and metallicity content.
    Parameters:
        age_yr (float, optional): Age in years. Either `age_yr` or `logage` must be provided, but not both.
        Z (float, optional): Metallicity. Either `Z` or `MH` must be provided, but not both.
        logage (float, optional): Logarithm of age. Either `logage` or `age_yr` must be provided, but not both.
        MH (float, optional): Metallicity in terms of [M/H]. Either `MH` or `Z` must be provided, but not both.
        **kwargs: Additional keyword arguments to be passed to the `get_isochrones` function.
    Returns:
        pd.DataFrame | bytes: containing the isochrone data, format depends on `ret_table` parameter.
    Raises:
        ValueError: If neither `age_yr` nor `logage` is provided.
        ValueError: If both `age_yr` and `logage` are provided.
        ValueError: If neither `Z` nor `MH` is provided.
        ValueError: If both `Z` and `MH` are provided.
    """
    if age_yr is None and logage is None:
        raise ValueError("Either age_yr or logage must be provided.")
    if age_yr is not None and logage is not None:
        raise ValueError("Only one of age_yr or logage can be provided.")
    if Z is None and MH is None:
        raise ValueError("Either Z or MH must be provided.")
    if Z is not None and MH is not None:
        raise ValueError("Only one of Z or MH can be provided.")

    query = {}
    if age_yr is not None:
        query["age_yr"] = [age_yr, age_yr, 0]
    else:
        query["logage"] = [logage, logage, 0]

    if Z is not None:
        query["Z"] = [Z, Z, 0]
    else:
        query["MH"] = [MH, MH, 0]

    return get_isochrones(return_df=ret_table, **query, **kwargs)


@deprecated_replacedby("get_isochrones")
def get_Z_isochrones(
    z0, z1, dz, age_yr=None, logage=None, ret_table=True, **kwargs
) -> Union[pd.DataFrame, bytes]:
    """
    Retrieve isochrones for a given metallicity range and age.

    Parameters:
    z0 (float): Lower bound of the metallicity range in Z units.
    z1 (float): Upper bound of the metallicity range in Z units.
    dz (float): Step size for the metallicity range in Z units.
    age_yr (float, optional): Age in years. Either `age_yr` or `logage` must be provided, but not both.
    logage (float, optional): Logarithm of the age. Either `age_yr` or `logage` must be provided, but not both.
    ret_table (bool, optional): If True, return the result as a DataFrame. Default is True.
    **kwargs: Additional keyword arguments to be passed to the `get_isochrones` function.

    Returns:
    DataFrame | bytes: Isochrones data, format depends on `ret_table` parameter.

    Raises:
    ValueError: If neither `age_yr` nor `logage` is provided, or if both are provided.
    """
    if age_yr is None and logage is None:
        raise ValueError("Either age_yr or logage must be provided.")
    if age_yr is not None and logage is not None:
        raise ValueError("Only one of age_yr or logage can be provided.")

    query = {"Z": [z0, z1, dz]}

    if age_yr is not None:
        query["age_yr"] = [age_yr, age_yr, 0]
    else:
        query["logage"] = [logage, logage, 0]

    return get_isochrones(return_df=ret_table, **query, **kwargs)


@deprecated_replacedby("get_isochrones")
def get_t_isochrones(
    logt0, logt1, dlogt, Z=None, MH=None, ret_table=True, **kwargs
) -> Union[pd.DataFrame, bytes]:
    """
    Retrieve isochrones for a given age range and metallicity.

    Parameters:
    logt0 (float): Lower bound of the age range in log10(years).
    logt1 (float): Upper bound of the age range in log10(years).
    dlogt (float): Step size for the age range in log10(years).
    Z (float, optional): Metallicity. Either `Z` or `MH` must be provided, but not both.
    MH (float, optional): Metallicity in terms of [M/H]. Either `Z` or `MH` must be provided, but not both.
    ret_table (bool, optional): If True, return the result as a DataFrame. Default is True.
    **kwargs: Additional keyword arguments to be passed to the `get_isochrones` function.

    Returns:
    DataFrame | bytes: Isochrones data, format depends on `ret_table` parameter.

    Raises:
    ValueError: If neither `Z` nor `MH` is provided, or if both are provided.
    """
    if Z is None and MH is None:
        raise ValueError("Either Z or MH must be provided.")
    if Z is not None and MH is not None:
        raise ValueError("Only one of Z or MH can be provided.")

    query = {"logage": [logt0, logt1, dlogt]}

    if Z is not None:
        query["Z"] = [Z, Z, 0]
    else:
        query["MH"] = [MH, MH, 0]

    return get_isochrones(return_df=ret_table, **query, **kwargs)
