#! /usr/bin/env python
"""!
-----------------------------------------------------------------------------
File Name : updatePartyInfo.py

Purpose: This python module is scan the information added to the donations
database through updateDatabase.py and collate a list of all the unique
political parties, storing the result in a separate table.

Created: 11-Mar-2015 14:04:58 AEDT
-----------------------------------------------------------------------------
Revision History



-----------------------------------------------------------------------------
S.D.G
"""
__author__ = 'Ben Johnston'
__revision__ = '0.1'
__date__ = '11-Mar-2015 14:04:58 AEDT'
__license__ = 'MPL v2.0'

## LICENSE DETAILS############################################################
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

##IMPORTS#####################################################################
from dbConfig import partyCoinDbase
from updateDonations import MAIN_TABLE as DONATIONS_TABLE
import wikipedia
import re
import pdb
##############################################################################
#This table contains the information for each of the political parties
INFO_TABLE = 'funds_tracker_partyinfo'
WIKI_PARTY_LIST = 'List of registered political parties in Australia'

#CLASSES#######################################################################


class updatePartyInfo(partyCoinDbase):
    """!
    This class is used to update the party information table.  The party
    information table contains details such as web addresses of party icons and
    party website addresses etc.
    """
    def __init__(self, debug_level=0):
        """!
        The constructor for the object
        @param self The pointer for the object
        """
        #Instantiate the parent class
        partyCoinDbase.__init__(self, debug_level=debug_level)
        self.connect_to_db()

    def sync_with_funds(self):
        """!
        This method lists all of the party names within the donations table of
        the party coin database and checks they are present within the party
        information table
        @param self The pointer for the object
        """
        #Get a list of the parties in the donations database
        self.execute_command('SELECT DISTINCT party FROM %s' % DONATIONS_TABLE)
        donation_parties = self.cur.fetchall()
        #Clean up list
        donation_parties_clean = self.__clean_list(donation_parties)

        #Get a list of the parties in the party info table
        self.execute_command('SELECT DISTINCT party FROM %s' % INFO_TABLE)
        info_parties = self.cur.fetchall()
        #Clean up list
        info_parties_clean = self.__clean_list(info_parties)
        #Check the donation parties are in the party info table
        for party in donation_parties_clean:
            if not (party in info_parties_clean):
                self.execute_command("INSERT INTO %s (party) VALUES ('%s')" %
                                     (INFO_TABLE, party))

    def update_common_images(self):
        """!
        This method updates the image links within the party information table
        @param self The pointer for the object
        @todo Finish this
        """
        #Get the parties in the info party table
        self.execute_command('SELECT * FROM %s' % INFO_TABLE)
        info_parties = self.cur.fetchall()
        #Clean up list
        for party in info_parties:
            logo = ''
            wiki = ''
            if (party[1].find('Australian Democrats') >= 0):
                logo = 'https://images.duckduckgo.com/iu/?u=http%3A%2F%2F'\
                       'www.thewire.org.au%2FStoryImages%2Fausdems.png&f=1'
                wiki = 'https://en.wikipedia.org/wiki/Australian_Democrats'
            elif (party[1].find('Greens') >= 0):
                logo = 'https://upload.wikimedia.org/wikipedia/commons/thum'\
                       'b/1/12/AustralianGreensLogo.svg/1200px-AustralianG'\
                       'reensLogo.svg.png'
                wiki = 'https://en.wikipedia.org/wiki/Australian_Greens'
            elif (party[1].find('Australian Labor Party') >= 0):
                logo = 'https://upload.wikimedia.org/wikipedia/en/thumb/7'\
                       '/7b/Australian_Labor_Party_logo.svg/1200px-Austr'\
                       'alian_Labor_Party_logo.svg.png'
                wiki = 'https://en.wikipedia.org/wiki/Australian_Labor_Party'
            elif (party[1].find('Christian Democratic') >= 0):
                logo = 'https://upload.wikimedia.org/wikipedia/en/7/74/'\
                       'CDPbanner.jpg'
                wiki = 'https://en.wikipedia.org/wiki/Christian_Democr'\
                       'atic_Party_%28Australia%29'
            elif (party[1].find('Liberal Party') >= 0):
                logo = 'https://upload.wikimedia.org/wikipedia/en/3/38/'\
                       'Liberal_Party_of_Australia_logo.png'
                wiki = 'https://en.wikipedia.org/wiki/Liberal_Party_of_'\
                       'Australia'
            elif (party[1].find('National Party') >= 0):
                logo = 'https://upload.wikimedia.org/wikipedia/commons/'\
                       '4/4d/Nationals_FRA_stacke_9013DF.jpg'
                wiki = 'https://en.wikipedia.org/wiki/National_Party_of'\
                       '_Australia'
            elif (party[1].find('One Nation') >= 0):
                logo = 'https://upload.wikimedia.org/wikipedia/en/c/c0/'\
                       'Onenationlogo.jpg'
                wiki = 'https://en.wikipedia.org/wiki/One_Nation_%28'\
                       'Australia%29'

            if((logo != '') and (wiki != '')):
                self.execute_command("UPDATE %s SET logo='%s', wiki_page='%s'"
                                     "WHERE party='%s'" %
                                     (INFO_TABLE, logo, wiki, party[1]))

    def __clean_list(self, dirty_list):
        """!
        This method takes a list of tuples and returns a list containing only
        the 0th element of the tuple
        @param self The pointer for the object
        @param dirty_list The list of tuples to be cleaned
        """
        clean_list = []
        for i in range(len(dirty_list)):
            clean_list.append(dirty_list[i][0])
        return clean_list
