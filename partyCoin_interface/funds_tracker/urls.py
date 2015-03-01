#! /usr/bin/env python
"""!
-----------------------------------------------------------------------------
File Name : urls.py

Purpose: url handler for funds_tracker app

Created: 01-Mar-2015 23:32:20 AEDT
-----------------------------------------------------------------------------
Revision History



-----------------------------------------------------------------------------
S.D.G
"""
__author__ = 'Ben Johnston'
__revision__ = '0.1'
__date__ = '01-Mar-2015 23:32:20 AEDT'
__license__ = 'MPL v2.0'

## LICENSE DETAILS############################################################
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

##IMPORTS#####################################################################
from django.conf.urls import patterns, url
from funds_tracker import views
##############################################################################

urlpatterns = patterns('',
                       url(r'^$', views.IndexView.as_view(), name='index'),
                       )
