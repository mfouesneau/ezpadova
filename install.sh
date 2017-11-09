#!/usr/bin/env bash
rm -rf ./build
python setup.py build_ext --inplace
python setup.py install
