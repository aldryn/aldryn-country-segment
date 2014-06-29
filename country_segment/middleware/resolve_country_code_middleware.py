# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import warnings
from ..dat_getter import dat_getter

from django.contrib.gis.geoip import GeoIP


class ResolveCountryCodeMiddleware(object):

    '''
    This middleware uses the GeoIP API to resolve country codes from the
    visitors IP Address.
    '''

    def __init__(self):
        try:
            country_data = dat_getter.update_dat()
            print 'GeoIP data at: {0}'.format(country_data)
            self.geo_ip = GeoIP(**country_data)
        except Exception as e:
            warnings.warn('GeoIP database is not initialized: {0}'.format(e))
            self.geo_ip = False


    def get_country_code(self, ipa):
        if self.geo_ip:
            try:
                return self.geo_ip.country(ipa)['country_code'].upper()
            except:
                pass
        return None


    def process_request(self, request):
        ipa = request.META.get("HTTP_X_FORWARDED_FOR",
            request.META["REMOTE_ADDR"])
        request.META['COUNTRY_CODE'] = self.get_country_code(ipa)
