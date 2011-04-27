from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from mainapp.models import Report, ReportUpdate, Ward, FixMyStreetMap, ReportCategory
from mainapp.forms import ReportForm,ReportUpdateForm
from django.template import Context, RequestContext
from django.contrib.gis.geos import *
from fixmystreet import settings
from django.utils.translation import ugettext as _
from olwidget.widgets import Map, InfoLayer, EditableLayer
from django.contrib.gis.measure import D 

def new( request ):
    category_error = None

    if request.method == "POST":
        point_str = "POINT(" + request.POST["lon"] + " " + request.POST["lat"] + ")"
        pnt = fromstr(point_str, srid=4326)         
        f = request.POST.copy()
        update_form = ReportUpdateForm( {'email':request.POST['email'], 'desc':request.POST['desc'],
                                         'author':request.POST['author'], 'phone': request.POST['phone']})    
        report_form = ReportForm({'title' : request.POST['title']}, request.FILES)
        
        # this is a lot more complicated than it has to be because of the infortmation
        # spread across two records.
        
        if request.POST['category_id'] != "" and update_form.is_valid() and report_form.is_valid():
            report = report_form.save( commit = False )
            report.point = pnt
            report.category_id = request.POST['category_id']
            report.author = request.POST['author']
            report.desc = request.POST['desc']
            report.ward = Ward.objects.get(geom__contains=pnt)
            report.save()
            update = update_form.save(commit=False)
            update.report = report
            update.first_update = True
            update.created_at = report.created_at
            update.save()
            return( HttpResponseRedirect( report.get_absolute_url() ))
        
         # other form errors are handled by the form objects.
        if not request.POST['category_id']:
            category_error = _("Please select a category")
            
    else:
        point_str = "POINT(" + request.GET["lon"] + " " + request.GET["lat"] + ")"
        pnt = fromstr(point_str, srid=4326)
        report_form = ReportForm()
        update_form = ReportUpdateForm()

    wards = Ward.objects.filter(geom__contains=point_str)
    if (len(wards) == 0):
        return( index(request, _("Sorry, we don't yet have that area in our database.  Please have your area councillor contact FixMyStreet.ge.")))
    
    ward = wards[0]
    wardBoundary = InfoLayer([[ward.geom,"Boundary"]],{
        'overlay_style': {
            'fill_color': '#FFFFFF',
            'fill_opacity':0,
            'stroke_color': '#0000FF',
            'stroke_width': 2,}})

    reportPoint = EditableLayer({ 'name': 'report-point',
        'overlay_style': {
            'externalGraphic': '/media/images/marker/default/marker.png',
            'pointRadius': '15',
            'graphicOpacity': '1'}})
    allLayers = [wardBoundary,reportPoint]

    if request.LANGUAGE_CODE == 'ka':
        map_lang = 'osm.omcka'
    else:
        map_lang = 'osm.omcen'
    
    olMap = Map(vector_layers=allLayers,options={'layers': [map_lang],'map_div_style':{'width': '400px', 'height': '400px'},'map_options': {'controls': ['Navigation', 'PanZoom']},'default_zoom': 15, 'default_lat':pnt.y, 'default_lon':pnt.x, 'zoom_to_data_extent': False},layer_names=[None,"report-point"],template="multi_layer_map.html",params={'point':pnt}, )
    
    return render_to_response("reports/new.html",
                { "lat": pnt.y,
                  "lon": pnt.x,
                  "pnt": pnt,
                  "olMap": olMap,
                  "categories": ReportCategory.objects.all().order_by("category_class"),
                  "report_form": report_form,
                  "update_form": update_form, 
                  "category_error" : category_error, },
                context_instance=RequestContext(request))
    
def show( request, report_id ):
    report = get_object_or_404(Report, id=report_id)
    subscribers = report.reportsubscriber_set.count() + 1
# OpenLayers Support -DD
    reportLayer = InfoLayer([(report.point,report.title)],{
        'overlay_style': {
				'externalGraphic': '/media/images/marker/default/marker.png',
				'pointRadius': '15',
				'graphicOpacity': '1',
			        #'fill_color': '#ffffff',
				#'stroke_color': '#008800',
				}})

    if request.LANGUAGE_CODE == 'ka':
        map_lang = 'osm.omcka'
    else:
        map_lang = 'osm.omcen'
    olMap = Map([reportLayer],options={
        'layers': [map_lang],
		'map_div_style':{'width': '400px', 'height': '400px'},
        'map_options': {'controls': ['Navigation', 'PanZoom', 'Attribution'] },
        'default_zoom': 1})

    return render_to_response("reports/show.html",
                { "report": report,
                  "subscribers": subscribers,
                  "ward":report.ward,
                  "updates": ReportUpdate.objects.filter(report=report, is_confirmed=True).order_by("created_at")[1:], 
                  "update_form": ReportUpdateForm(), 
                  "google":  FixMyStreetMap((report.point)), 
                  "olMap": olMap },
                context_instance=RequestContext(request))

def poster ( request, report_id ):
    # Build URL
    report = get_object_or_404(Report,id=report_id)
    url = request.get_host()+request.path[:-7] # Hard-coded value to trim "/poster" off the end. Sorry.
    return render_to_response("reports/poster.html", { 'url': url, 'report':report})
