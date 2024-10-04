
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
| YBC_2mass_spitzer | 2MASS + Spitzer (IRAC+MIPS) |
| YBC_2mass_spitzer_wise | 2MASS + Spitzer (IRAC+MIPS) + WISE |
| YBC_2mass | 2MASS JHKs |
| YBC_ogle_2mass_spitzer | OGLE + 2MASS + Spitzer (IRAC+MIPS) |
| YBC_ubvrijhk | UBVRIJHK (cf. Maiz-Apellaniz 2006 + Bessell 1990) |
| YBC_bessell | UBVRIJHKLMN (cf. Bessell 1990 + Bessell & Brett 1988) |
| YBC_akari | AKARI |
| YBC_batc | BATC |
| YBC_megacam_wircam | CFHT Megacam + Wircam (all ABmags) |
| YBC_wircam | CFHT Wircam |
| YBC_megacam_post2014 | CFHT/Megacam post-2014 u*g'r'i'z' |
| YBC_megacam | CFHT/Megacam pre-2014 u*g'r'i'z' |
| YBC_ciber | CIBER |
| YBC_clue_galex | CLUE + GALEX (Vegamags) |
| YBC_CSST | CSST (ABmags) |
| YBC_decam | DECAM (ABmags) |
| YBC_denis | DENIS |
| YBC_dmc14 | DMC 14 filters |
| YBC_dmc15 | DMC 15 filters |
| YBC_eis | ESO/EIS (WFI UBVRIZ + SOFI JHK) |
| YBC_wfi | ESO/WFI |
| YBC_wfi2 | ESO/WFI2 |
| YBC_euclid_nisp | Euclid VIS+NISP (ABmags) |
| YBC_galex_sloan | GALEX FUV+NUV (Vegamag) + SDSS ugriz (ABmags) |
| YBC_galex | GALEX FUV+NUV + Johnson's UBV (Maiz-Apellaniz version), all Vegamags |
| YBC_gaia_tycho2_2mass | Gaia DR1 + Tycho2 + 2MASS (all Vegamags) |
| YBC_gaiaDR2_tycho2_2mass | Gaia DR2 + Tycho2 + 2MASS (all Vegamags, Gaia passbands from Evans et al. 2018) |
| YBC_gaiaDR2weiler_tycho2_2mass | Gaia DR2 + Tycho2 + 2MASS (all Vegamags, Gaia passbands from Weiler 2018) |
| YBC_gaiaEDR3 | Gaia EDR3 (all Vegamags, Gaia passbands from ESA/Gaia website) |
| YBC_gaia | Gaia's DR1 G, G_BP and G_RP (Vegamags) |
| YBC_gaiaDR2 | Gaia's DR2 G, G_BP and G_RP (Vegamags, Gaia passbands from Evans et al. 2018) |
| YBC_gaiaDR2maiz | Gaia's DR2 G, G_BP and G_RP (Vegamags, Gaia passbands from Maiz-Apellaniz and Weiler 2018) |
| YBC_gaiaDR2weiler | Gaia's DR2 G, G_BP and G_RP (Vegamags, Gaia passbands from Weiler 2018) |
| YBC_UVbright | HST+GALEX+Swift/UVOT UV filters |
| YBC_acs_hrc | HST/ACS HRC |
| YBC_acs_wfc_pos04jul06 | HST/ACS WFC (c.f. 2007 revision, pos-04jul06) |
| YBC_acs_wfc_202101 | HST/ACS WFC - updated filters and zeropoints, 2021 |
| YBC_nicmosab | HST/NICMOS AB |
| YBC_nicmosvega | HST/NICMOS Vega |
| YBC_stis | HST/STIS imaging mode, Vegamag |
| YBC_wfc3_wideverywide | HST/WFC3 all W+LP+X filters (UVIS1+IR, final throughputs) |
| YBC_wfc3_202101_verywide | HST/WFC3 long-pass and extremely wide filters (UVIS) - updated filters and zeropoints, 2021 |
| YBC_wfc3_202101_medium | HST/WFC3 medium filters (UVIS+IR) - updated filters and zeropoints, 2021 |
| YBC_wfc3_202101_wide | HST/WFC3 wide filters (UVIS+IR) - updated filters and zeropoints, 2021 |
| YBC_wfpc2 | HST/WFPC2 (Vegamag, cf. Holtzman et al. 1995) |
| YBC_hipparcos | Hipparcos+Tycho+Gaia DR1 (Vegamags) |
| YBC_int_wfc | INT/WFC (Vegamag) |
| YBC_iphas | IPHAS |
| YBC_jwst_miri_wide | JWST MIRI wide filters, Vegamags |
| YBC_jwst_nircam_wide | JWST NIRCam wide+verywide filters, Vegamags |
| jwst_nircam_widemedium_nov22 | JWST NIRCam wide+verywide+medium filters (Nov 2022), Vegamags |
| YBC_jwst_nircam_widemedium | JWST NIRCam wide+verywide+medium filters, Vegamags |
| jwst_niriss_nov22 | JWST NIRISS filters (Nov 2022), Vegamags |
| YBC_jwst_nirspec | JWST Nirspec filters, Vegamags |
| YBC_kepler | Kepler + SDSS griz + DDO51 (in ABmags) |
| YBC_kepler_2mass | Kepler + SDSS griz + DDO51 (in ABmags) + 2MASS (~Vegamag) |
| YBC_vst_vista | KiDS/VIKING (VST/OMEGAM + VISTA/VIRCAM, all ABmags) |
| YBC_lbt_lbc | LBT/LBC (Vegamag) |
| YBC_lsst_wfirst_proposed2017 | LSST (ABmags) + WFIRST proposed filters (Vegamags) |
| YBC_lsst | LSST ugrizY, March 2012 total filter throughputs (all ABmags) |
| lsstDP0 | LSST ugrizy, Oct 2017 total filter throughputs for DP0 (all ABmags) |
| lsstR1.9 | LSST ugrizy, Sept 2023, total filter throughputs R1.9 (all ABmags) |
| YBC_noao_ctio_mosaic2 | NOAO/CTIO/MOSAIC2 (Vegamag) |
| YBC_ogle | OGLE-II |
| YBC_panstarrs1 | Pan-STARRS1 |
| Roman2021 | Roman (ex-WFIRST) 2021 filters, Vegamags |
| YBC_splus | S-PLUS (Vegamags), revised on Nov. 2017 |
| YBC_sloan | SDSS ugriz |
| YBC_sloan_2mass | SDSS ugriz + 2MASS JHKs |
| YBC_sloan_ukidss | SDSS ugriz + UKIDSS ZYJHK |
| YBC_swift_uvot | SWIFT/UVOT UVW2, UVM2, UVW1,u (Vegamag) |
| YBC_skymapper | SkyMapper (ABmags) |
| YBC_spitzer | Spitzer IRAC+MIPS |
| YBC_stroemgren | Stroemgren-Crawford |
| YBC_hsc | Subaru/Hyper Suprime-Cam (ABmags) |
| YBC_suprimecam | Subaru/Suprime-Cam (ABmags) |
| SuperBIT | SuperBIT, all ABmags |
| YBC_TESS_2mass | TESS + 2MASS (Vegamags) |
| YBC_TESS_2mass_kepler | TESS + 2MASS (Vegamags) + Kepler + SDSS griz + DDO51 (in ABmags) |
| YBC_ukidss | UKIDSS ZYJHK (Vegamag) |
| YBC_uvit | UVIT (all ABmags) |
| YBC_visir | VISIR |
| YBC_vista | VISTA ZYJHKs (Vegamag) |
| YBC_vphas | VPHAS+ (ABmags) |
| YBC_vst_omegacam | VST/OMEGACAM (ABmag) |
| YBC_vilnius | Vilnius |
| YBC_wfc3_uvisCaHK | WFC3/UVIS around CaHK |
| YBC_washington_ddo51 | Washington CMT1T2 + DDO51 |
| YBC_ztf | ZTF (ABmags) |
| YBC_deltaa | deltaa (Paunzen) + UBV (Maiz-Apellaniz), in Vegamags |


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


