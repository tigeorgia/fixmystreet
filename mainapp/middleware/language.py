from django.conf.global_settings import LANGUAGES
from django.conf import settings
from django.http import HttpResponsePermanentRedirect, HttpResponse
from django.utils import translation


class LanguagePrefixMiddleware:
    def process_request(self, request):
        LANG_BLACKLIST = ['i18n', 'jsi18n', 'media']
        l_path = request.path.split('/')
        request.session['path_without_lang'] = request.path
        codes = []
        for code, name in LANGUAGES:
            codes.append(code)
        if l_path[1] in codes:
            del l_path[1]
            path_without_lang = '/'.join(l_path)
            request.session['path_without_lang'] = path_without_lang
        elif l_path[1] not in codes and l_path[1] not in LANG_BLACKLIST:
            cur_lang = request.session.get('django_language', settings.LANGUAGE_CODE)
            path = ('/' + cur_lang + request.path)
            return HttpResponsePermanentRedirect(path)