from django.conf.urls import url
from forum.views import *

urlpatterns = [
    url(r'^$', CategoryView.as_view(), name="home"),
    url(r'^(?P<slug>[A-Za-z0-9\-]+)$', ThreadView.as_view(), name= "category_name"),
    url(r'^thread/(?P<slug>[A-Za-z0-9\-]+)-(?P<pk>[0-9]+)$', PostView.as_view()),
]