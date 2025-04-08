from .deprecated import get_Z_isochrones, get_one_isochrone, get_t_isochrones
from .parsec import get_isochrones, resample_evolution_label
from . import parsec
from .interpolate import QuickInterpolator

__version__ = "2.0.4"

__all__ = ["get_isochrones", "get_Z_isochrones", "get_one_isochrone",
           "get_t_isochrones", "parsec", "QuickInterpolator", "resample_evolution_label"]
