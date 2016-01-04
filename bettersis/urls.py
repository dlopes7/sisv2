from django.conf.urls import url

from bettersis import views

urlpatterns = [
    url(r'^$', views.chart, name='chart'),
    url(r'^json_chart/$', views.json_chart, name='json_chart'),
    url(r'^host_list/$', views.view_host_list, name='host_list'),

]