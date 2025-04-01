
# EzPadova configuration file

_This file contains the configuration for the EzPadova package. It is generated automatically by the package and should not be modified manually._

All detailed description of the parameters can be found on the [CMD webpage](http://stev.oapd.inaf.it/cgi-bin/cmd).

## Track flavors `track_parsec`

| value | description |
| --- | --- |
| parsec_CAF09_v2.0 | PARSEC version 2.0   Available for 0.002≤ Z ≤0.03 (-0.89≤[M/H]≤+0.34), with rotation turned off for the lowest masses. The 0.004≤ Z ≤0.017 tracks are described in  Nguyen et al. (2022) ; outside this range we are using preliminary tracks from Nguyen et al. (in preparation).  with ωi=  (in the range 0≤ωi≤0.99). Notes: this choice will (1) turn off features like the star-by-star extinction, the Reimers-resettable mass loss, etc. and (2) change the output format. |
| parsec_CAF09_v1.2S | PARSEC version 1.2S   Available for 0.0001≤ Z ≤0.06 (-2.2≤[M/H]≤+0.5); for 0.0001≤ Z ≤0.02 the mass range is 0.1≤ M/M ☉<350; for 0.03≤ Z ≤0.04 0.1≤ M/M ☉<150, and for  Z =0.06 0.1≤ M/M ☉<20 (cf.  Tang et al. (2014)  for 0.001≤ Z ≤0.004, and  Chen et al. (2015)  for other  Z ). With revised and calibrated surface boundary conditions in low-mass dwarfs ( Chen et al. (2014) ). |
| parsec_CAF09_v1.1 | PARSEC version 1.1    Available for 0.0001≤Z≤0.06 (-2.2≤[M/H]≤+0.5), in the range 0.1≤M/M☉<12. With revised diffusion+overshooting in low-mass stars, and improvements in interpolation scheme. |
| parsec_CAF09_v1.0 | PARSEC version 1.0    Available for 0.0005≤Z≤0.07 (-1.5≤[M/H]≤+0.6), in the range 0.1≤M/M☉<12. |


### Track Rotation `track_omegai`

_only available for PARSEC 2.0_

| value | description |
| --- | --- |
| 0.00 |  (in the range 0≤ω i ≤0.99).   Notes: this choice will (1) turn off features like the star-by-star extinction, the Reimers-resettable mass loss, etc. and (2) change the output format. |


### Track COLIBRI `track_colibri`

_only available for PARSEC 1.2S_

| value | description |
| --- | --- |
| parsec_CAF09_v1.2S_S_LMC_08_web | + COLIBRI S_37 ( Pastorelli et al. (2020) ) for 0.008≤ Z ≤0.02, + COLIBRI S_35 ( Pastorelli et al. (2019) ) for 0.0005≤ Z ≤0.006 + COLIBRI PR16 ( Marigo et al. (2013) ,  Rosenfield et al. (2016) ) for  Z ≤0.0002 and  Z ≥0.03 ) |
| parsec_CAF09_v1.2S_S35 | + COLIBRI S_35 ( Pastorelli et al. (2019) )  (limited to 0.0005≤Z≤0.03) |
| parsec_CAF09_v1.2S_S07 | + COLIBRI S_07 ( Pastorelli et al. (2019) )  (limited to 0.0005≤Z≤0.03) |
| parsec_CAF09_v1.2S_NOV13 | + COLIBRI PR16 ( Marigo et al. (2013)  and  Rosenfield et al. (2016) )  (limited to 0.0001≤Z≤0.06) |
| no | No   (no limitation in Z) |


### additional parameters

| parameter | value | description |
| --- | --- | --- |
| `eta_reimers` | 0.2 |  |
| `n_inTPC` | 10 |  as detailed in  Marigo et al. (2017)   |


## Photometric systems `photsys_file`

