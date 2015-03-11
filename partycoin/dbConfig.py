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
from stdtoolbox.logging import logger
import MySQLdb as mdb
##############################################################################
HOST = 'localhost'
USER = 'partyCoin'
PWORD = 'money'
DBASE = 'donations'

#CLASSES#######################################################################


class partyCoinDbase(object):
    """!
    This class forms the base class for connecting to the partyCoin database
    and executing commands
    """
    def __init__(self, debug_level=0):
        """!
        The constructor for the object
        @param self The pointer for the object
        """
        self.info_logger = logger('info.log', debug_level=debug_level)
        self.connect_to_db()

    def connect_to_db(self):
        """!
        This method connects to the mysql database using the parameters
        specified within dbConfig.py
        @param self The pointer for the object
        """
        self.con = mdb.connect(HOST, USER, PWORD, DBASE)
        self.cur = self.con.cursor()

    def execute_command(self, command):
        """!
        This method is used to execute sql commands and appropriately handling
        logging of debug messages
        """
        self.info_logger.info('to db: %s' % command)
        self.cur.execute(command)
        self.con.commit()

    def disconnect(self):
        """!
        This method disconnects the sql database connection
        @param self The pointer for the object
        """
        self.con.close()
