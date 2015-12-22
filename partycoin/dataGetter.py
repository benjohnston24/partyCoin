#! /usr/bin/env python
"""!
-----------------------------------------------------------------------------
File Name : dataGetter.py

Purpose: This python module downloads the political party funding information
available at the AEC website

Updated: Thu Mar  5 19:26:17 AEDT 2015
Created: 21-Feb-2015 08:31:36 AEDT
-----------------------------------------------------------------------------
Revision History

Thu Mar  5 19:26:17 AEDT 2015: Version 1.0
First Release

-----------------------------------------------------------------------------
S.D.G
"""
__author__ = 'Ben Johnston'
__revision__ = '1.0'
__date__ = 'Thu Mar  5 19:27:26 AEDT 2015'
__license__ = 'MPL v2.0'

# LICENSE DETAILS############################################################
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# IMPORTS#####################################################################
import mechanize
import cookielib
from BeautifulSoup import BeautifulSoup
from stdtoolbox.logging import logger
import httplib
import re
import os
##############################################################################

# Web addresses to be used
main_address = "http://periodicdisclosures.aec.gov.au/"
locator_service = main_address + "Default.aspx"
party_analysis_address = main_address + "AnalysisParty.aspx"
__aec__ = "http://www.aec.gov.au"

# Raw data location
RAW_DATA = 'dat'
# Log file extension
FILE_EXT = '.csv'


