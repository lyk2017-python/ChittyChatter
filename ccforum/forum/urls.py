from django.conf.urls import url
from forum.views import *

urlpatterns = [
    url(r'^$', CategoryView),
    url(r'^category/(?P<slug>[A-Za-z0-9\-]+)$', ThreadView),
    url(r'^thread/(?P<slug>[A-Za-z0-9\-]+)-(?P<pk>[0-9]+)$', PostView),
]