| value | description |
| --- | --- |
| 2mass_spitzer | 2MASS + Spitzer (IRAC+MIPS) |
| 2mass_spitzer_wise | 2MASS + Spitzer (IRAC+MIPS) + WISE |
| 2mass | 2MASS JHKs |
| ogle_2mass_spitzer | OGLE + 2MASS + Spitzer (IRAC+MIPS) |
| ubvrijhk | UBVRIJHK (cf. Maiz-Apellaniz 2006 + Bessell 1990) |
| bessell | UBVRIJHKLMN (cf. Bessell 1990 + Bessell & Brett 1988) |
| akari | AKARI |
| batc | BATC |
| megacam_wircam | CFHT Megacam + Wircam (all ABmags) |
| wircam | CFHT Wircam |
| megacam_post2014 | CFHT/Megacam post-2014 u*g'r'i'z' |
| megacam | CFHT/Megacam pre-2014 u*g'r'i'z' |
| ciber | CIBER |
| clue_galex | CLUE + GALEX (Vegamags) |
| CSST | CSST (ABmags) |
| decam | DECAM (ABmags) |
| denis | DENIS |
| dmc14 | DMC 14 filters |
| dmc15 | DMC 15 filters |
| eis | ESO/EIS (WFI UBVRIZ + SOFI JHK) |
| wfi | ESO/WFI |
| wfi2 | ESO/WFI2 |
| euclid_nisp | Euclid VIS+NISP (ABmags) |
| galex_sloan | GALEX FUV+NUV (Vegamag) + SDSS ugriz (ABmags) |
| galex | GALEX FUV+NUV + Johnson's UBV (Maiz-Apellaniz version), all Vegamags |
| gaia_tycho2_2mass | Gaia DR1 + Tycho2 + 2MASS (all Vegamags) |
| gaiaDR2_tycho2_2mass | Gaia DR2 + Tycho2 + 2MASS (all Vegamags, Gaia passbands from Evans et al. 2018) |
| gaiaDR2weiler_tycho2_2mass | Gaia DR2 + Tycho2 + 2MASS (all Vegamags, Gaia passbands from Weiler 2018) |
| gaiaEDR3 | Gaia EDR3 (all Vegamags, Gaia passbands from ESA/Gaia website) |
| gaia | Gaia's DR1 G, G_BP and G_RP (Vegamags) |
| gaiaDR2 | Gaia's DR2 G, G_BP and G_RP (Vegamags, Gaia passbands from Evans et al. 2018) |
| gaiaDR2maiz | Gaia's DR2 G, G_BP and G_RP (Vegamags, Gaia passbands from Maiz-Apellaniz and Weiler 2018) |
| gaiaDR2weiler | Gaia's DR2 G, G_BP and G_RP (Vegamags, Gaia passbands from Weiler 2018) |
| UVbright | HST+GALEX+Swift/UVOT UV filters |
| acs_hrc | HST/ACS HRC |
| acs_wfc_pos04jul06 | HST/ACS WFC (c.f. 2007 revision, pos-04jul06) |
| acs_wfc_202101 | HST/ACS WFC - updated filters and zeropoints, 2021 |
| nicmosab | HST/NICMOS AB |
| nicmosvega | HST/NICMOS Vega |
| stis | HST/STIS imaging mode, Vegamag |
| wfc3_wideverywide | HST/WFC3 all W+LP+X filters (UVIS1+IR, final throughputs) |
| wfc3_202101_verywide | HST/WFC3 long-pass and extremely wide filters (UVIS) - updated filters and zeropoints, 2021 |
| wfc3_202101_medium | HST/WFC3 medium filters (UVIS+IR) - updated filters and zeropoints, 2021 |
| wfc3_202101_wide | HST/WFC3 wide filters (UVIS+IR) - updated filters and zeropoints, 2021 |
| wfpc2 | HST/WFPC2 (Vegamag, cf. Holtzman et al. 1995) |
| hipparcos | Hipparcos+Tycho+Gaia DR1 (Vegamags) |
| int_wfc | INT/WFC (Vegamag) |
| iphas | IPHAS |
| jwst_miri_wide | JWST MIRI wide filters, Vegamags |
| jwst_nircam_wide | JWST NIRCam wide+verywide filters, Vegamags |
| jwst_nircam_widemedium_nov22 | JWST NIRCam wide+verywide+medium filters (Nov 2022), Vegamags |
| jwst_nircam_widemedium | JWST NIRCam wide+verywide+medium filters, Vegamags |
| jwst_niriss_nov22 | JWST NIRISS filters (Nov 2022), Vegamags |
| jwst_nirspec | JWST Nirspec filters, Vegamags |
| jwst_fnl | JWST custom, Vegamags |
| kepler | Kepler + SDSS griz + DDO51 (in ABmags) |
| kepler_2mass | Kepler + SDSS griz + DDO51 (in ABmags) + 2MASS (~Vegamag) |
| vst_vista | KiDS/VIKING (VST/OMEGAM + VISTA/VIRCAM, all ABmags) |
| lbt_lbc | LBT/LBC (Vegamag) |
| lsst_wfirst_proposed2017 | LSST (ABmags) + WFIRST proposed filters (Vegamags) |
| lsst | LSST ugrizY, March 2012 total filter throughputs (all ABmags) |
| lsstDP0 | LSST ugrizy, Oct 2017 total filter throughputs for DP0 (all ABmags) |
| lsstR1.9 | LSST ugrizy, Sept 2023, total filter throughputs R1.9 (all ABmags) |
| noao_ctio_mosaic2 | NOAO/CTIO/MOSAIC2 (Vegamag) |
| ogle | OGLE-II |
| panstarrs1 | Pan-STARRS1 |
| gulli | Pan-STARRS1 + narrow Omegacam filters (ABmags) |
| Roman2021 | Roman (ex-WFIRST) 2021 filters, Vegamags |
| splus | S-PLUS (Vegamags), revised on Nov. 2017 |
| sloan | SDSS ugriz |
| sloan_2mass | SDSS ugriz + 2MASS JHKs |
| sloan_ukidss | SDSS ugriz + UKIDSS ZYJHK |
| swift_uvot | SWIFT/UVOT UVW2, UVM2, UVW1,u (Vegamag) |
| skymapper | SkyMapper (ABmags) |
| spitzer | Spitzer IRAC+MIPS |
| stroemgren | Stroemgren-Crawford |
| hsc | Subaru/Hyper Suprime-Cam (ABmags) |
| suprimecam | Subaru/Suprime-Cam (ABmags) |
| SuperBIT | SuperBIT, all ABmags |
| TESS_2mass | TESS + 2MASS (Vegamags) |
| TESS_2mass_kepler | TESS + 2MASS (Vegamags) + Kepler + SDSS griz + DDO51 (in ABmags) |
| ukidss | UKIDSS ZYJHK (Vegamag) |
| uvit | UVIT (all ABmags) |
| visir | VISIR |
| vista | VISTA ZYJHKs (Vegamag) |
| vphas | VPHAS+ (ABmags) |
| vst_omegacam | VST/OMEGACAM (ABmag) |
| vilnius | Vilnius |
| wfc3_uvisCaHK | WFC3/UVIS around CaHK |
| washington_ddo51 | Washington CMT1T2 + DDO51 |
| ztf | ZTF (ABmags) |
| deltaa | deltaa (Paunzen) + UBV (Maiz-Apellaniz), in Vegamags |


