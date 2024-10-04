.. ezpadova documentation master file
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

EZPADOVA -- A python package that allows you to download PADOVA isochrones directly from their website
======================================================================================================

.. image:: https://img.shields.io/badge/Parsec_CMD-3.8-green.svg
  :target: http://stev.oapd.inaf.it/cgi-bin/cmd_3.8

.. image:: https://img.shields.io/badge/python-3.9,_3.10,_3.11,_3.12-blue.svg
    :target: https://www.python.org/

This small package provides a direct interface to the PADOVA/PARSEC isochrone webpage (http://stev.oapd.inaf.it/cgi-bin/cmd).
It compiles the URL needed to query the website and retrives the data into a python variable.

This package has been tested on python 3.9, 3.10, 3.11, 3.12 through the github actions CI.

New in version 2.0
------------------
* Updated the interface to the new PADOVA website (i.e. >=3.8) [minor changes in the form format from 3.7]
* New function `get_isochrone` does all the slices directly (combines `get_Z_isochrones`, `get_t_isochrones`, and `get_one_isochrone` which are now deprecated.)
* `get_isochrone` handles ages, log ages, Z and [M/H] as inputs (see documentation).
* Most of the code has been rewritten to be more robust and easier to maintain. In particular the parsing of the online form has been improved.
* Many integration tests to keep checking the package interface.
* The output format is now a `pandas.DataFrame` instead of the internal format. (though previous aliases of columns are no more available)
* added `resample_evolution_phase` function to resample the `label` into a continuous evolution phase instead of discrete labels.
* Documentation has been updated and (hopefully) improved. -- more in progress

Available photometric systems, parameters, and default values: :ref:`parsec parameters`

TODOs
-----

* [ ] create and merge PR
* [ ] make a release package


Installation
------------

* Using pip: Use the `--user` option if you don't have permissions to install libraries

.. code-block:: none

        pip install git+https://github.com/mfouesneau/ezpadova

* Manually:

.. code-block:: none

        git clone https://github.com/mfouesneau/ezpadova
        cd ezpadova
        python setup.py intall


Example usage (deprecated)
--------------------------

.. deprecated:: 2.0
    The following examples are deprecated and will be removed in the next version. Please use the new interface :func:`ezpadova.parsec.get_isochrones` instead.

* Basic example of downloading a sequence of isochrones, plotting, saving

.. code-block:: python

    from ezpadova import get_t_isochrones
    r = parsec.get_t_isochrones(6.0, 7.0, 0.05, 0.02)

    import pylab as plt
    plt.scatter(r['logT'], r['logL'], c=r['logA'], edgecolor='None')
    plt.show()

* getting only one isochrone

.. code-block:: python

    from ezpadova import get_one_isochrone
    r = parsec.get_one_isochrone(1e7, 0.02, model='parsec12s', phot='spitzer')


Contents
---------

.. toctree::
   :maxdepth: 2

   query_parameters
   API <ezpadova>

