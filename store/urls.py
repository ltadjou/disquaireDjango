from django.conf.urls import url 
from . import views # import views so we can use then in urls

urlpatterns = [
    url(r'^$', views.listing, name="listing"), # Toute url qui commcence ou se termine par une  chaîne vide "/store will call the method "index" in "views.py"
    url(r'^(?P<album_id>[0-9]+)/$', views.detail, name="detail"),#url(r'^search/\?query=(?P<query>[A-Z][a-z]+)/$', views.)
    url(r'^search/$', views.search, name = "search")
]

