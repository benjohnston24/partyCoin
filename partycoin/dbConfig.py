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

#regular expression search strings
#the first string searches for the acronym of the state without any alphabet
#characters on either side
#STATES is used to to determine in which state a given political party resides
STATES = {'nsw': '([^A-Za-z]nsw([^A-Za-z]|$))|'
                 '([^A-Za-z]n[\.,\-]s[\.,\-]w[^A-Za-z])|'
                 '(new south wales)',
          'qld': '([^A-Za-z]qld([^A-Za-z]|$))|'
                 '(^A-Za-z]q[\.,\-]l[\.,\-]d[^A-Za-z])|'
                 '(queensland)',
          'vic': '([^A-Za-z]vic([^A-Za-z]|$))|'
                 '([^A-Za-z]v[\.,\-]i[\.,\-]c[^A-Za-z])|'
                 '(victoria)',
          'sa': '([^A-Za-z]sa([^A-Za-z]|$))|'
                '([^A-Za-z]s[\.,\-]a[^A-Za-z])|'
                '(south australia)',
          'nt': '([^A-Za-z]nt([^A-Za-z]|$))|'
                '([^A-Za-z]n[\.,\-]t[^A-Za-z])|'
                 '(northern territory)',
          'wa': '([^A-Za-z]wa([^A-Za-z]|$))|'
                '([^A-Za-z]w[\.,\-]a[^A-Za-z])|'
                '(western australia)',
          'act': '([^A-Za-z]act([^A-Za-z]|$))|'
                 '([^A-Za-z]a[\.,\-]c[\.,\-]t[^A-Za-z])|'
                 '(australian captial territory)',
          'tas': '([^A-Za-z]tas([^A-Za-z]|$))|'
                 '([^A-Za-z]t[\.,\-]a[\.,\-]s[^A-Za-z])|'
                 '(tasmania)',
          }

#FEDERAL is used to indicate that a political party is a country wide
#organisation
FEDERAL = 'FED'


