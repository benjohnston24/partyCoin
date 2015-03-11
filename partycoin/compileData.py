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
from updateDonations import updateDonations
from updatePartyInfo import updatePartyInfo
import argparse
import sys
import os
##############################################################################


def main(import_data_only=False, debug_level=0,
         sync_only=False,
         log_folder=RAW_DATA, file_extension=FILE_EXT):
    """!
    This method executes the program.  The instructions have been encapsulated
    in a method to allow for calling from the command line
    @param import_data_only A boolean flag to indicate if the data is only to
    be imported from data files into the data base
    @param sync_only A boolean flag used to indicate if the donations database
    is only to be synchronised with the party info database
    @param debug_level A flag to indicate the debug level for the method.  0
    indicates debugging is disabled, 1 indicates messages displayed through
    stdout, 2 indicates debug messages are logged to info.log
    @param log_folder The folder used to store the raw data files
    @param file_extension The file extension of the files containing the data
    """

    if (not import_data_only) and (not sync_only):
        #Get the data
        try:
            dataGetter(debug_level=debug_level).launch_funds_getter()
        except:
            print "Unable to get new funds from website"
            sys.exit()

    #Update the database
    if not sync_only:
        #Try connecting to the database
        try:
            db = updateDonations(debug_level=debug_level)
        except:
            print "Unable to connect to database"
            sys.exit()

        #Import Data
        try:
            db.prepare_for_new_data()
            db.import_data_from_dir(log_folder=os.path.join(os.getcwd(),
                                                            log_folder),
                                    file_extension=FILE_EXT)
            db.disconnect()
        except:
            print "Unable to import data to database"
            sys.exit()

    #Sync the partyinfo database to the donations database
    try:
        partyInfo = updatePartyInfo(debug_level=debug_level)
        partyInfo.sync_with_funds()
        #partyInfo.update_images()

    except:
        print "Unable to sync database"
        sys.exit()


if __name__ == "__main__":
    #Command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', action='store_true',
                        default=False, help="Enable debug mode")
    parser.add_argument('-l', '--log', action='store_true',
                        default=False, help="Enable debug logging")
    parser.add_argument('-i', '--import_data', action='store_true',
                        default=False, help="Import local data only")
    parser.add_argument('-s', '--sync', action='store_true',
                        default=False, help="Sync databases only")
    args = parser.parse_args()

    #Modify debug level as per user input
    debug_level = 0
    if args.debug:
        debug_level = 1
    if args.log:
        debug_level = 2

    main(import_data_only=args.import_data,
         sync_only=args.sync,
         debug_level=debug_level,
         log_folder=RAW_DATA,
         file_extension=FILE_EXT)
