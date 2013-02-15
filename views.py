# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

import os
import mimetypes

def get_class( kls ):
    ''' returns a function or class from a given string
    adapted from: http://stackoverflow.com/a/452981/375789
    '''
    parts = kls.split('.')
    module = ".".join(parts[:-1])
    try:
        m = __import__( module )
        for comp in parts[1:]:
            m = getattr(m, comp)
        return m
    except ImportError, AttributeError:
        raise

# import a generic filename generator function provided by settings; this function
# should return a unique filename taking 'user' and 'filename.ext' as parameters
FILENAME_GENERATOR = None
try:
    function_string = settings.PROTECTED_DOWNLOADS_GENERATOR
    FILENAME_GENERATOR = get_class( function_string )
except Exception:
    raise ImproperlyConfigured


def can_access_url(user, filename):
    ''' verificação simples se um usuário pode acessar um arquivo '''
    correct_name = FILENAME_GENERATOR(user, filename)
    if user.is_staff or correct_name == filename:
        return True
    else:
        return False

@login_required
def simple_download(request, category, filename):
    file_path = os.path.join( category, filename )
    directory = os.path.join( settings.MEDIA_ROOT, category )

    if filename not in os.listdir(directory):
        raise Http404

    if not can_access_url(request.user, filename):
        raise Http404

    full_path = os.path.join( directory, filename )

    response = HttpResponse()
    mime, encoding = mimetypes.guess_type( full_path )
    response['Content-Type'] = mime
    response['X-Accel-Redirect'] = '/protected/' + file_path
    response['Content-Disposition'] = 'attachment;filename=' + filename

    return response

