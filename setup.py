#! /usr/bin/env python
"""!
-----------------------------------------------------------------------------
File Name : setup.py

Purpose: python package setup script for partyCoin backend

Created: 05-Mar-2015 20:52:42 AEDT
-----------------------------------------------------------------------------
Revision History

Thu Mar  5 20:53:27 AEDT 2015: Version 1.0
First Release

-----------------------------------------------------------------------------
S.D.G
"""
__author__ = 'Ben Johnston'
__revision__ = '1.0'
__date__ = '05-Mar-2015 20:52:42 AEDT'
__license__ = 'MPL v2.0'

## LICENSE DETAILS############################################################
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

##IMPORTS#####################################################################
from distutils.core import setup
##############################################################################
setup(
    name='partycoin',
    description='Get Australian political party funding information',
    url='www.partycoin.org',
    author='Ben Johnston',
    author_email='',
    version=__revision__,
    packages=['partycoin'],
    license=open('LICENSE.txt').read(),
    long_description=open('README.md').read())
