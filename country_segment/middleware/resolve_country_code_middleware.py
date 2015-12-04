# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from aldryn_geoip.core import get_country


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
        try:
            country_data = get_country(request)
        except Exception:
            country_code = 'XB'
        else:
            country_code = country_data.get('country_code')

        if country_code:
            country_code = country_code.upper()
        else:
            country_code = 'XX'

        request.META['COUNTRY_CODE'] = country_code
