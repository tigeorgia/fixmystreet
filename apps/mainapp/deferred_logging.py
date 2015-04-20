import os
from logging import FileHandler as BaseFileHandler

try:
    import codecs
except ImportError:
    codecs = None


class DefferedFileHandler(BaseFileHandler):

    def __init__(self, filename, *args, **kwargs):
        self.filename = filename
        kwargs['delay'] = True
        super(DefferedFileHandler, self).__init__('/dev/null', *args, **kwargs)

    def set_stream(self):
        if self.encoding is None:
            stream = open(self.baseFilename, self.mode)
        else:
            stream = codecs.open(self.baseFilename, self.mode, self.encoding)
        return stream

    def _open(self):
        from django.conf import settings

        if not os.path.exists(settings.LOG_PATH):
                os.makedirs(settings.LOG_PATH)

        self.baseFilename = os.path.join(settings.LOG_PATH, self.filename)
        stream = self.set_stream()
        return stream
