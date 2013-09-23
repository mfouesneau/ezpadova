EZPADOVA -- A python package that allows you to download PADOVA isochrones directly from their website
======================================================================================================


This small package provides a direct interface to the PADOVA/PARSEC isochrone webpage (http://stev.oapd.inaf.it/cgi-bin/cmd).
It compiles the URL needed to query the website and retrives the data into a python variable.

:version: 0.1dev
:author: MF
:requirements: eztables (github.com/mfouesneau/eztables)


TODO list
--------
* test with parsec 1.1 (currently working with cmd2.3/2.5)
* make a full doc
* cleanup the mess


EXAMPLE USAGE
-------------

* Basic example of downloading a sequence of isochrones, plotting, saving
```python 
>>> r = cmd.get_t_isochrones(6.0, 7.0, 0.05, 0.02)
>>> import pylab as plt
>>> plt.scatter(r['logTe'], r['logL/Lo'], c=r['log(age/yr)'], edgecolor='None')
>>> plt.show()
>>> r.write('myiso.fits')
```

* getting only one isochrone
```python 
>>> r = cmd.get_one_isochrones(1e7, 0.02, phot='spitzer')
```
