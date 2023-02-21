from django.contrib import admin
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from django.conf.urls.static import static
from django.conf import settings
from . import views, settings as s


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),

    path('', views.index, name='index'),

    path('upload/', views.uploadFile, name='upload'),
    path('read/<str:file_name>/', views.readFile, name='read_file'),
    path('read/<str:file_name>/<str:username>/', views.readUserFile, name='read_user_file'),
    path('delete/<str:file_name>/', views.deleteFile, name='delete_file'),
    path('tag/<str:tag_name>/', csrf_exempt(views.addTag), name='add_tag'),
    path('search/', views.searchFile, name='search'),
    path('compare/<str:file_name>/', views.compare, name='compare'),
]

if not s.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Change Some Default Admin Text
admin.site.site_header = 'Read Text Data'
admin.site.index_title = 'Welcome to read text data'
admin.site.site_title = 'Read Text Data'




# from django.contrib import admin
# from django.urls import path
# from django.views.decorators.csrf import csrf_exempt
# from django.conf.urls.static import static
# from django.conf import settings
# from . import views, settings as s


# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('login/', views.login, name='login'),
#     path('logout/', views.logout, name='logout'),

#     path('', views.index, name='index'),

#     path('upload/', views.uploadFile, name='upload'),
#     path('read/<str:file_name>/', views.readFile, name='read_file'),
#     path('read/<str:file_name>/<str:username>/', views.readUserFile, name='read_user_file'),
#     path('delete/<str:file_name>/', views.deleteFile, name='delete_file'),
#     path('tag/<str:tag_name>/', csrf_exempt(views.addTag), name='add_tag'),
#     path('search/', views.searchFile, name='search'),
#     path('compare/<str:file_name>/', views.compare, name='compare'),
# ]

# if not s.DEBUG:
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# # Change Some Default Admin Text
# admin.site.site_header = 'Read Text Data'
# admin.site.index_title = 'Welcome to read text data'
# admin.site.site_title = 'Read Text Data'