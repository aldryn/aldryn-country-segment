# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from aldryn_geoip.core import get_country


def cowboy_log(msg):
    # DEBUG
    with open('/tmp/segmentation-debug.log', 'a') as debug_file:
        debug_file.write('{}\n'.format(msg))


class ResolveCountryCodeMiddleware(object):

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

        try:
            country_code = get_country(request)

            if country_code:
                country_code = country_code.upper()
            else:
                country_code = 'XX'
                cowboy_log('Country could not be determined') # DEBUG
        except Exception as ex:
            country_code = 'XB'
            cowboy_log(
                'Error trying to determine country: {} {}\n'.format(
                    repr(ex), str(ex))) # DEBUG

        cowboy_log('COUNTRY_CODE == {}'.format(country_code)) # DEBUG

        request.META['COUNTRY_CODE'] = country_code
