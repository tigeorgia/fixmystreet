from django import forms
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.admin.widgets import AdminDateWidget
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import get_object_or_404

from apps.mainapp.models import Report, ReportUpdate, ReportSubscriber, VerifiedAuthor


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100,
                           widget=forms.TextInput(attrs={'class': 'form-control required', 'placeholder': _('Name')}),
                           label="")
    email = forms.EmailField(widget=forms.TextInput(attrs=dict({'class': 'form-control required',
                                                                'placeholder': _('Email')},
                                                               maxlength=200)),
                             label="")
    body = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control form-margin-fix required', 'rows': '5', 'cols': '20',
                                     'placeholder': _('Message')}),
        label="")

    def save(self, fail_silently=False):
        message = render_to_string("emails/contact/message.txt", self.cleaned_data)
        send_mail('FixMyStreet.ge User Message from %s' % self.cleaned_data['email'], message,
                  settings.EMAIL_FROM_USER, [settings.ADMIN_EMAIL], fail_silently=False)


class ReportUpdateForm(forms.ModelForm):
    def __init__(self, report_id=None, *args, **kwargs):
        self.report_id = report_id
        super(ReportUpdateForm, self).__init__(*args, **kwargs)

    class Meta:
        model = ReportUpdate
        fields = ('desc', 'photo', 'status')

    def clean(self):
        clean_data = super(ReportUpdateForm, self).clean()
        status = self.cleaned_data.get('status')

        return clean_data


class ReportSubscriberForm(forms.ModelForm):
    class Meta:
        model = ReportSubscriber
        fields = ('email',)


class ReportForm2(forms.ModelForm):
    class Meta:
        model = Report
        fields = ('desc', 'photo')


class ReportForm1(forms.Form):
    title = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'required form-control input-small',
            'placeholder': _("Problem Title")
        }))

    street = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'required form-control input-small',
            'placeholder': _("Street")
        }))

    first_name = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'required form-control input-small user-hidden',
            'placeholder': _("First Name")
        }))

    last_name = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'required form-control input-small user-hidden',
            'placeholder': _("Last Name")
        }))

    phone = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'required form-control input-small user-hidden',
            'placeholder': _("Phone Number")
        }))
    email = forms.EmailField(widget=forms.TextInput(
        attrs={
            'class': 'required form-control input-small user-hidden',
            'placeholder': _("Email"),
            'type': 'hidden',
        }))
    lon = forms.CharField(widget=forms.TextInput(attrs={'class': 'required', 'type': 'hidden'}))
    lat = forms.CharField(widget=forms.TextInput(attrs={'class': 'required', 'type': 'hidden'}))


class sortingForm(forms.Form):
    CHOICES = (('-created_at', _('Created descending')),
               ('created_at', _('Created ascending')),
               ('-sub_count', _('Most subscribers')),
    )
    sorting = forms.ChoiceField(required=False, widget=forms.RadioSelect(attrs={'class': ''}), choices=CHOICES)
