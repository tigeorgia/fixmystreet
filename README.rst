This is the code for https://www.chemikucha.ge

===============
Installation
===============
1. `Install Geodjango <https://docs.djangoproject.com/en/1.7/ref/contrib/gis/install/>`_ with the geospatial libraries (GEOS, PROJ.4, GDAL, PostGIS)
2. Create the database with postgis support. http://postgis.net/install/
3. Clone this repository - ``git clone git@github.com:tigeorgia/fixmystreet.git``
4. Install requirements inside your virtualenv - ``pip install -r requirements.txt``
5. Migrate apps by running ``./manage.py migrate``
6. Create your superuser account - ``./manage.py createsuperuser``
7. Copy ``local_settings_example.py`` to ``local_settings.py`` and configure your database

