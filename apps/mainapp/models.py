# -*- coding: utf-8 -*-
import hashlib
import urllib
import time
from datetime import datetime as dt
import json

from django.db import connection
from django.contrib.gis.db import models
from django.contrib.gis.maps.google import GoogleMap, GMarker, GEvent, GPolygon, GIcon
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import send_mail, EmailMessage
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.utils import translation
from transmeta import TransMeta
from stdimage import StdImageField
from django.utils.encoding import iri_to_uri

from apps.mainapp import emailrules
from signals import councillor_notified


class CCEmailMessage(EmailMessage):
    def __init__(self, subject='', body='', from_email=None, to=None, cc=None,
                 bcc=None, connection=None, attachments=None, headers=None):
        super(CCEmailMessage, self).__init__(subject, body, from_email, to,
                                             bcc, connection, attachments, headers)
        if cc:
            self.cc = list(cc)
        else:
            self.cc = []

    def recipients(self):
        """
        Returns a list of all recipients of the email
        """
        return super(CCEmailMessage, self).recipients() + self.cc

    def message(self):
        msg = super(CCEmailMessage, self).message()
        if self.cc:
            msg['Cc'] = ', '.join(self.cc)
        return msg


class Province(models.Model):
    __metaclass__ = TransMeta

    name = models.CharField(max_length=100, verbose_name=_("Name"))
    abbrev = models.CharField(max_length=3)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = u'province'
        translate = ('name',)


class City(models.Model):
    __metaclass__ = TransMeta

    province = models.ForeignKey(Province)
    name = models.CharField(max_length=100, verbose_name=_("Name"))
    # the city's 311 email, if it has one.
    email = models.EmailField(blank=True, null=True)

    objects = models.GeoManager()

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return "/cities/" + str(self.id)

    @property
    def get_all_cities(self):
        return City.objects.all()

    class Meta:
        db_table = u'cities'
        translate = ('name',)


class Councillor(models.Model):
    __metaclass__ = TransMeta

    first_name = models.CharField(max_length=100, verbose_name=_("First name"))
    last_name = models.CharField(max_length=100, verbose_name=_("Last name"))

    # this email addr. is used to send reports to if there is no 311 email for the city.
    email = models.EmailField(blank=True, null=True)
    fax = models.CharField(max_length=20, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)

    def __unicode__(self):
        return self.last_name

    class Meta:
        db_table = u'councillors'
        translate = ('first_name', 'last_name',)


class Ward(models.Model):
    __metaclass__ = TransMeta

    name = models.CharField(max_length=100, verbose_name=_("Name"))
    number = models.IntegerField()
    councillor = models.ForeignKey('users.FMSUser', limit_choices_to={'is_councillor': True})
    city = models.ForeignKey(City)
    geom = models.MultiPolygonField(null=True)
    objects = models.GeoManager()

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return "/wards/" + str(self.id)

    # return a list of email addresses to send new problems in this ward to.
    def get_emails(self, report):
        to_emails = []
        cc_emails = []
        if self.city.email:
            to_emails.append(self.city.email)

        # check for rules for this city.
        rules = EmailRule.objects.filter(city=self.city)
        for rule in rules:
            rule_email = rule.get_email(report)
            if rule_email:
                if not rule.is_cc:
                    to_emails.append(rule_email)
                else:
                    cc_emails.append(rule_email)
        return ( to_emails, cc_emails )

    class Meta:
        db_table = u'wards'
        translate = ('name', )


class ReportCategoryClass(models.Model):
    __metaclass__ = TransMeta

    name = models.CharField(max_length=100, verbose_name=_("Title"))

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = u'report_category_classes'
        translate = ('name', )


class ReportCategory(models.Model):
    __metaclass__ = TransMeta

    name = models.CharField(max_length=100, verbose_name=_("Title"))
    hint = models.TextField(blank=True, null=True, verbose_name=_("Hint"))
    category_class = models.ForeignKey(ReportCategoryClass)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return "category/" + str(self.id)

    class Meta:
        db_table = u'report_categories'
        translate = ('name', 'hint', )


