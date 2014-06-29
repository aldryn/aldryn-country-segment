# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os
import urllib
import gzip
import sched, time

from random import randint
from datetime import datetime, timedelta


class DatGetter(object):

    path = ''
    filename = 'GeoIP.dat'
    url = 'http://geolite.maxmind.com/download/geoip/database/GeoLiteCountry/GeoIP.dat.gz'
    daily = 24 * 3600
    weekly = 7 * 24 * 3600


    def __init__(self):
        '''
        Upon loading this module, it will create a singleton instance of
        itself which figures out where it is on the filesystem, then starts an
        independent process that repeatedly (weekly) checks to see if it has
        an up-to-date GeoIP.dat file, and if not, fetches one.
        '''

        #
        # Fix-up paths
        #
        self.path = os.path.abspath(os.path.dirname(__file__))
        self.zfilepath = os.path.join(self.path, self.filename + '.gz')
        self.filepath = os.path.join(self.path, self.filename)

        pid = os.fork()
        if pid == 0:
            #
            # Set-up a scheduler in another process
            #
            self.scheduler = sched.scheduler(time.time, time.sleep)
            self.scheduler.enter(self.weekly, 1, self.update_dat, (self.scheduler,))
            self.scheduler.run()


    def update_dat(self, scheduler=None):
        '''
        Checks to see if the GeoIP.dat file exists and is less than 1 week
        old, else will fetch (a new) one from MaxMind.

        Returns a path, filename dict suitable for passing to GeoIP(), if
        available, else None.
        '''

        #
        # Since this service may be stopped and started occassionally, we'll
        # not actually initiate a DL from MaxMind unless a GeoIP.dat file
        # doesn't exist or it is already older than 1 week old.
        #
        # This '1 week' only counts when this service is started. Once it is
        # running, it will DL a new file ever 7 days. Since MaxMind only
        # update the file on a monthly basis, this could mean that the file
        # gets, at most, 38 days out-of-date. Any application that requires
        # more up-to-date data should consider a proper MaxMind subscription.
        #
        # If there was an error of some sort, it will re-try in 24 hours.
        #
        if os.path.isfile(self.filepath):
            mtime = os.path.getmtime(self.filepath)
        else:
            mtime = None

        if not mtime or datetime.fromtimestamp(mtime) < datetime.now() - timedelta(days=7):
            print 'Fetching new dat file...'
            try:
                self.get_updated_dat()
                print 'GeoIP.dat file is now updated!'

            except Exception as e:
                print 'Unable to update the GeoIP.dat file: {0}'.format(e)

                #
                # Since there was an error, let's try again in 24 hours.
                #
                if scheduler:
                    scheduler.enter(self.daily, 1, self.update_dat, (scheduler,))

                return None
        else:
            print "GeoIP.dat file is already up-to-date"

        #
        # Schedule another update in a week.
        #
        if scheduler:
            scheduler.enter(self.weekly, 1, self.update_dat, (scheduler,))

        return { 'path': self.path, 'country': self.filename }


    def get_updated_dat(self):
        '''
        Get's the GeoIP.dat.gz file from MaxMind, ungzip it into a temporary
        file, and renames it to the correct filename. May throw exceptions.
        '''

        #
        # Grab the file from MaxMind...
        #
        datfile=urllib.URLopener()
        datfile.retrieve(self.url, self.zfilepath)

        #
        # Ungzip it into a temporary file. This is to minimize having only
        # a partial .dat file in place when a read is required.
        #
        tmpfilepath = os.path.join(self.path, 'temp' + str(randint(1000,9999)) + '.dat')
        with gzip.open(self.zfilepath, 'rb') as zipfile:
            with open(tmpfilepath, 'wb') as datfile:
                datfile.write(zipfile.read())

        #
        # Rename the tmpfilepath to the correct filename
        #
        os.rename(tmpfilepath, self.filepath)

dat_getter = DatGetter()
