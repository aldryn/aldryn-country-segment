# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from country_segment import __version__

REQUIREMENTS = [
    'aldryn-geoip',
]

CLASSIFIERS = [
    'Development Status :: 2 - Pre-Alpha',
    'Environment :: Web Environment',
    'Framework :: Django',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    'Topic :: Software Development',
    'Topic :: Software Development :: Libraries :: Application Frameworks',
]

setup(
    name='aldryn-country-segment',
    version=__version__,
    description='A Country Segment for Aldryn Segmentation for django CMS',
    author='Divio AG',
    author_email='info@divio.ch',
    url='https://github.com/aldryn/aldryn-country-segment',
    packages=find_packages(),
    package_data={
        "country_segment": [
            "locale/*/LC_MESSAGES/*",
        ],
    },
    license='LICENSE.txt',
    platforms=['OS Independent'],
    install_requires=REQUIREMENTS,
    classifiers=CLASSIFIERS,
    include_package_data=True,
    zip_safe=False
)