# Override where to send a report for a given city.
#
# If no rule exists, the email destination is the 311 email address
# for that city.
#
# Cities can have more than one rule.  If a given report matches more than
# one rule, more than one email is sent.  (Desired behaviour for cities that
# want councillors CC'd)

class EmailRule(models.Model):
    TO_COUNCILLOR = 0
    MATCHING_CATEGORY_CLASS = 1
    NOT_MATCHING_CATEGORY_CLASS = 2

    RuleChoices = [
        (TO_COUNCILLOR, 'Send Reports to Councillor Email Address'),
        (MATCHING_CATEGORY_CLASS, 'Send Reports Matching Category Class (eg. Parks) To This Email'),
        (NOT_MATCHING_CATEGORY_CLASS, 'Send Reports Not Matching Category Class To This Email'), ]

    RuleBehavior = {TO_COUNCILLOR: emailrules.ToCouncillor,
                    MATCHING_CATEGORY_CLASS: emailrules.MatchingCategoryClass,
                    NOT_MATCHING_CATEGORY_CLASS: emailrules.NotMatchingCategoryClass}

    rule = models.IntegerField(choices=RuleChoices)

    # is this a 'to' email or a 'cc' email
    is_cc = models.BooleanField(default=False)

    # the city this rule applies to
    city = models.ForeignKey(City)

    # filled in if this is a category class rule
    category_class = models.ForeignKey(ReportCategoryClass, null=True, blank=True)

    # filled in if this is a category rule
    category = models.ForeignKey(ReportCategory, null=True, blank=True)

    # filled in if an additional email address is required for the rule type
    email = models.EmailField(blank=True, null=True)

    def get_email(self, report):
        rule_behavior = EmailRule.RuleBehavior[self.rule]()
        return rule_behavior.get_email(report, self)

    def __str__(self):
        rule_behavior = EmailRule.RuleBehavior[self.rule]()
        if self.is_cc:
            prefix = "CC:"
        else:
            prefix = "TO:"
        return "%s - %s (%s)" % (self.city.name, rule_behavior.describe(self), prefix)


class ActiveManager(models.Manager):
    """
    Filtering out inactive items from QuerySet
    """

    def get_queryset(self):
        return super(ActiveManager, self).get_queryset().filter(is_active=True, user__is_active=True,
                                                                user__is_confirmed=True)


