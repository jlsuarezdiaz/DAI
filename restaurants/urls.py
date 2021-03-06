# restaurantes/urls.py

from django.conf.urls import url
from django.http import HttpResponseRedirect


from . import views

urlpatterns = [
  url(r'^$', views.restaurants, name='restaurants'),
  url(r'^query/$', views.query_restaurants, name='query_restaurants'),
  url(r'^search/$',views.search_restaurant, name='search_restaurant'),
  url(r'^new/$',views.new_restaurant, name='new_restaurant'),
  url(r'^edit/$',lambda r: HttpResponseRedirect('/restaurants/'),name='edit_restaurant'),
  url(r'^edit/(.*)/$',views.edit_restaurant,name='edit_restaurant_x'),
  url(r'^remove/$',views.remove_restaurant,name='remove_restaurant'),
  url(r'^mapview/$',views.view_restaurant,name='view_restaurant'),
  url(r'^stats/$',views.stats_restaurants,name='stats_restaurants'),
  url(r'^stats/query$',views.stats_query,name='stats_query'),
  url(r'^football/$',views.football,name='football'),
  url(r'^football/add/$',views.football_add,name='football_add'),
  url(r'^football/remove/$',views.football_remove,name='football_remove'),
  url(r'^football/get/$',views.football_get,name='football_get'),
  url(r'^football/addkey/$',views.football_addkey,name='football_addkey'),
  url(r'^football/removekey/$',views.football_removekey,name='football_removekey')
]