#! /usr/bin/env python
"""!
-----------------------------------------------------------------------------
File Name : compileData.py

Purpose: This module takes the csv files obtained from dataGetter.py and
adds the information to the database using updateDatabase.py

Updated: Thu Mar  5 19:23:38 AEDT 2015
Created: 25-Feb-2015 23:31:30 AEDT
-----------------------------------------------------------------------------
Revision History

Thu Mar  5 19:25:00 AEDT 2015: Version 0.1
*First Draft


-----------------------------------------------------------------------------
S.D.G
"""
__author__ = 'Ben Johnston'
__revision__ = '0.1'
__date__ = 'Thu Mar  5 19:23:20 AEDT 2015'
__license__ = 'MPL v2.0'

## LICENSE DETAILS############################################################
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

##IMPORTS#####################################################################
from dataGetter import dataGetter, RAW_DATA, FILE_EXT
from updateDatabase import updateDatabase
import argparse
import sys
##############################################################################

if __name__ == "__main__":
    #Command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', action='store_true',
                        default=False, help="Enable debug mode")
    parser.add_argument('-l', '--log', action='store_true',
                        default=False, help="Enable debug logging")
    parser.add_argument('-i', '--input_data', action='store_true',
                        default=False, help="Import local data only")
    args = parser.parse_args()

    #Modify debug level as per user input
    debug_level = 0
    if args.debug:
        debug_level = 1
    if args.log:
        debug_level = 2

    if not args.input_data:

        #Get the data
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
        sys.exit()

    #Import the data from the log files
    try:
        db.import_data_from_dir(log_folder=RAW_DATA,
                                file_extension=FILE_EXT)
    except:
        print "Unable to import data to database"
        sys.exit()
