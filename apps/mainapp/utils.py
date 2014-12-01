import os
import random
import datetime

from django.conf import settings
from django.db.models import Q
from django.core.cache import caches

from apps.mainapp.models import Report


def random_image(image_dir=''):
    try:
        valid_extensions = settings.RANDOM_IMAGE_EXTENSIONS
    except AttributeError:
        valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', ]

    if image_dir:
        rel_dir = image_dir
    else:
        rel_dir = settings.RANDOM_IMAGE_DIR

    rand_dir = os.path.join(settings.STATIC_ROOT, rel_dir)
    files = [f for f in os.listdir(rand_dir) if os.path.splitext(f)[1] in valid_extensions]

    #Don't cache these images
    image = os.path.join(rel_dir, random.choice(files))
    image.split('.')[0].join('.').join(image.split('.')[-1])

    return image


class ReportCount(object):
    def __init__(self, start, end, status=None):
        self.start = start
        self.end = end
        self.status = status
        self._cache = caches['default']

    @classmethod
    def by_interval(cls, interval):
        formats = {'day': 1, 'week': 7, 'month': 30, 'year': 365}  # Accepted formats with their day multipliers
        formatting_error = "Incorrect interval formatting. '%d %s' is the correct format. Example: 1 year"

        try:
            count, datetype = interval.strip().split(' ')
        except ValueError as e:
            raise type(e)(formatting_error)

        if datetype not in formats.keys():
            raise ValueError(formatting_error)

        start = datetime.datetime.now().date() - datetime.timedelta(days=int(count) * formats[datetype])
        end = datetime.datetime.now().date()

        return cls(start=start, end=end)

    def fixed(self):
        self.status = 'fixed'
        return self

    def not_fixed(self):
        self.status = 'not-fixed'
        return self

    @property
    def count_cache(self):
        cache_key = 'repcnt_{0}_{1}_{2}'.format(self.status, self.start.isoformat(), self.end.isoformat())
        return self._cache.get(cache_key)

    @count_cache.setter
    def count_cache(self, value):
        cache_key = 'repcnt_{0}_{1}_{2}'.format(self.status, self.start.isoformat(), self.end.isoformat())
        self._cache.set(cache_key, value, 60 * 60 * 24)

    def get_counts(self):
        q = Q(created_at__range=(self.start, self.end))
        q.add(Q(status=self.status), Q.AND) if self.status else None

        report_count = Report.objects.filter(q).count() if not self.count_cache else self.count_cache
        self.count_cache = report_count

        self.status = None
        return report_count
