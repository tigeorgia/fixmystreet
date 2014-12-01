from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect

from apps.mainapp.forms import ContactForm


def thanks(request):
     return render_to_response("contact/thanks.html", {},
                context_instance=RequestContext(request))

def new(request):
    if request.method == 'POST':
        form = ContactForm(data=request.POST, auto_id=False)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('contact_thanks'))
    else:
        form = ContactForm()

    return render_to_response("contact/new.html",
                              { 'contact_form': form },
                              context_instance=RequestContext(request))