class Report(models.Model):
    NOT_FIXED = 'not-fixed'
    FIXED = 'fixed'
    IN_PROGRESS = 'in-progress'
    REPORT_STATUS_CHOICES = (
        (NOT_FIXED, _('Not Fixed')),
        (FIXED, _('Fixed')),
        (IN_PROGRESS, _('In Progress'))
    )

    # ForeignKeys
    category = models.ForeignKey(ReportCategory, verbose_name=_("category"), help_text=_('Report category'))
    user = models.ForeignKey('users.FMSUser', related_name='reports', help_text=_('Author of the report'))
    ward = models.ForeignKey(Ward, verbose_name=_("ward"), help_text=_('Ward associated with report'))

    # CharFields
    street = models.CharField(max_length=255, verbose_name=_("street address"), help_text=_("Address of the problem"))
    status = models.CharField(_('status'), max_length=32, choices=REPORT_STATUS_CHOICES,
                              default=NOT_FIXED, help_text=_('Report status'))
    sent_at = models.DateTimeField(null=True, help_text=_('Date when report was sent to city representative'))
    title = models.CharField(max_length=100, verbose_name=_("title"), help_text=_('Report title'))

    # BooleanFields
    is_active = models.BooleanField(default=True)

    # DateTimeFields
    created_at = models.DateTimeField(auto_now_add=True, help_text=_('Date when report was created'))
    fixed_at = models.DateTimeField(blank=True, null=True, help_text=_('Date when report was fixed'))
    reminded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, help_text=_('Date when report was updated'))

    # Other fields
    desc = models.TextField(verbose_name=_("details"), help_text=_('Report description'))
    email_sent_to = models.EmailField(blank=True, null=True)
    ip = models.GenericIPAddressField(blank=True, null=True)
    # Postgis 1.5 is breaking migrations on this field. See https://code.djangoproject.com/ticket/23085
    point = models.PointField(null=True)

    objects = models.GeoManager()
    active = ActiveManager()

    def __unicode__(self):
        return self.title

    @property
    def is_fixed(self):
        if self.status is 'fixed':
            return True

    @property
    def get_status(self):
        return self.status

    @property
    def has_photo(self):
        return True if self.photo else False

    def is_subscribed(self, email):
        if len(self.subscribers.filter(email=email)) != 0:
            return True
        return self.first_update().email == email

    def sent_at_diff(self):
        if not self.sent_at:
            return ( None )
        else:
            return self.sent_at - self.created_at

    @property
    def subscriber_count(self):
        return self.subscribers.count() + 1

    def get_last_update(self):
        return self.report_updates.order_by('-created_at').first()

    def get_first_update(self):
        return ReportUpdate.objects.get(report=self, first_update=True)

    def get_absolute_url(self):
        return reverse('report_detail', args=[self.id])

    def get_full_absolute_url(self):
        return '{0}{1}'.format(settings.SITE_URL, self.get_absolute_url())

    def email_councillor(self):
        """
        Email councillor that report was created
        """
        if self.user.is_confirmed and self.user.is_active:
            councillor = self.ward.councillor
            user_language = councillor.user_settings.language
            translation.activate(user_language)
            subject = render_to_string("emails/send_report_to_city/subject.txt", {'report': self})
            message = render_to_string("emails/send_report_to_city/message.txt", {'report': self})
            councillor.email_user(subject, message)
            #Send signal that councillor was notified
            councillor_notified.send(sender=self.__class__, report=self, councillor=councillor)

    class Meta:
        db_table = u'reports'
        ordering = ['-created_at']


class ReportPhoto(models.Model):
    report = models.ForeignKey('mainapp.Report', related_name='report_photos')
    photo = StdImageField(upload_to="photos", blank=True, verbose_name=_("photo"),
                          variations={'large': (800, 600), 'thumbnail': (133, 100)},
                          help_text=_('Report photo'))


class ReportCount(object):
    def __init__(self, interval):
        self.interval = interval

    def dict(self):
        return ({
                    "recent_new": "count( case when age(clock_timestamp(), reports.created_at) < interval '%s' THEN 1 ELSE null end )" % self.interval,
                    "recent_fixed": "count( case when age(clock_timestamp(), reports.fixed_at) < interval '%s' AND reports.status = 'fixed' THEN 1 ELSE null end )" % self.interval,
                    "recent_updated": "count( case when age(clock_timestamp(), reports.updated_at) < interval '%s' AND reports.status = 'not-fixed' and reports.updated_at != reports.created_at THEN 1 ELSE null end )" % self.interval,
                    "old_fixed": "count( case when age(clock_timestamp(), reports.fixed_at) > interval '%s' AND reports.status = 'fixed' THEN 1 ELSE null end )" % self.interval,
                    "old_unfixed": "count( case when age(clock_timestamp(), reports.fixed_at) > interval '%s' AND reports.status = 'not-fixed' THEN 1 ELSE null end )" % self.interval} )


