from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from mainapp.models import Report, ReportUpdate, Ward, FixMyStreetMap, ReportCountQuery, City, FaqEntry, GoogleAddressLookup
from django.template import Context, RequestContext
from django.contrib.gis.measure import D 
from django.contrib.gis.geos import *
import settings
from django.utils.translation import ugettext as _
from django.utils.http import urlquote
from django.utils.encoding import iri_to_uri
from mainapp.views.cities import home as city_home
import logging
import os
import urllib
from olwidget.widgets import Map, EditableLayer, InfoLayer


def home(request, error_msg = None, disambiguate=None): 
    if request.subdomain:
        matching_cities = City.objects.filter(name__iexact=request.subdomain)
        if matching_cities:
            return( city_home(request, matching_cities[0], error_msg, disambiguate ) )
            
    reports_with_photos = Report.objects.filter(is_confirmed=True).exclude(photo='').order_by("-created_at")[:3]
    recent_reports = Report.objects.filter(is_confirmed=True).order_by("-created_at")[:5]
        
    return render_to_response("home.html",
                {"report_counts": ReportCountQuery('1 year'),
                 "cities": City.objects.all(),
                 "reports_with_photos": reports_with_photos,
                 "recent_reports": recent_reports , 
                 'error_msg': error_msg,
                 'disambiguate':disambiguate },
                context_instance=RequestContext(request))    


def search_address(request):
    if request.method == 'POST':
        address = iri_to_uri(u'/search?q=%s' % request.POST["q"])
        return HttpResponseRedirect( address )
        #address = urllib.urlencode({'x':urlquote(request.POST["q"])})[2:]
        #return HttpResponseRedirect("/search?q=" + address )

    address = request.GET["q"] 
    address_lookup = address 

    if address == '8':
        lon = 44.922294596002
        lat = 41.688166794582
    elif address == '9':
        lon = 44.745675450098
        lat = 41.714791286274
    elif address == '10':
        lon = 44.821181771768
        lat = 41.791573324918
    elif address == '11':
        lon = 44.749838791985
        lat = 41.676073592951
    elif address == '12':
        lon = 44.777475720192
        lat = 41.749283573879
    elif address == '13':
        lon = 44.80153927177
        lat = 41.694033197126
    else:
        lon = 0 # In case someone puts in something else. -DD
        lat = 0

    '''    if not address_lookup.resolve():
        return index(request, _("Sorry, we couldn\'t retrieve the coordinates of that location, please use the Back button on your browser and try something more specific or include the city name at the end of your search."))

    if not address_lookup.exists():
        return index( request, _("Sorry, we couldn\'t find the address you entered.  Please try again with another intersection, address or postal code, or add the name of the city to the end of the search."))

    if address_lookup.matches_multiple() and not request.GET.has_key("index"):
        addrs = address_lookup.get_match_options() 
        addr_list = "" 
        for i in range(0,len(addrs)):
            link = "/search?q=" + urlquote(address) + "&index=" + str(i)
            addr_list += "<li><a href='%s'>%s</a></li>" % ( link, addrs[i] )
            addr_list += "</ul>"
        return index(request,disambiguate = addr_list )'''

    # otherwise, we have a specific match
    match_index = 0
    if request.GET.has_key("index"):
        match_index = int(request.GET["index"])

    point_str = "POINT("+ str(lon) +" "+ str(lat) +")"
    pnt = fromstr(point_str, srid=4326)    
    wards = Ward.objects.filter(geom__contains=point_str)
    if (len(wards) == 0):
        return( index(request, _("Sorry, we don't yet have that area in our database.  Please have your area councillor contact fixmystreet.ca.")))

    reports = Report.objects.filter(is_confirmed = True,point__distance_lte=(pnt,D(km=1))).distance(pnt).order_by('distance')
#    gmap = FixMyStreetMap(pnt,True,reports)
    ward = wards[0]
    wardBoundary = InfoLayer([[ward.geom,"Boundary"]],{
                            'overlay_style': {
                                'fillColor': '#FFFFFF',
                                'fill_opacity': 0,
                                'stroke_color': '#0000FF',
                                'stroke_width': 2,}})

    reportPoint = EditableLayer({ 'name': 'report-point',
                            'overlay_style': {
                                'externalGraphic': '/media/images/marker/default/marker.png',
                                'pointRadius': '15',
                                'graphicOpacity': '1'}})
    reportsOld = Report.objects.filter( ward = ward, is_confirmed = True ).extra( select = { 'status' : """
        CASE 
        WHEN age( clock_timestamp(), created_at ) < interval '1 month' AND is_fixed = false THEN 'New Problems'
        WHEN age( clock_timestamp(), created_at ) > interval '1 month' AND is_fixed = false THEN 'Older Unresolved Problems'
        WHEN age( clock_timestamp(), fixed_at ) < interval '1 month' AND is_fixed = true THEN 'Recently Fixed'
        WHEN age( clock_timestamp(), fixed_at ) > interval '1 month' AND is_fixed = true THEN 'Old Fixed'
        ELSE 'Unknown Status'
        END """,
        'status_int' : """
        CASE 
        WHEN age( clock_timestamp(), created_at ) < interval '1 month' AND is_fixed = false THEN 0
        WHEN age( clock_timestamp(), created_at ) > interval '1 month' AND is_fixed = false THEN 1
        WHEN age( clock_timestamp(), fixed_at ) < interval '1 month' AND is_fixed = true THEN 2
        WHEN age( clock_timestamp(), fixed_at ) > interval '1 month' AND is_fixed = true THEN 3
        ELSE 4
        END """ }, order_by = ['status_int'] )
    counter = 1
    allLayers = [wardBoundary, reportPoint] 
    for r in reportsOld:
        if r.is_fixed:
            markerColor = 'green'
        else:
            markerColor = 'red'	
        options = {'overlay_style': {
        'externalGraphic': '/media/images/marker/%s/marker%d.png' %(markerColor, counter),
        'pointRadius': '15',
        'graphicOpacity': '1',}}
        counter+=1
        thisLayer = InfoLayer([(r.point,r.title)],options)
        allLayers.append(thisLayer)	
    olMap = Map(vector_layers=allLayers,
                options={'layers': ['osm.omc'],
                         'map_div_style':{'width': '400px', 'height': '400px'},
                         'map_options': {'controls': ['Navigation', 'PanZoom', 'Attribution'] },
                         'zoom_to_data_extent':False, 
                         'default_zoom':14, 
                         'default_lat':pnt.y, 
                         'default_lon':pnt.x,},
                layer_names=[None,"report-point"],
                template="multi_layer_map.html",
                params={'point':pnt})   
    return render_to_response("search_result.html",
                {"lat": pnt.y,
                 "lon": pnt.x,
                 "olMap": olMap,
                 "pnt": pnt,
                 "enable_map": True,
                 "ward" : wards[0],
                 "reports" : reports, },
                 context_instance=RequestContext(request))

def about(request):
   return render_to_response("about.html",{'faq_entries' : FaqEntry.objects.all().order_by('order')},
                context_instance=RequestContext(request))    
