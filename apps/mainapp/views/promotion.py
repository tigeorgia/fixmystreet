from django.template import RequestContext
from django.shortcuts import render_to_response

from apps.mainapp.models import Report


def show(request, promo_code):
    matchstr = "author LIKE '%%" + promo_code + "%%'"
    reports = Report.active.extra(select={'match': matchstr }).order_by('created_at')[0:100]
    count = Report.objects.filter(author__contains=promo_code).count()
    return render_to_response("promotions/show.html",
                {   "reports": reports,
                    "promo_code":promo_code,
                    "count": count },
                context_instance=RequestContext(request))

