# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from django.conf.urls import url
from app import views

urlpatterns = [

    # The home page
    path('', views.index, name='home'),
    path('reload', views.index2),
    path('refresh', views.index),
   path('upload-csv/', views.upload_csv, name='upload_csv'),

    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]
