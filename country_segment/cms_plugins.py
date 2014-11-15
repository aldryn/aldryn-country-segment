# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from cms.plugin_pool import plugin_pool

from aldryn_segmentation.cms_plugins import SegmentPluginBase

from .models import CountrySegmentPluginModel

class CountrySegmentPlugin(SegmentPluginBase):
    '''
    This plugin allows segmentation based on the visitor's IP addresses
    associated country code. Use of this segment requires the use of the
    'resolve_country_code_middleware' provided in this distribution. This
    middleware, in turn, depends on django.contrib.geo_ip and MaxMind's
    GeoLite dataset or similar.
    '''

    model = CountrySegmentPluginModel
    name = _('Segment by country')

    #
    # If django-easy-select2 is installed, we can greatly enhance the
    # useability of this change form.
    #
    try:
        from easy_select2 import select2_modelform
        form = select2_modelform(CountrySegmentPluginModel, attrs={'width': '250px'})
    except:
        pass

    def is_context_appropriate(self, context, instance):
        code = context.get('COUNTRY_CODE')
        return (code == instance.country_code)

plugin_pool.register_plugin(CountrySegmentPlugin)