class ReportUpdate(models.Model):
    NOT_FIXED = 'not-fixed'
    FIXED = 'fixed'
    IN_PROGRESS = 'in-progress'
    REPORT_STATUS_CHOICES = (
        (NOT_FIXED, _('Not Fixed')),
        (FIXED, _('Fixed')),
        (IN_PROGRESS, _('In Progress'))
    )

    # ForeignKeys
    report = models.ForeignKey(Report, related_name='report_updates')
    user = models.ForeignKey('users.FMSUser', related_name='report_updates')

    # CharFields
    status = models.CharField(_('status'), max_length=32, choices=REPORT_STATUS_CHOICES, default=NOT_FIXED)

    # BooleanFields
    is_active = models.BooleanField(default=True)

    # DateTimeFields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Other fields
    desc = models.TextField(verbose_name=_("details"))
    ip = models.GenericIPAddressField(null=True)
    photo = StdImageField(upload_to="photos/updates", blank=True, verbose_name=_("photo"),
                          variations={'large': (800, 600), 'thumbnail': (133, 100)})

    active = ActiveManager()

    def __unicode__(self):
        return self.report.title

    def get_absolute_url(self):
        return reverse('report_detail', kwargs={'pk': self.report_id})

    def send_emails(self):
        if self.first_update:
            self.notify_on_new()
        else:
            self.notify_on_update()

    @property
    def is_fixed(self):
        if self.status is 'fixed':
            return True

    @property
    def get_status(self):
        return self.status

    def notify_on_new(self):
        # send to the city immediately.
        subject = render_to_string("emails/send_report_to_city/subject.txt", {'update': self})
        message = render_to_string("emails/send_report_to_city/message.txt", {'update': self})

        to_email_addrs, cc_email_addrs = self.report.ward.get_emails(self.report)
        email_msg = CCEmailMessage(subject, message, settings.EMAIL_FROM_USER,
                                   to_email_addrs, cc_email_addrs, headers={'Reply-To': self.email})
        if self.report.photo:
            email_msg.attach_file(self.report.photo.file.name)

        email_msg.send()

        # update report to show time sent to city.
        self.report.sent_at = dt.now()
        email_addr_str = ""
        for email in to_email_addrs:
            if email_addr_str != "":
                email_addr_str += ", "
            email_addr_str += email

        self.report.email_sent_to = email_addr_str
        self.report.save()

    def notify_on_update(self):
        subject = render_to_string("emails/report_update/subject.txt",
                                   {'update': self})

        # tell our subscribers there was an update.
        for subscriber in self.report.subscribers.all():
            unsubscribe_url = settings.SITE_URL + "/reports/subscribers/unsubscribe/" + subscriber.confirm_token
            message = render_to_string("emails/report_update/message.txt",
                                       {'update': self, 'unsubscribe_url': unsubscribe_url})
            send_mail(subject, message,
                      settings.EMAIL_FROM_USER, [subscriber.email], fail_silently=False)

        # tell the original problem reporter there was an update
        message = render_to_string("emails/report_update/message.txt",
                                   {'update': self})
        send_mail(subject, message,
                  settings.EMAIL_FROM_USER,
                  [self.report.first_update().email], fail_silently=False)

    def title(self):
        if self.first_update:
            return self.report.title
        if self.is_fixed:
            return "Reported Fixed"
        return "Update"

    class Meta:
        db_table = u'report_updates'
        ordering = ['-created_at']


class ReportSubscriber(models.Model):
    """
        Report Subscribers are notified when there's an update.
    """

    report = models.ForeignKey(Report, related_name='subscribers')
    confirm_token = models.CharField(max_length=255, null=True)
    is_confirmed = models.BooleanField(default=False)
    email = models.EmailField(verbose_name=_('Email'))

    class Meta:
        db_table = u'report_subscribers'


    def save(self):
        if not self.confirm_token or self.confirm_token == "":
            m = hashlib.md5()
            m.update(self.email)
            m.update(str(time.time()))
            self.confirm_token = m.hexdigest()
            confirm_url = settings.SITE_URL + "/reports/subscribers/confirm/" + self.confirm_token
            message = render_to_string("emails/subscribe/message.txt",
                                       {'confirm_url': confirm_url, 'subscriber': self})
            send_mail('FixMyStreet.ge-ზე გამოწერილი შეტყობინების განახლებები', message,
                      settings.EMAIL_FROM_USER, [self.email], fail_silently=False)
        super(ReportSubscriber, self).save()


class VerifiedAuthor(models.Model):
    """ Email domains; report updates by authors from these email domains will be marked as verified."""

    domain = models.CharField(max_length=255, verbose_name=_("Domain"))
    name = models.CharField(max_length=255, verbose_name=_("Name"))

    def __unicode__(self):
        return self.name


