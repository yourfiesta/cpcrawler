
from django.conf.urls import url
from . import views

urlpatterns = [
    url('tables/', views.crawl_main, name='crawl_main'),
    url('charts/', views.crawl_main_c, name='crawl_main_c'),
    url('index/', views.crawl_main_d, name='crawl_main_d'),
    url(r'^$', views.test, name='test'),
    url(r'^getJsonData/$', views.getJsonData, name='getJsonData'),
]

