EZPADOVA -- A python package that allows you to download PADOVA isochrones directly from their website
======================================================================================================


This small package provides a direct interface to the PADOVA/PARSEC isochrone
webpage (http://stev.oapd.inaf.it/cgi-bin/cmd).
It compiles the URL needed to query the website and retrives the data into a
python variable.

This package has been tested on python 2.7 and python 3.

:version: 1
:author: MF


TODO list
---------
* make a full documentation
* cleanup the mess


EXAMPLE USAGE
-------------

* Basic example of downloading a sequence of isochrones, plotting, saving
```python 
>>> r = cmd.get_t_isochrones(6.0, 7.0, 0.05, 0.02)
>>> import pylab as plt
>>> plt.scatter(r['logT'], r['logL'], c=r['logA'], edgecolor='None')
>>> plt.show()
>>> r.write('myiso.fits')
```

* getting only one isochrone
```python 
>>> r = cmd.get_one_isochrones(1e7, 0.02, model='parsec12s', phot='spitzer')
```

Available model interfaces
--------------------------
`parsec12s_r14`: PARSEC version 1.2S + TP-AGB tracks from COLIBRI (Marigo et al. (2013)), version PR16 (Rosenfield et al. (2016)).

`parsec12s`: PARSEC version 1.2S,  Tang et al. (2014),  Chen et al. (2014)

`parsec11`: PARSEC version 1.1, With revised diffusion+overshooting in
low-mass stars, and improvements in interpolation scheme.

`parsec10`: PARSEC version 1.0

`2010`: Marigo et al. (2008) with the Girardi et al. (2010) Case A correction
for low-mass, low-metallicity AGB tracks

`2008`: Marigo et al. (2008): Girardi et al. (2000) up to early-AGB +
detailed TP-AGB from Marigo & Girardi (2007) (for M <= 7 Msun) + Bertelli et al.
(1994) (for M > 7 Msun) + additional Z=0.0001 and Z=0.001 tracks.

`2010b`: Marigo et al. (2008) with the Girardi et al. (2010) Case B correction
for low-mass, low-metallicity AGB tracks

`2002`:  Basic set of Girardi et al. (2002) : Girardi et al. (2000) +
simplified TP-AGB (for M <= 7 Msun) + Bertelli et al.  (1994) (for M > 7 Msun) +
additional Z=0.0001 and Z=0.001 tracks.

Photometric systems 
-------------------
(incomplete list)


`2mass_spitzer`:  2MASS + Spitzer (IRAC+MIPS)

`2mass_spitzer_wise`:  2MASS + Spitzer (IRAC+MIPS) + WISE

`2mass`:  2MASS JHKs

`ubvrijhk`: UBVRIJHK (cf. Maiz-Apellaniz 2006 + Bessell 1990)

`bessell`: UBVRIJHKLMN (cf. Bessell 1990 + Bessell & Brett 1988)

`akari`: AKARI

`batc`: BATC

`megacam`: CFHT/Megacam u g'r'i'z'

`dcmc`: DCMC

`denis`: DENIS

`dmc14`: DMC 14 filters

`dmc15`: DMC 15 filters

`eis`: ESO/EIS (WFI UBVRIZ + SOFI JHK)

`wfi`: ESO/WFI

`wfi_sofi`: ESO/WFI+SOFI

`wfi2`: ESO/WFI2

`galex`: GALEX FUV+NUV (Vegamag) + Johnson's UBV

`galex_sloan`: GALEX FUV+NUV + SDSS ugriz (all ABmags) 

`UVbright`: HST+GALEX+Swift/UVOT UV filters

`acs_hrc`: HST/ACS HRC

`acs_wfc`: HST/ACS WFC

`nicmosab`: HST/NICMOS AB

`nicmosst`: HST/NICMOS ST

`nicmosvega`: HST/NICMOS vega

`stis`: HST/STIS imaging mode

`wfc3ir`: HST/WFC3 IR channel (final throughputs)

`wfc3uvis1`: HST/WFC3 UVIS channel, chip 1 (final throughputs)

`wfc3uvis2`: HST/WFC3 UVIS channel, chip 2 (final throughputs)

`wfc3_medium`: HST/WFC3 medium filters (UVIS1+IR, final throughputs)

`wfc3`: HST/WFC3 wide filters (UVIS1+IR, final throughputs)

`wfpc2`: HST/WFPC2 (Vegamag, cf. Holtzman et al. 1995)

`kepler`: Kepler + SDSS griz + DDO51 (in ABmags)

`kepler_2mass`: Kepler + SDSS griz + DDO51 (in ABmags) + 2MASS (~Vegamag)

`ogle`: OGLE-II

`panstarrs1`: Pan-STARRS1

`sloan`: SDSS ugriz

`sloan_2mass`: SDSS ugriz + 2MASS JHKs

`sloan_ukidss`: SDSS ugriz + UKIDSS ZYJHK

`swift_uvot`: SWIFT/UVOT UVW2, UVM2, UVW1,u (Vegamag) 

`spitzer`: Spitzer IRAC+MIPS

`stroemgren`: Stroemgren-Crawford

`suprimecam`: Subaru/Suprime-Cam (ABmags)

`tycho2`: Tycho VTBT

`ukidss`: UKIDSS ZYJHK (Vegamag)

`visir`: VISIR

`vista`: VISTA ZYJHKs (Vegamag)

`washington`: Washington CMT1T2

`washington_ddo51`: Washington CMT1T2 + DDO51
