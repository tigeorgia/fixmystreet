{% autoescape off %}{% block vars %}var map;{% endblock %}
{% block functions %}{% endblock %}
{% block load %}function {{ load_func }}(){
  if (GBrowserIsCompatible()) {
  	alert("Maps template called");
  }else {
    alert("Sorry, the Google Maps API is not compatible with this browser.");
  }
}
{% endblock %}{% endautoescape %}
