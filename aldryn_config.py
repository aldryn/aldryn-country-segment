# -*- coding: utf-8 -*-

from aldryn_client import forms

class Form(forms.BaseForm):
    def to_settings(self, cleaned_data, settings_dict):
        country_mw = 'country_segment.middleware.ResolveCountryCodeMiddleware'
        if country_mw not in settings_dict['MIDDLEWARE_CLASSES']:
            for position, mw in enumerate(settings_dict['MIDDLEWARE_CLASSES']):
                #
                # Its not a strict requirement that the
                # ResolveCountryCodeMiddleware go after SessionMiddleware,
                # but, it seems like a pretty nice place.
                #
                if mw == 'django.contrib.sessions.middleware.SessionMiddleware':
                    settings_dict['MIDDLEWARE_CLASSES'].insert(position + 1, country_mw)
                    break
            else:
                #
                # B'okay, not sure how this CMS installation works, but...
                # let's just put it at the top.
                #
                settings_dict['MIDDLEWARE_CLASSES'].insert(0, country_mw)

        return settings_dict
