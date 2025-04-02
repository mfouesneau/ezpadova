EZPADOVA -- A python package that allows you to download PADOVA isochrones directly from their website
======================================================================================================

[![](https://img.shields.io/badge/Parsec_CMD-3.8-green.svg)](http://stev.oapd.inaf.it/cgi-bin/cmd_3.8)
![](https://img.shields.io/badge/python-3.9,_3.10,_3.11,_3.12-blue.svg)

This small package provides a direct interface to the PADOVA/PARSEC isochrone
webpage (http://stev.oapd.inaf.it/cgi-bin/cmd).
It compiles the URL needed to query the website and retrieves the data into a
python variable.

This package has been tested on Python 3.9, 3.10, 3.11, and 3.12 through the GitHub actions CI.

> ℹ️ If you use this package, please use the citation information. Please do not forget also to cite the PARSEC work listed on their website.

New in version 2.0
------------------
* Updated the interface to the new PADOVA website (i.e. >=3.8) [minor changes in the form format from 3.7]
* New function `get_isochrone` does all the slices directly (combines `get_Z_isochrones`, `get_t_isochrones`, and `get_one_isochrone` which are now deprecated.)
* `get_isochrone` handles ages, log ages, Z and [M/H] as inputs (see documentation).
* Most of the code has been rewritten to be more robust and easier to maintain. In particular, the parsing of the online form has been improved.
* Many integration tests to keep checking the package interface.
* The output format is now a `pandas.DataFrame` instead of the internal format. (though previous aliases of columns are no longer available)
* added `resample_evolution_phase` function to resample the `label` into a continuous evolution phase instead of discrete labels.
* added `interpolate.QuickInterpolator` to quickly interpolate isochrones over (logage, MH, evolution phase)
* Documentation has been updated and (hopefully) improved.

Available photometric systems, parameters, and default values: [see internal documentation](src/ezpadova/parsec.md)

Installation
------------
Install with pip

```
pip install git+https://github.com/mfouesneau/ezpadova
```
(`--user` if you want to install it in your user profile)

Manual installation

download the repository and pip install from it

```python
git clone https://github.com/mfouesneau/ezpadova
cd ezpadova
python -m pip install . 
```

Example Usage
-------------
Since v2.0, ezpadova combines all queries through a single function, `get_isochrones`. 

The following example queries the Padova service to retrieve a set of isochrones spanning ages and metallicities
```python
import ezpadova
import matplotlib.pyplot as plt
r = ezpadova.get_isochrones(photsys_file='gaiaEDR3', logage=(6, 10, 0.2), MH=(-2, 1, 0.4))
```

The following example queries the Padova service to retrieve log(age/yr)-space isochrones at solar metallicity and the Gaia eDR3 photometry.
```python
import ezpadova
import matplotlib.pyplot as plt
r = ezpadova.get_isochrones(logage=(6, 7, 0.1), MH=(0, 0, 0), photsys_file='gaiaEDR3')
plt.scatter(r['logTe'], r['logL'], c=r['logAge'], edgecolor='None')
plt.show()
```
