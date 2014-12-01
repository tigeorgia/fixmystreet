from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from apps.mainapp.models import FaqEntry


def show( request, slug ):
    faq = get_object_or_404(FaqEntry, slug=slug)
    return render_to_response("faq/show.html",
                {"faq_entry":faq },
                 context_instance=RequestContext(request))

