# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

# regex for filename based on UUID + extension (of 3 or 4 digits):
# UUID: [a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}'
# extension: r'.\w{3,4}/$'
uuid_filename = r'(?P<filename>' + \
            r'[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}' + \
            r'\.\w{3,4})/$'
expression = r'^(?P<category>\w*)/' + uuid_filename

urlpatterns = patterns('',
    url(
        expression,
        'protected_downloads.views.simple_download',
        name = 'protected_uuid_file',
    ),
)