## Stellar Atmospheres `photsys_version`

| value | description |
| --- | --- |
| YBC | YBC |
| YBCnewVega | YBC +new Vega |
| odfnew | OBC |


## Circumstellar dust flavors    

### Dust for M stars `dust_sourceM`

| value | description |
| --- | --- |
| nodustM | No dust |
| sil | Silicates as in  Bressan et al. (1998) |
| AlOx | 100% AlOx as in  Groenewegen (2006) |
| dpmod60alox40 | 60% Silicate + 40% AlOx as in  Groenewegen (2006) |
| dpmod | 100% Silicate as in  Groenewegen (2006) |


### Dust for C stars `dust_sourceC`

| value | description |
| --- | --- |
| nodustC | No dust |
| gra | Graphites as in  Bressan et al. (1998) |
| AMC | 100% AMC as in  Groenewegen (2006) |
| AMCSIC15 | 85% AMC + 15% SiC as in  Groenewegen (2006) |


## Extinction

| parameter | value | description |
| --- | --- | --- |
| `extinction_av` | 0.0 |  mag. Apply this extinction Using extinction coefficients computed star-by-star (except for the OBC case, which uses constant coefficients) Adopted extinction curve Cardelli et al. (1989) + O'Donnell (1994), with RV=3.1 Warning: Interstellar extinction works only for isochrone tables, not for LFs or simulated populations. Moreover, it does not work (yet) on the PARSEC rotating models. |
| `extinction_coeff` | constant | Using extinction coefficients computed star-by-star (except for the OBC case, which uses constant coefficients) |
| `extinction_curve` | cardelli | Cardelli et al. (1989)  +  O'Donnell (1994) , with  RV =3.1 |


