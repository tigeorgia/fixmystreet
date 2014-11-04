from django.conf.global_settings import LANGUAGES
from django.conf import settings
from django.http import HttpResponsePermanentRedirect, HttpResponse
from django.utils import translation


class LanguagePrefixMiddleware:
    def __init__(self):
        self.lang_blacklist = ['i18n', 'jsi18n', 'media', 'admin', 'rosetta', 'accounts', 'static', '__debug__']
        self.codes = []

    def process_request(self, request):
        #Get the path without language code
        l_path = request.path.split('/')
        request.session['path_without_lang'] = request.path

        for code, name in LANGUAGES:
            self.codes.append(code)
        if l_path[1] in self.codes:
            del l_path[1]
            path_without_lang = '/'.join(l_path)
            request.session['path_without_lang'] = path_without_lang
        elif l_path[1] not in self.codes and l_path[1] not in self.lang_blacklist:
            cur_lang = request.session.get('django_language', settings.LANGUAGE_CODE)
            path = ('/' + cur_lang + request.path)
            return HttpResponsePermanentRedirect(path)