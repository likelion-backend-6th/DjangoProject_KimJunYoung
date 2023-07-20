from django.urls import path, re_path

from . import views

app_name = 'blog'

urlpatterns = [
	# path('', views.post_list, name='post_list'),
	path('', views.PostListView.as_view(), name='post_list'),
	# path('<int:year>/<int:month>/<int:day>/<str:post>/', views.post_detail, name='post_detail'),
	re_path(r'^(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/(?P<day>[0-9]{1,2})/(?P<post>[-\w]+)/$', views.post_detail,
																								 name='post_detail'),
	path('<int:post_id>/share/', views.post_share, name='post_share'),
	path('<int:post_id>/comment/', views.post_comment, name='post_comment'),

]

# r'^post/(?P<slug>[-\w]+)/$'