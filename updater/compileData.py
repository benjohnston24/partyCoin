#! /usr/bin/env python
"""!
-----------------------------------------------------------------------------
File Name : compileData.py

Purpose: This module takes the csv files obtained from dataGetter.py and
adds the information to the database using updateDatabase.py

Created: 25-Feb-2015 23:31:30 AEDT
-----------------------------------------------------------------------------
Revision History



-----------------------------------------------------------------------------
S.D.G
"""
__author__ = 'Ben Johnston'
__revision__ = '0.1'
__date__ = '25-Feb-2015 23:31:30 AEDT'
__license__ = 'MPL v2.0'

## LICENSE DETAILS############################################################
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

##IMPORTS#####################################################################
from dataGetter import dataGetter, RAW_DATA
from updateDatabase import updateDatabase
import os
import argparse
import sys
import re
import pdb
##############################################################################

CSV = '.csv'
#regular expression search strings
#the first string searches for the acronym of the state without any alphabet
#characters on either side
STATES = {'nsw': '([^A-Za-z]nsw([^A-Za-z]|$))|'
                 #'([^A-Za-z]nsw)|'
                 '([^A-Za-z]n[\.,\-]s[\.,\-]w[^A-Za-z])|'
                 '(new south wales)',
          'qld': '([^A-Za-z]qld([^A-Za-z]|$))|'
                 #'([^A-Za-z]qld)|'
                 '(^A-Za-z]q[\.,\-]l[\.,\-]d[^A-Za-z])|'
                 '(queensland)',
          'vic': '([^A-Za-z]vic([^A-Za-z]|$))|'
                 #'([^A-Za-z]vic)|'
                 '([^A-Za-z]v[\.,\-]i[\.,\-]c[^A-Za-z])|'
                 '(victoria)',
          'sa': '([^A-Za-z]sa([^A-Za-z]|$))|'
                 #'([^A-Za-z]sa)|'
                '([^A-Za-z]s[\.,\-]a[^A-Za-z])|'
                '(south australia)',
          'nt': '([^A-Za-z]nt([^A-Za-z]|$))|'
                 #'([^A-Za-z]nt)|'
                '([^A-Za-z]n[\.,\-]t[^A-Za-z])|'
                 '(northern territory)',
          'wa': '([^A-Za-z]wa([^A-Za-z]|$))|'
                 #'([^A-Za-z]wa)|'
                '([^A-Za-z]w[\.,\-]a[^A-Za-z])|'
                '(western australia)',
          'act': '([^A-Za-z]act([^A-Za-z]|$))|'
                 #'([^A-Za-z]act)|'
                 '([^A-Za-z]a[\.,\-]c[\.,\-]t[^A-Za-z])|'
                 '(australian captial territory)',
          'tas': '([^A-Za-z]tas([^A-Za-z]|$))|'
                 #'([^A-Za-z]tas)|'
                 '([^A-Za-z]t[\.,\-]a[\.,\-]s[^A-Za-z])|'
                 '(tasmania)',
          }

FEDERAL = 'FED'

if __name__ == "__main__":
    #Command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', action='store_true',
                        default=False, help="Enable debug mode")
    parser.add_argument('-l', '--log', action='store_true',
                        default=False, help="Enable debug logging")
    args = parser.parse_args()

    #Modify debug level as per user input
    debug_level = 0
    if args.debug:
        debug_level = 1
    if args.log:
        debug_level = 2

    #Get the data
    if False:
        try:
            dataGetter(debug_level=debug_level).launch_funds_getter()
        except:
            print "Unable to get new funds from website"
            sys.exit()

    #Try connecting to the database
    try:
        db = updateDatabase(debug_level=debug_level)
    except:
        print "Unable to connect to database"

    #Walk through the collected file list
    working_dir = os.path.join(os.getcwd(), RAW_DATA)
    file_list = os.listdir(working_dir)
    counter = 0
    for f in file_list:
        #If the file is a csv file
        if os.path.splitext(f)[1] == CSV:
            counter += 1
            #print "Reading file %s" % f
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
                    #print year
                #The second row contains the name
                elif (row_counter == 1):
                    party = row.split(',')[0]
                    party_state = None
                    #find the state
                    #if party.find('Consandine') >=0:
                    #    pdb.set_trace()
                    test_party = party.lower().replace('.', '')
                    for state in STATES.keys():
                        #print STATES[state]
                        if re.search(STATES[state], test_party):
                            party_state = state
                            break
                        #if test_party.find(value) > 0:
                            #    party_state = state
                        if party_state is not None:
                            break
                    if party_state is None:
                        party_state = FEDERAL
                    print '%s\t%s\t\t:%s' % (party, test_party, party_state)
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
                    db.add_funds_to_db(year=year,
                                       party=party,
                                       party_state=party_state,
                                       donor=extracted_data[0],
                                       address=extracted_data[1],
                                       state=extracted_data[3],
                                       postcode=extracted_data[4],
                                       don_type=extracted_data[6],
                                       amount=float(extracted_data[5]))
                row_counter += 1
    db.replace_old_data()
    print 'Files read: %s' % counter