# This and subsequent 'XMap' classes should probably be in
# views somewhere--their primary function is as intermediate
# classes to aid in displaying model data on maps.
class ReportMarker(GMarker):
    """
        A marker for an existing report.  Override the GMarker class to
        add a numbered, coloured marker.

        If the report is fixed, show a green marker, otherwise red.
    """

    def __init__(self, report, icon_number):
        if report.status is 'fixed':
            color = 'green'
        elif report.status is 'not-fixed':
            color = 'red'
        elif report.status is 'in-progress':
            color = 'yellow'
        icon_number = icon_number
        # img = "/static/images/marker/%s/marker%s.png" %( color, icon_number )
        img = "/static/images/marker/%s/blank.png" % ( color)
        name = 'letteredIcon%s' % ( icon_number )
        gIcon = GIcon(name, image=img, iconsize=(20, 34))
        GMarker.__init__(self, geom=(report.point.x, report.point.y),
                         title=json.dumps(report.title, ensure_ascii=False)[1:-1], icon=gIcon)

    def __unicode__(self):
        "The string representation is the JavaScript API call."
        return mark_safe('GMarker(%s)' % ( self.js_params))


class GmapPoint(object):
    x = 0
    y = 0

    def __init__(self, point):
        self.__class__.x = point[0]
        self.__class__.y = point[1]


class FixMyStreetMap(GoogleMap):
    """
        Overrides the GoogleMap class that comes with GeoDjango.  Optionally,
        show nearby reports.
    """

    def __init__(self, pnt, draggable=False, nearby_reports=[]):
        # self.icons = []
        version = settings.GOOGLE_MAPS_API_VERSION
        markers = []
        center = (pnt.x, pnt.y)
        gIcon = GIcon("dragme",
                      image="/static/images/marker/default/marker.png",
                      iconsize=(29, 38))
        marker = GMarker(geom=(pnt.x, pnt.y), draggable=draggable, icon=gIcon)
        if draggable:
            event = GEvent('dragend', 'function(){}')
            marker.add_event(event)
        markers.append(marker)

        for i in range(len(nearby_reports)):
            nearby_marker = ReportMarker(nearby_reports[i], str(i + 1))
            markers.append(nearby_marker)

        GoogleMap.__init__(self, center=center, zoom=17, key=settings.GMAP_KEY, version=version,
                           markers=markers, dom_id='map_canvas', )


class WardMap(GoogleMap):
    """
        Show a single ward as a gmap overlay.  Optionally, show reports in the
        ward.
    """

    def __init__(self, ward, reports=[]):
        polygons = []
        for poly in ward.geom:
            polygons.append(GPolygon(poly))
        markers = []
        for i in range(len(reports)):
            marker = ReportMarker(reports[i], str(i + 1))
            markers.append(marker)

        GoogleMap.__init__(self, zoom=13, markers=markers, key=settings.GMAP_KEY, polygons=polygons,
                           dom_id='map_canvas')


class CityMap(GoogleMap):
    """
        Show all wards in a city as overlays.
    """

    def __init__(self, city):
        polygons = []
        kml_url = 'http://localhost:8000/media/kml/' + city.name + '.kml'

        ward = Ward.objects.filter(city=city)[:1][0]
        # for ward in Ward.objects.filter(city=city):
        #    for poly in ward.geom:
        #        polygons.append( GPolygon( poly ) )
        GoogleMap.__init__(self, center=ward.geom.centroid, zoom=13, key=settings.GMAP_KEY, polygons=polygons,
                           kml_urls=[kml_url], dom_id='map_canvas')


