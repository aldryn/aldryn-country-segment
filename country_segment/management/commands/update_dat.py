# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from ...dat_getter import DatGetter

class Command(BaseCommand):

    help = 'Re-downloads the MaxMind dat file, if it is older than 1 week locally.'

    def handle(self, *args, **kwargs):
    	DatGetter()
