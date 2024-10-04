import pytest
import pandas as pd
from .deprecated import get_t_isochrones, get_one_isochrone, get_Z_isochrones


@pytest.mark.filterwarnings("ignore::DeprecationWarning")
def test_get_t_isochrones():
    # Test with valid Z and logt range
    result = get_t_isochrones(logt0=8.0, logt1=9.0, dlogt=0.1, Z=0.02)
    assert isinstance(result, (pd.DataFrame, bytes))

    # Test with valid MH and logt range
    result = get_t_isochrones(logt0=8.0, logt1=9.0, dlogt=0.1, MH=0.0)
    assert isinstance(result, (pd.DataFrame, bytes))

    # Test with invalid Z and MH both provided
    with pytest.raises(ValueError, match="Only one of Z or MH can be provided."):
        get_t_isochrones(logt0=8.0, logt1=9.0, dlogt=0.1, Z=0.02, MH=0.0)

    # Test with neither Z nor MH provided
    with pytest.raises(ValueError, match="Either Z or MH must be provided."):
        get_t_isochrones(logt0=8.0, logt1=9.0, dlogt=0.1)

    # Test with invalid logt range (logt0 > logt1)
    with pytest.raises(ValueError):
        get_t_isochrones(logt0=9.0, logt1=8.0, dlogt=0.1, Z=0.02)

    # Test with invalid dlogt (negative step size)
    with pytest.raises(ValueError):
        get_t_isochrones(logt0=8.0, logt1=9.0, dlogt=-0.1, Z=0.02)

@pytest.mark.filterwarnings("ignore::DeprecationWarning")
def test_get_one_isochrone():
    # Test with valid age_yr and Z
    result = get_one_isochrone(age_yr=1e9, Z=0.02)
    assert isinstance(result, (pd.DataFrame, bytes))

    # Test with valid logage and MH
    result = get_one_isochrone(logage=9.0, MH=0.0)
    assert isinstance(result, (pd.DataFrame, bytes))

    # Test with invalid age_yr and logage both provided
    with pytest.raises(ValueError, match="Only one of age_yr or logage can be provided."):
        get_one_isochrone(age_yr=1e9, logage=9.0, Z=0.02)

    # Test with neither age_yr nor logage provided
    with pytest.raises(ValueError, match="Either age_yr or logage must be provided."):
        get_one_isochrone(Z=0.02)

    # Test with invalid Z and MH both provided
    with pytest.raises(ValueError, match="Only one of Z or MH can be provided."):
        get_one_isochrone(age_yr=1e9, Z=0.02, MH=0.0)

    # Test with neither Z nor MH provided
    with pytest.raises(ValueError, match="Either Z or MH must be provided."):
        get_one_isochrone(age_yr=1e9)

@pytest.mark.filterwarnings("ignore::DeprecationWarning")
def test_get_Z_isochrones():
    # Test with valid Z range and age_yr
    result = get_Z_isochrones(z0=0.01, z1=0.03, dz=0.01, age_yr=1e9)
    assert isinstance(result, (pd.DataFrame, bytes))

    # Test with valid Z range and logage
    result = get_Z_isochrones(z0=0.01, z1=0.03, dz=0.01, logage=9.0)
    assert isinstance(result, (pd.DataFrame, bytes))

    # Test with invalid age_yr and logage both provided
    with pytest.raises(ValueError, match="Only one of age_yr or logage can be provided."):
        get_Z_isochrones(z0=0.01, z1=0.03, dz=0.01, age_yr=1e9, logage=9.0)

    # Test with neither age_yr nor logage provided
    with pytest.raises(ValueError, match="Either age_yr or logage must be provided."):
        get_Z_isochrones(z0=0.01, z1=0.03, dz=0.01)

    # Test with invalid Z range (z0 > z1)
    with pytest.raises(ValueError):
        get_Z_isochrones(z0=0.03, z1=0.01, dz=0.01, age_yr=1e9)

    # Test with invalid dz (negative step size)
    with pytest.raises(ValueError):
        get_Z_isochrones(z0=0.01, z1=0.03, dz=-0.01, age_yr=1e9)