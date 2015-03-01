#! /usr/bin/env python
"""!
-----------------------------------------------------------------------------
File Name : dbConfig.py

Purpose: Specifies the configuration paramters for the Mysql database to be
used within updateDatabase.py

Created: 24-Feb-2015 21:52:17 AEDT
-----------------------------------------------------------------------------
Revision History



-----------------------------------------------------------------------------
S.D.G
"""
__author__ = 'Ben Johnston'
__revision__ = '0.1'
__date__ = '24-Feb-2015 21:52:17 AEDT'
__license__ = 'MPL v2.0'

## LICENSE DETAILS############################################################
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

##IMPORTS#####################################################################

##############################################################################
HOST = 'localhost'
USER = 'partyCoin'
PWORD = 'money'
DBASE = 'donations'
MAIN_TABLE = 'funds_tracker_donation'
SECONDARY_TABLE = 'new_funds'
