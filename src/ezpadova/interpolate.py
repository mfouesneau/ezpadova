"""
A quick isochrone interpolator from PARSEC cmd input file.

>>> iso = QuickIsochrone("filename.txt")
>>> cluster_logAge = 8.3
>>> cluster_mh = -0.2
>>> cluster_isochrone = iso(cluster_logAge, cluster_mh)
"""

from itertools import chain
from numbers import Number
from typing import Sequence, Union

import numpy as np
import pandas as pd
from scipy.interpolate import LinearNDInterpolator

from .parsec import parse_result


class QuickInterpolator:
    """Quick and "no so dirty" isochrone interpolation

    Isochrones are defined by (logAge, MH, evolution state) triplet.
    The latter dimension is indicated by `label` in the parsec isochrones. However, only integers are reported.

    For any input (logAge, MH) pair, we first bracket these values with the available models.

    Each of the 4 neighbor combinations corresponding to a single isochrone, we recompute
    the float values of `label` into `evol`.

    Finally, using the 4 isochrones we interpolate any quantity from (logAge, MH, evol) input dimensions.
    The interpolation uses `LinearNDInterpolator`.
    """

    def __init__(self, fname: Union[str, pd.DataFrame]):
        """
        Initialize the interpolation object with isochrone data.

        Parameters
        ----------
        fname : Union[str, pd.DataFrame]
            If a string is provided, it should be the file path to a file containing
            isochrone data. If a pandas DataFrame is provided, it should contain
            the isochrone data directly.

        Attributes
        ----------
        data : pd.DataFrame
            The isochrone data indexed by 'logAge' and 'MH'.
        coords : dict
            A dictionary containing unique values of 'logAge' and 'MH' from the isochrone data.
        ndim : int
            The number of dimensions in the coordinates.
        interpolation_keys : tuple
            A tuple containing the keys used for interpolation: 'logAge', 'MH', 'evol'.
        """
        if isinstance(fname, pd.DataFrame):
            isochrones = fname
        else:
            with open(fname, "r") as f:
                isochrones = parse_result(f)
        self.data = isochrones.set_index(["logAge", "MH"]).drop("index", axis=1)
        self.coords = {
            "logAge": np.unique(isochrones.logAge),
            "MH": np.unique(isochrones.MH),
        }
        self.ndim = len(self.coords)

        self.interpolation_keys = "logAge", "MH", "evol"

    def get_closest_coordinates(self, *args) -> Sequence[Number]:
        """returns the closest (logAge, MH) from the input coordinates"""
        if len(args) != self.ndim:
            raise AttributeError("Coordinates are {0:d} dimensions".format(self.ndim))
        where = [
            val[abs(val - ref).argmin()] for val, ref in zip(self.coords.values(), args)
        ]
        return where

    @staticmethod
    def _bracket(value: Number, sorted_seq: Sequence[Number]) -> Sequence[Number]:
        """returns the interval from the sequence bracketting the given values"""
        if value < sorted_seq[0]:
            return sorted_seq[0], sorted_seq[0]
        for val_min, val_max in zip(sorted_seq, sorted_seq[1:]):
            if val_min <= value < val_max:
                return val_min, val_max
        return sorted_seq[-1], sorted_seq[-1]

    def get_bracket_coordinates(self, *args) -> Sequence[Number]:
        """Get the 4 coordinate pairs around the input (logAge, MH)"""
        if len(args) != self.ndim:
            raise AttributeError("Coordinates are {0:d} dimensions".format(self.ndim))

        where = [
            self._bracket(ref, val) for val, ref in zip(self.coords.values(), args)
        ]
        final_quadrupole = [[(val0, val1) for val1 in where[1]] for val0 in where[0]]
        return list(chain(*final_quadrupole))

    def get_closest(self, logAge: float, MH: float) -> pd.DataFrame:
        """Returns the table corresponding to the closest isochrone from (logAge, MH)"""
        return self.data.loc[self.get_closest_coordinates(logAge, MH)]

    @staticmethod
    def add_evolution_phase(iso: pd.DataFrame, inplace: bool = False) -> pd.DataFrame:
        """Add evol field which expands label into continuous quantities"""
        if inplace:
            current = iso
        else:
            current = iso.copy()
        current["evol"] = 0.0
        for label in set(current["label"].values):
            sub = current[current.label == label]
            delta = 1.0 / len(sub)
            evol = label + np.arange(0, 1 - 0.5 * delta, delta)
            current.loc[current.label == label, "evol"] = evol
        return current

    @staticmethod
    def get_interp_data(iso: pd.DataFrame) -> np.array:
        """Extract interpolation dimensions: (logAge, MH, evol)"""
        logAge = iso.logAge.values[0]
        MH = iso.MH.values[0]
        evol = iso.evol.values
        values = np.array(
            [np.ones_like(evol) * logAge, np.ones_like(evol) * MH, evol]
        ).T
        return values

    def __call__(
        self, logAge: Number, MH: Number, what: Sequence[str] = None
    ) -> pd.DataFrame:
        """
        Interpolate isochrones at given (logAge, MH).

        Parameters
        ----------
        logAge: Number
            The logarithm of the age for interpolation.
        MH: Number
            The metallicity for interpolation.
        what: Sequence[str], optional
            Specific columns to interpolate. If None, all columns are used.

        Returns
        -------
        pd.DataFrame: A DataFrame containing the interpolated isochrones with columns specified in `what`,
                  along with 'logAge', 'MH', and 'evol' columns.
        """
        # make sure we get unique isochrones
        bracket = list(set(self.get_bracket_coordinates(logAge, MH)))

        # get individual isochrones with continuous evolution phases
        iso_ = [
            self.add_evolution_phase(k[1]).reset_index()
            for k in self.data.loc[bracket].groupby(["logAge", "MH"])
        ]

        interp_points = np.vstack([self.get_interp_data(isok) for isok in iso_])

        if what is None:
            what = self.data.columns

        targets = np.vstack([np.vstack([k[what_] for what_ in what]).T for k in iso_])

        # dimensions without dispersion are not useful for interpolation
        # e.g, single age, or single MH.
        useful_dim = np.ptp(interp_points, 0) > 0

        interp_fn = LinearNDInterpolator(interp_points[:, useful_dim], targets)

        phase = np.arange(0, 9, 1e-3)
        values = np.array(
            [np.ones_like(phase) * logAge, np.ones_like(phase) * MH, phase]
        ).T

        res = interp_fn(values[:, useful_dim])
        data = pd.DataFrame.from_records(res, columns=what)
        data["logAge"] = logAge
        data["MH"] = MH
        data["evol"] = phase
        return data.dropna()
