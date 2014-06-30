NOTICE
======

This app will not work until Aldryn includes the MaxMind GeoIP C-API into
their build pack. For example:
https://github.com/Bouke/heroku-buildpack-python-geoip/tree/master


Aldryn Country Segmentation
===========================

This segmentation plugin for Aldryn Segmentation relies on middleware to
lookup the (likely) country from MaxMind's GeoIP database for incoming IP
addresses. It isn't 100% accurate, but its pretty close!

The middleware performs the lookup, then places a new attribute on the
HTTPRequest object nameed `COUNTRY_CODE`.

The segmentation plugin contained herein allows any number of "segments" to be
defined based on the COUNTRY_CODE attribute.

Installation
------------

At this time, the package is not submitted to PyPi, but you can still use pip
if you like. Here's how to get started quickly:

NOTE: At this time, the project has been tested under:
- Python 2.6, 2.7, 3.3, 3.4
- Django 1.4, 1.5, 1.6
- django CMS 3.0.2 (276fd37b0e49555bafce6c071ca50508de5e4c49 or later)
- Aldryn Segmentation 0.4.0 or later

1. Make sure you're using a version of django-CMS that is later than
   3.0.2.dev1, otherwise the Segment menu will not appear correctly and likely
   the whole toolbar won't render at all and you may have trouble with
   AliasPlugins.
1. Install Aldryn Segmentation (not yet in PyPI).
1. Add `'country-segment'` to INSTALLED_APPS in your Django project's
   settings file.
1. Add `country_segment.middleware.ResolveCountryCodeMiddleware`
   to your settings.MIDDLEWARE.
1. `python manage.py schemamigration country_segment --initial`.
1. `python manage.py migrate country_segment`.
1. Properly configure your installation with the MaxMind dataset (read on).

Optional but recommended:

1. Install django-easy select2: `pip install django-easy-select2` (highly
   recommended).
1. Add `'easy_select2'` to your project's settings.INSTALLED_APPS.


Setup the GeoIP Database
------------------------

MaxMind (http://www.maxmind.com/) generously provide a free "lite" version of
their geo-location products. The one we're interested in here is called
"GeoLite Country" and is effectively a static database in a single file:
`GeoIP.dat`.

This database is *not* distributed with Aldryn Country Segment, however, this
version of this app will automatically get it for you.

NOTE: There is no need to include any settings for GEO_IP. If you provide some
anyway, the middleware will not use them.
````

# Install the middleware. Should go near the top.
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'country_segment.middleware.resolve_country_code_middleware.ResolveCountryCodeMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    ...
)
````

On application server start, the middleware will emit a warning to your
console/logs: "GeoIP database is not initialized." if it could not find or
otherwise initialize the database.


Helpful links
-------------

- https://docs.djangoproject.com/en/dev/ref/contrib/gis/geoip/
- http://dev.maxmind.com/geoip/
