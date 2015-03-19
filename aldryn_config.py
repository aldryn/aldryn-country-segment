# -*- coding: utf-8 -*-

from aldryn_client import forms

class Form(forms.BaseForm):

    def to_settings(self, cleaned_data, settings_dict):
        settings_dict['MIDDLEWARE_CLASSES'].append(
            'country_segment.middleware.ResolveCountryCodeMiddleware')
        return settings_dict
