from django import forms
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
from django.utils.translation import get_language, ugettext_lazy as _

from apps.mainapp.models import Report, ReportUpdate, ReportSubscriber, ReportCategory
from apps.users.models import FMSUser, FMSUserValidators

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
    error_messages = {
        'login_required': _('You need to be logged in to post an update'),
        'no_permissions': _('Only city councillors and report creators can update report status')
    }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.report = kwargs.pop('report', None)
        super(ReportUpdateForm, self).__init__(*args, **kwargs)

    class Meta:
        model = ReportUpdate
        fields = ('desc', 'photo', 'status')

    def clean(self):
        clean_data = super(ReportUpdateForm, self).clean()
        status = clean_data['status']
        if not self.user.is_authenticated():
            raise forms.ValidationError(self.error_messages['login_required'], code='login_required')
        if status != self.report.status:
            if not (self.user.is_councillor or self.user == self.report.user):
                raise forms.ValidationError(self.error_messages['no_permissions'], code='no_permissions')
        return clean_data


class ReportSubscriberForm(forms.ModelForm):
    class Meta:
        model = ReportSubscriber
        fields = ('email',)


class ReportForm2(forms.ModelForm):
    """
    2nd step of form submission
    """
    category = forms.ModelChoiceField(queryset=ReportCategory.objects.all().order_by('name_' + get_language()[:2]),
                                      label=_('Category'))

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.user_validators = FMSUserValidators()
        super(ReportForm2, self).__init__(*args, **kwargs)
        # We don't need user creation fields if user is already logged in
        if not self.user.is_authenticated():
            self.fields['username'] = forms.CharField(label=_('Username'), max_length=30)
            self.fields['password1'] = forms.CharField(widget=forms.PasswordInput, label=_('Password'),)
            self.fields['password2'] = forms.CharField(widget=forms.PasswordInput, label=_('Repeat Password'))

    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        username = self.cleaned_data.get('username')
        self.user_validators.validate_passwords(password1, password2)
        self.user_validators.validate_username(username)
        return self.cleaned_data

    class Meta:
        model = Report
        fields = ('desc', 'photo', 'category')


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

    first_name = forms.CharField(required=False,
                                 widget=forms.TextInput(
                                     attrs={
                                         'class': 'required form-control input-small user-hidden',
                                         'placeholder': _("First Name")
                                     }))

    last_name = forms.CharField(required=False,
                                widget=forms.TextInput(
                                    attrs={
                                        'class': 'required form-control input-small user-hidden',
                                        'placeholder': _("Last Name")
                                    }))

    phone = forms.CharField(required=False,
                            widget=forms.TextInput(
                                attrs={
                                    'class': 'required form-control input-small user-hidden',
                                    'placeholder': _("Phone Number")
                                }))
    email = forms.EmailField(required=False,
                             widget=forms.TextInput(
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
