#! /usr/bin/env python
"""!
-----------------------------------------------------------------------------
File Name : updateDatabase.py

Purpose: This module is used to read the data downloaded from the Australian
electoral commission website and update the database accordingly

Created: 24-Feb-2015 21:32:45 AEDT
-----------------------------------------------------------------------------
Revision History

24-Feb-2015 21:32:45 AEDT: Version 0.1

*Configured to work with Mysql database only


-----------------------------------------------------------------------------
S.D.G
"""
__author__ = 'Ben Johnston'
__revision__ = '0.1'
__date__ = '24-Feb-2015 21:32:45 AEDT'
__license__ = 'MPL v2.0'

## LICENSE DETAILS############################################################
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

##IMPORTS#####################################################################
from dbConfig import HOST, USER, PWORD, DBASE, MAIN_TABLE, SECONDARY_TABLE
from stdtoolbox.logging import logger
import MySQLdb as mdb
##############################################################################


class updateDatabase(object):
    """!
    This class is used to update the mysql database containing the political
    funding information. The class possesses methods that enable reading of the
    data supplied by dataGetter.py
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
        #Drop the secondary table if it exists
        try:
            self.execute_command('DROP TABLE %s' % SECONDARY_TABLE)
        except Exception as e:
            if e[1].find('Unknown table') >= 0:
                pass
            else:
                raise(e)
        #Create a new blank instances of the secondary table
        msg = 'CREATE TABLE %s LIKE %s' % (
              SECONDARY_TABLE, MAIN_TABLE)
        self.execute_command(msg)

    def add_funds_to_db(self,
                        year=None,
                        party=None,
                        donor=None,
                        address=None,
                        state=None,
                        postcode=None,
                        don_type=None,
                        amount=None):
        """!
        This method adds donation information to the database
        """
        if (donor is None) or (address is None) or (state is None) or\
            (postcode is None) or (don_type is None) or (amount is None)\
                or (party is None) or (year is None):
                return False
        #Check inputs
        year = year.replace("'", '')
        party = party.replace("'", '')
        donor = donor.replace("'", '')
        address = address.replace("'", '')
        don_type = don_type.replace("'", '')
        state = state.replace("'", '')
        msg = 'INSERT INTO %s(year, party,'\
              'donor, address, state, postCode, donor_type, amount)'\
              " VALUES('%s', '%s','%s','%s', '%s', '%s', '%s', %0.2f)" %\
              (SECONDARY_TABLE, year, party, donor, address, state,
               postcode, don_type, amount)
        #try:
        self.execute_command(msg)
        #except:
        #    pdb.set_trace()

    def replace_old_data(self):
        """!
        This method replaces the old data in the database with the recently
        collected
        """
        try:
            self.execute_command('DROP TABLE %s' % MAIN_TABLE)
        except Exception as e:
            if e[1].find('Unknown table') >= 0:
                pass
            else:
                raise(e)
        self.execute_command('ALTER TABLE %s RENAME %s' % (SECONDARY_TABLE,
                                                           MAIN_TABLE))

    def execute_command(self, command):
        """!
        This method is used to execute sql commands and appropriately handling
        logging of debug messages
        """
        self.info_logger.info('to db: %s' % command)
        self.cur.execute(command)
        self.con.commit()
