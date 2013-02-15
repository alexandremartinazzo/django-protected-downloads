# -*- coding: utf-8 -*-

from django.test import TestCase
from django.test.client import Client
from django.test.utils import override_settings
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ImproperlyConfigured

import os

class DownloadTest(TestCase):
    def setUp(self):
        self.client = Client()

        # creates a file with a UUID name
        self.base_dir = settings.MEDIA_ROOT
        self.directory = 'rg'
        self.filename = '41677f81-2e93-5461-9fde-53263b1079ce.txt'
        self.path = os.path.join(self.base_dir, self.directory, self.filename)
        instance = open(self.path, 'a')
        instance.write('This is a test\n')
        instance.close()

        self.username = '55555555555'
        self.password = 'senha'
        User.objects.create_user(self.username, 'user@email.com', self.password)

    def tearDown(self):
        os.remove( self.path )

    def test_file_does_not_exist(self):
        ''' if file does not exist, raises a 404 error '''

        url = settings.MEDIA_URL + 'unknown/does_not_exist.pdf/'
        response_detail = self.client.get( url )
        self.assertEqual( response_detail.status_code, 404 )

    def test_file_exist(self):
        ''' if file does exist, return a file for download
            (django returns an empty file in development mode) '''

        url = settings.MEDIA_URL + self.directory + '/' + self.filename + '/'
        self.client.login( username=self.username, password=self.password )
        response_detail = self.client.get( url )
        self.assertEqual( response_detail.status_code, 200 )

    def test_file_exist_no_login(self):
        ''' if user is not logged in, redirects to login page '''

        url = settings.MEDIA_URL + self.directory + '/' + self.filename + '/'
        expected_url = settings.LOGIN_URL + '?next=' + url

        response_detail = self.client.get( url, follow=True )

        self.assertRedirects( response_detail, expected_url )

    def test_wrong_user(self):
        ''' user tries to access a file URL but he/she is not authorized
        to do so because the file is not hers/his; should raise a 404 error.
        '''

        user = 'wrong_user'
        password = 'password'
        User.objects.create_user(user, 'wrong@user.com', password)
        url = settings.MEDIA_URL + self.directory + '/' + self.filename + '/'

        self.client.login( username=user, password=password )
        response_detail = self.client.get( url )
        self.assertEqual( response_detail.status_code, 404 )

    def test_staff_user(self):
        ''' an admin site user tries to access an existing file '''

        user = 'staff'
        password = 'passwd'
        # Create staff member
        instance = User.objects.create_user(user, 'staff@email.com', password)
        instance.is_staff = True
        instance.save()

        # Existing file URL
        url = settings.MEDIA_URL + self.directory + '/' + self.filename + '/'

        self.client.login( username=user, password=password )
        response_detail = self.client.get( url )
        self.assertEqual( response_detail.status_code, 200 )


class ConfigurationTest(TestCase):
    def setUp(self):
        self.client = Client()

        self.base_dir = settings.MEDIA_ROOT
        self.directory = 'rg'
        self.filename = '41677f81-2e93-5461-9fde-53263b1079ce.txt'

    @override_settings(PROTECTED_DOWNLOADS_GENERATOR = 'invalid.module.function')
    def test_filename_generator(self):
        ''' if filename generator function can't be imported,
        raises an ImproperlyConfigured error '''

        url = settings.MEDIA_URL + self.directory + '/' + self.filename + '/'
        self.assertRaises(ImproperlyConfigured, self.client.get, url)

