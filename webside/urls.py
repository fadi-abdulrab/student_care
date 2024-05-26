from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from . import views
from student_management_system import settings

app_name = 'webside'

urlpatterns = [
    path('', views.index, name="wibside_index"),
    path('Blog/', views.Blogs, name="Blog"),
    path('Contact/', views.Contact, name="Contact"),


 
]