class dataGetter(object):

    """!
    This class is used to download political funding data from the australian
    electoral commission website.

    """

    def __init__(self, debug_level=1):
        """!
        The constructor for the object
        @param self The pointer for the object
        @param debug_level The selected debug level for the object
        A debug level of 0 disables debug messages
        A debug level of 1 prints debug messages to stdout only
        A debug level of 2 prints debug messages to stdout and logs them to
        dataGetter.log
        *Note: mechanize browser messages are not logged to dataGetter.log.  If
        these are required use output redirection when calling the python
        script.
        """
        # Logging device
        self.debug_level = debug_level
        self.info_logger = logger(file_name="dataGetter.log",
                                  debug_level=debug_level)
        # Browser
        self.info_logger.info('Construct Browser Object')

        # Use HTTP version 1.0, required to download file
        httplib.HTTPConnection._http_vsn = 10
        httplib.HTTPConnection._http_vsn_str = 'HTTP/1.0'

        self.br = mechanize.Browser()

        # Cookie Jar
        self.cj = cookielib.LWPCookieJar()
        self.br.set_cookiejar(self.cj)

        # Browser options
        self.br.set_handle_equiv(True)
        # self.br.set_handle_gzip(True)
        self.br.set_handle_redirect(True)
        self.br.set_handle_referer(True)
        self.br.set_handle_robots(False)

        # Follows refresh 0 but not hangs on refresh > 0
        self.br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(),
                                   max_time=1)

        # Want debugging messages?
        if debug_level >= 2:
            self.br.set_debug_http(True)
            self.br.set_debug_redirects(True)
            self.br.set_debug_responses(True)

        # User-Agent (this is cheating, ok?)
        self.br.addheaders = [('User-agent',
                               'Mozilla/5.0'
                               '(X11; U; Linux i686; en-US;rv:1.9.0.1)'
                               'Gecko/2008071615 Ubuntu/14.04.2'
                               'Firefox/3.0.1')]

        # Available years of data
        self.available_years = []

        # Check the directory to log folders exists

    def launch_funds_getter(self, log_folder=RAW_DATA):
        """!
        This method is used to extract the data from the australian electorocal
        commision website for all parties for all available years.
        @param self The pointer for the object
        """
        log_folder_path = os.path.join(os.getcwd(), log_folder)
        if not os.path.exists(log_folder_path):
            os.makedirs(log_folder_path)
            self.info_logger.info('Created directory %s' % log_folder_path)
        self.get_available_years()
        for year_list in self.available_years:
            self.info_logger.info('Select data for year: %s' % year_list[0])
            # Access the main site
            self.br.open(locator_service)
            # Select the export form
            self.br.select_form(predicate=lambda f:
                                f.attrs.get('id', None) == 'formMaster')
            # Select the year
            self.br["ctl00$dropDownListPeriod"] = [year_list[1]]
            # Click the Go button
            req = self.br.click(type="submit",
                                name="ctl00$buttonGo")
            self.br.open(req)
            # Get party list for that year
            self.get_party_list()

            for party in self.party_list:

                # Access the main site
                self.br.open(party_analysis_address)
                # Select the export form
                self.br.select_form(predicate=lambda f:
                                    f.attrs.get('id', None) == 'formMaster')
                # Select the party

                self.br["ctl00$ContentPlaceHolderBody$dropDownListParties"] = \
                    [party[0]]

                # Scroll through each pages of data for the specified party
                # Use the analysis button on the form
                req = self.br.click(type="submit",
                                    name="ctl00$ContentPlaceHolderBody"
                                    "$analysisControl$buttonExport")

                # Navigate to the export menu
                self.br.open(req)
                self.br.select_form(nr=0)
                # Select a csv file
                self.br["ctl00$ContentPlaceHolderBody$export"
                        "Control$dropDownListOptions"] = ['csv']
                result = self.br.submit("ctl00$ContentPlaceHolderBody"
                                        "$exportControl$buttonExport")
                data = result.read()
                # Before writing the file, remove all invalid characters
                file_name = re.sub('\W+', '', party[1])
                # Store the data as a csv file for later use
                file_name = os.path.join(os.getcwd(), RAW_DATA,
                                         year_list[0] + '-' + file_name +
                                         '.csv')
                with open(file_name, 'w') as f:
                    f.write(data)
                # Log the file being written
                self.info_logger.info('%s file written' % file_name)

    def get_available_years(self):
        """!
        This method gets the years for which data was collected by the
        Australian electoral commission.
        @param self The pointer for the object
        """
        # Open the party analysis page
        page = self.br.open(locator_service)
        # Read the page into a soup
        soup = BeautifulSoup(page.read())
        # Get all options
        options = soup.findAll('option')
        for option in options:
            tmp_list = []
            # Get the year value and corresponding form code
            tmp_list.append(option.text.__str__())
            tmp_list.append(option.get("value").__str__())
            self.available_years.append(tmp_list)

    def get_party_list(self):
        """!
        This method gets a list of all the parties registered with the
        Australian electrocal for the selected year
        @param self The pointer for the object
        """
        # Open the party analysis page
        page = self.br.open(party_analysis_address)
        # Read the page into the soup
        soup = BeautifulSoup(page.read())
        # Extract the html code for the party list
        html_parties = soup.findAll('tr')[0].findAll('option')
        # Create a blank list
        self.party_list = []
        for html_party in html_parties:
            tmp_list = []
            value = html_party.get('value').__str__()
            name = html_party.text.__str__()
            tmp_list.append(value)
            tmp_list.append(name)
            self.party_list.append(tmp_list)

    def get_donor_info(self, soup):
        """!
        Scan html code using BeautifulSoup to extract the
        Donor, the donation type, the postcode of the donor and the amount
        @param self The pointer for the object
        @param soup The Beautiful Soup object containing the html data
        @return A list of dictionary objects containing the details of a given
        donation
        """
        trs = soup.findAll('tr')
        data = []
        # Extract the donation information
        for tr in trs:
            if tr.__str__().find('Donor.aspx') >= 0:
                data.append(tr)
        donor_info = []
        for line in data:
            tmp_dict = {}
            # Extract the info from the line
            info = line.findAll('td')
            tmp_dict['name'] = info[0].text.__str__()
            tmp_dict['address'] = info[1].text.__str__()
            tmp_dict['state'] = info[2].text.__str__()
            tmp_dict['postcode'] = info[3].text.__str__()
            tmp_dict['type'] = info[4].text.__str__()
            tmp_dict['amount'] = float(info[5].text.__str__().
                                       replace('$', '').
                                       replace(',', ''))
            donor_info.append(tmp_dict)
        return donor_info
