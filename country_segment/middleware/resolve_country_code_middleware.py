# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import warnings
# XXX intellectronica 2015-03-19
# Disabling dat_getter for now. Users need to make sure they have the GeoIP
# DB installed to use this.
# from ..dat_getter import dat_getter

from django.contrib.gis.geoip import GeoIP


def cowboy_log(msg):
    # DEBUG
    with open('/tmp/segmentation-debug.log', 'a') as debug_file:
        debug_file.write('{}\n'.format(msg))


class ResolveCountryCodeMiddleware(object):

    def __init__(self):
        cowboy_log('Entering ResolveCountryCodeMiddleware.__init__') # DEBUG
        try:
            # XXX intellectronica 2015-03-19
            # Disabling dat_getter for now. Users need to make sure they have
            # the GeoIP DB installed to use this.
            # country_data = dat_getter.update_dat()
            # The values supplied here only work in the
            # Aldryn base project >= 1.4.2
            country_data = {
                'path': '/opt/geoip',
                'country': 'GeoIP.dat',
            }
            self.geo_ip = GeoIP(**country_data)
            cowboy_log('ResolveCountryCodeMiddleware.__init__ self.geoip == {}'.format(self.geo_ip)) # DEBUG
        except Exception as e:
            warnings.warn('GeoIP database is not initialized: {0}'.format(e))
            cowboy_log('GeoIP database is not initialized: {0}\n'.format(e)) # DEBUG
            self.geo_ip = False


    def get_client_ip(self, request):
        #
        # NOTE: this is a particularly naïve implementation! See:
        # http://esd.io/blog/flask-apps-heroku-real-ip-spoofing.html
        #
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


    def process_request(self, request):

        '''
        Use the GeoIP API to resolve country codes from the visitors IP
        Address. In case the IP address does not resolve or of technical
        issues, the resulting code may be set to one {'XA', 'XB', ... 'XZ'}.
        This range is explicitly reserved for 'private use', so should never
        conflict.

        See: http://en.wikipedia.org/wiki/ISO_3166-1_alpha-2
        '''

        cowboy_log('Entering process_request') # DEBUG

        if self.geo_ip:
            try:
                country_code = self.geo_ip.country_code(self.get_client_ip(request))
                if country_code:
                    country_code = country_code.upper()
                else:
                    country_code = 'XX'
                    cowboy_log('Country could not be determined') # DEBUG
            except Exception, ex:
                country_code = 'XB'
                cowboy_log(
                    'Error trying to determine country: {} {}\n'.format(
                        repr(ex), str(ex))) # DEBUG
        else:
            country_code = 'XA'
            cowboy_log('GeoIP not initialised.') # DEBUG

        cowboy_log('COUNTRY_CODE == {}'.format(country_code)) # DEBUG

        request.META['COUNTRY_CODE'] = country_code