## LPVs `kind_LPV`

| value | description |
| --- | --- |
| 1 | 1. Periods from  Trabucchi et al. (2017) . |
| 2 | 2. Periods from  Trabucchi et al. (2019) . |
| 3 | 3. Periods from  Trabucchi et al. (2021) . |
| 4 | 4. Periods and dominant regime from  Trabucchi et al. (2021) . |


## IMF `imf_file`

| value | description | filename |
| --- | --- | --- |
| salpeter | Salpeter (1955) with cutoff at 0.01 M☉ | tab_imf/imf_salpeter.dat |
| chabrier_exponential | Chabrier (2001) exponential | tab_imf/imf_chabrier_exponential.dat |
| chabrier_lognormal | Chabrier (2001) lognormal | tab_imf/imf_chabrier_lognormal.dat |
| chabrier_lognormal_salpeter | Chabrier (2001) lognormal + Salpeter (1955) for M>1M☉ | tab_imf/imf_chabrier_lognormal_salpeter.dat |
| kroupa_orig | Kroupa (2001, 2002) canonical two-part-power law IMF, corrected for unresolved binaries | tab_imf/imf_kroupa_orig.dat |


## Default values

| parameter | value |
| --- | --- |
| `cmd_version` | 3.8 |
| `track_omegai` | 0.00 |
| `track_parsec` | parsec_CAF09_v1.2S |
| `track_colibri` | parsec_CAF09_v1.2S_S_LMC_08_web |
| `track_postagb` | no |
| `n_inTPC` | 10 |
| `eta_reimers` | 0.2 |
| `kind_interp` | 1 |
| `kind_postagb` | -1 |
| `photsys_file` | YBC_tab_mag_odfnew/tab_mag_ubvrijhk.dat |
| `photsys_version` | YBCnewVega |
| `dust_sourceM` | dpmod60alox40 |
| `dust_sourceC` | AMCSIC15 |
| `kind_mag` | 2 |
| `kind_dust` | 0 |
| `extinction_av` | 0.0 |
| `extinction_coeff` | constant |
| `extinction_curve` | cardelli |
| `kind_LPV` | 3 |
| `imf_file` | tab_imf/imf_kroupa_orig.dat |
| `isoc_isagelog` | 0 |
| `isoc_agelow` | 1.0e9 |
| `isoc_ageupp` | 1.0e10 |
| `isoc_dage` | 0.0 |
| `isoc_lagelow` | 6.6 |
| `isoc_lageupp` | 10.13 |
| `isoc_dlage` | 0.0 |
| `isoc_ismetlog` | 0 |
| `isoc_zlow` | 0.0152 |
| `isoc_zupp` | 0.03 |
| `isoc_dz` | 0.0 |
| `isoc_metlow` | -2 |
| `isoc_metupp` | 0.3 |
| `isoc_dmet` | 0.0 |
| `output_kind` | 0 |
| `output_evstage` | 1 |
| `lf_maginf` | -15 |
| `lf_magsup` | 20 |
| `lf_deltamag` | 0.5 |
| `sim_mtot` | 1.0e4 |
| `submit_form` | Submit |


