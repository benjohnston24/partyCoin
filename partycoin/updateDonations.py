#! /usr/bin/env python
"""!
-----------------------------------------------------------------------------
File Name : updateDonations.py

Purpose: This module is used to read the data downloaded from the Australian
electoral commission website and update the database accordingly

Updated: Thu Mar  5 19:25:41 AEDT 2015
Created: 24-Feb-2015 21:32:45 AEDT
-----------------------------------------------------------------------------
Revision History

Wed Mar 11 15:36:29 AEDT 2015: Version 0.2
*File renamed
*updateDonations class re-configured to inherit partyCoinDbase class

24-Feb-2015 21:32:45 AEDT: Version 0.1
*Configured to work with sql database only


-----------------------------------------------------------------------------
S.D.G
"""
__author__ = 'Ben Johnston'
__revision__ = '0.2'
__date__ = 'Wed Mar 11 15:36:17 AEDT 2015'
__license__ = 'MPL v2.0'

## LICENSE DETAILS############################################################
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

##IMPORTS#####################################################################
from dbConfig import partyCoinDbase
import re
import os
import pdb
##############################################################################
#Tables used in tracking the donations made by the political parties
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
                 '([^A-Za-z]v[\.,\-]i[\.,\-]c[^A-Za-z])|' '(victoria)',
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

#CLASSES#######################################################################


class updateDonations(partyCoinDbase):
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
        #Instantiate the parent class
        partyCoinDbase.__init__(self, debug_level=debug_level)
        self.connect_to_db()

    def prepare_for_new_data(self):
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
                        party_state=None,
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
                or (party is None) or (year is None) or (party_state is None):
                return False
        #Check inputs
        year = year.replace("'", '')
        party = party.replace("'", '')
        donor = donor.replace("'", '')
        address = address.replace("'", '')
        don_type = don_type.replace("'", '')
        state = state.replace("'", '')
        party_state = party_state.replace("'", '')
        msg = 'INSERT INTO %s(year, party,'\
              'donor, address, state, postCode, donor_type, amount, '\
              'party_state)'\
              " VALUES('%s', '%s','%s','%s', '%s', '%s', '%s', %0.2f, '%s')" %\
              (SECONDARY_TABLE, year, party, donor, address, state,
               postcode, don_type, amount, party_state.upper())
        self.execute_command(msg)

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

    def import_data_from_dir(self, log_folder=None, file_extension=None):
        """!
        This method is used to import data from log files into the database
        @param self The pointer for the object
        @param log_folder The folder containing the log files to import
        @param file_extension The file type to be imported
        """
        #Check the inputs are valid
        if (log_folder is None) or (file_extension is None):
            msg = 'log_folder and/or file_extension not supplied'
            self.info_logger.info(msg)
            return
        #Walk through the collected file list
        working_dir = log_folder
        file_list = os.listdir(working_dir)
        counter = 0
        for f in file_list:
            #If the file is a csv file
            if os.path.splitext(f)[1] == file_extension:
                counter += 1
                self.info_logger.info("Reading file %s" % f)
                row_counter = 0
                f_handle = open(os.path.join(working_dir, f), 'r')
                data = f_handle.read().split(',\r\n')
                #Process the data based on the row
                for row in data:
                    #Ensure the file acutally contains data
                    if len(data) == 1:
                        break
                    #The first row contains the year
                    if (row_counter == 0):
                        year = row.split(' ')
                        year = year[len(year) - 1][:4]
                    #The second row contains the name
                    elif (row_counter == 1):
                        party = row.split('data')[0].replace(',', '')
                        #party = row.split(',')[0]
                        party_state = None
                        #find the state
                        test_party = party.lower().\
                            replace('.', '').\
                            replace(',', '')

                        for state in STATES.keys():
                            #Check which state the party is from
                            if re.search(STATES[state], test_party):
                                party_state = state
                                break
                            #If a state has been allocated, break the loop
                            if party_state is not None:
                                break
                        #If a state has not been allocated default to FEDERAL
                        #level
                        if party_state is None:
                            party_state = FEDERAL

                    #Ignore the third row
                    elif(row_counter == 2):
                        pass
                    #Handle data rows except for last blank lines
                    elif (row != ''):
                        extracted_data = row.split('","')
                        #Remove existing quotation marks
                        for i in range(len(extracted_data)):
                            extracted_data[i] = \
                                extracted_data[i].replace('"', '').\
                                replace("'", '')

                        self.add_funds_to_db(year=year,
                                             party=party,
                                             party_state=party_state,
                                             donor=extracted_data[0],
                                             address=extracted_data[1],
                                             state=extracted_data[3],
                                             postcode=extracted_data[4],
                                             don_type=extracted_data[6],
                                             amount=float(extracted_data[5]))
                    row_counter += 1
        self.replace_old_data()