class GoogleAddressLookup(object):
    """
    Simple Google Geocoder abstraction - supports UTF8

    >>> doesnt_exist = GoogleAddressLookup("Foobar")
    >>> doesnt_exist.resolve()
    True
    >>> doesnt_exist.exists()
    False

    # Create test matches
    >>> single_match = GoogleAddressLookup("4691 Rue Garnier, Montreal Quebec")

    # Check existence
    >>> single_match.resolve()
    True
    >>> single_match.exists()
    True
    >>> single_match.matches_multiple()
    False
    >>> single_match.lat(0)
    '45.5320187'
    >>> single_match.lon(0)
    '-73.5789397'

    # multiple matches
    >>> multiple_matches = GoogleAddressLookup("Beaconsfield")
    >>> multiple_matches.resolve()
    True
    >>> multiple_matches.matches_multiple()
    True
    >>> multiple_matches.get_match_options()
    ['Beaconsfield, QC, Canada', 'Beaconsfield, Buckinghamshire, UK', 'Beaconsfield, St James, NB, Canada', 'Beaconsfield, Andover, NB, Canada', 'Beaconsfield, Norwich, ON, Canada', 'Beaconsfield, Annapolis, Subd. B, NS, Canada', 'Beaconsfield, Withernsea, East Riding of Yorkshire HU19 2, UK', 'Beaconsfield, Stirchley, Telford and Wrekin TF3 1, UK', 'Beaconsfield, Luton LU2 0, UK', 'Beaconsfield TAS, Australia']

    >>> utf8_match = GoogleAddressLookup(u'4691 Rue de Br\xe9beuf Montreal Canada')
    >>> utf8_match.resolve()
    True
    >>> utf8_match.exists()
    True
     """

    def __init__(self, address):
        self.query_results = []
        self.match_coords = []
        self.json_context = None
        self.url = iri_to_uri(
            u'http://maps.googleapis.com/maps/api/geocode/json?address=%s&sensor=false&region=ge' % (address))

    def resolve(self):
        try:
            resp = urllib.urlopen(self.url).read()
            self.json_context = json.loads(resp)
            self.query_results = []
            for r in self.json_context["results"]:
                loc = r["geometry"]["location"]
                self.query_results.append((loc["lng"], loc["lat"]))
            return ( True )
        except:
            return ( False )

    def exists(self):
        return len(self.query_results) != 0

    def matches_multiple(self):
        return len(self.query_results) > 1

    def lat(self, index):
        return str(self.query_results[index][1])

    def lon(self, index):
        return str(self.query_results[index][0])

    def get_match_options(self):
        addr_list = [r["formatted_address"] for r in self.json_context["results"]]
        return ( addr_list )


class SqlQuery(object):
    """
        This is a workaround: django doesn't support our optimized
        direct SQL queries very well.
    """

    def __init__(self):
        self.cursor = None
        self.index = 0
        self.results = None

    def next(self):
        self.index += 1

    def get_results(self):
        if not self.cursor:
            self.cursor = connection.cursor()
            self.cursor.execute(self.sql)
            self.results = self.cursor.fetchall()
        return self.results


class ReportCountQuery(SqlQuery):
    def name(self):
        return self.get_results()[self.index][5]

    def recent_new(self):
        return self.get_results()[self.index][0]

    def recent_fixed(self):
        return self.get_results()[self.index][1]

    def recent_updated(self):
        return self.get_results()[self.index][2]

    def old_fixed(self):
        return self.get_results()[self.index][3]

    def old_unfixed(self):
        return self.get_results()[self.index][4]

    def __init__(self, interval='1 month'):
        SqlQuery.__init__(self)
        self.base_query = """select count( case when age(clock_timestamp(), reports.created_at) < interval '%s' and reports.is_confirmed = True THEN 1 ELSE null end ) as recent_new,\
 count( case when age(clock_timestamp(), reports.fixed_at) < interval '%s' AND reports.status = 'fixed' THEN 1 ELSE null end ) as recent_fixed,\
 count( case when age(clock_timestamp(), reports.updated_at) < interval '%s' AND reports.status = 'not-fixed' AND reports.is_confirmed = True AND reports.updated_at != reports.created_at THEN 1 ELSE null end ) as recent_updated,\
 count( case when age(clock_timestamp(), reports.fixed_at) > interval '%s' AND reports.status = 'fixed' AND reports.is_confirmed = True THEN 1 ELSE null end ) as old_fixed,\
 count( case when age(clock_timestamp(), reports.created_at) > interval '%s' AND reports.is_confirmed = True AND reports.status = 'not-fixed' THEN 1 ELSE null end ) as old_unfixed
 """ % (interval, interval, interval, interval, interval)
        self.sql = self.base_query + " from reports where reports.is_confirmed = true"


class CityTotals(ReportCountQuery):
    def __init__(self, interval, city):
        ReportCountQuery.__init__(self, interval)
        self.sql = self.base_query
        self.sql += """ from reports left join wards on reports.ward_id = wards.id left join cities on cities.id = wards.city_id
        """
        self.sql += ' where reports.is_confirmed = True and city_id = %d ' % city.id
        print self.sql


class CityWardsTotals(ReportCountQuery):
    def __init__(self, city, lang):
        ReportCountQuery.__init__(self, "1 month")
        self.sql = self.base_query
        self.url_prefix = "/wards/"
        self.sql += ", wards.name_%s, wards.id, wards.number from wards " % lang  # Hack to link custom SQL with TransMeta
        self.sql += """left join reports on wards.id = reports.ward_id join cities on wards.city_id = cities.id join province on cities.province_id = province.id
        """
        self.sql += "and cities.id = " + str(city.id)
        self.sql += " group by  wards.name_%s, wards.id, wards.number order by wards.number" % (lang)

    def number(self):
        return self.get_results()[self.index][7]

    def get_absolute_url(self):
        return self.url_prefix + str(self.get_results()[self.index][6])


class AllCityTotals(ReportCountQuery):
    def __init__(self, lang):
        ReportCountQuery.__init__(self, "1 month")
        self.sql = self.base_query
        self.url_prefix = "/cities/"
        self.sql += ", cities.name_%s, cities.id, province.name_%s from cities " % (lang, lang)
        self.sql += """left join wards on wards.city_id = cities.id join province on cities.province_id = province.id left join reports on wards.id = reports.ward_id
        """
        self.sql += "group by cities.name_%s, cities.id, province.name_%s order by province.name_%s, cities.name_%s" % (
            lang, lang, lang, lang)

    def get_absolute_url(self):
        return self.url_prefix + str(self.get_results()[self.index][6])

    def province(self):
        return self.get_results()[self.index][7]

    def province_changed(self):
        if self.index == 0:
            return True
        return self.get_results()[self.index][7] != self.get_results()[self.index - 1][7]


class FaqEntry(models.Model):
    __metaclass__ = TransMeta

    q = models.CharField(max_length=100)
    a = models.TextField(blank=True, null=True)
    slug = models.SlugField(null=True, blank=True)
    order = models.IntegerField(null=True, blank=True)

    def save(self):
        super(FaqEntry, self).save()
        if self.order == None:
            self.order = self.id + 1
            super(FaqEntry, self).save()

    class Meta:
        db_table = u'faq_entries'
        translate = ('q', 'a', )


class FaqMgr(object):
    def incr_order(self, faq_entry):
        if faq_entry.order == 1:
            return
        other = FaqEntry.objects.get(order=faq_entry.order - 1)
        swap_order(other[0], faq_entry)

    def decr_order(self, faq_entry):
        other = FaqEntry.objects.filter(order=faq_entry.order + 1)
        if len(other) == 0:
            return
        swap_order(other[0], faq_entry)

    def swap_order(self, entry1, entry2):
        entry1.order = entry2.order
        entry2.order = entry1.order
        entry1.save()
        entry2.save()


class PollingStation(models.Model):
    """
    This is a temporary object.  Sometimes, we get maps in the form of
    polling stations, which have to be combined into wards.
    """
    number = models.IntegerField()
    ward_number = models.IntegerField()
    city = models.ForeignKey(City)
    geom = models.MultiPolygonField(null=True)
    objects = models.GeoManager()

    class Meta:
        db_table = u'polling_stations'

from .receivers import *