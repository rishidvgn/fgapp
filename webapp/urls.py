"""webapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib import admin
from django.urls import path
from fgapp.views import home,login,logout, upload, upload_to_model,viewfg,kam_comm,kam_des_date
from fgapp.views import kam_summary,cus_summary,kam_det, kam_des_adv, overall_filter,cus_det
urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', home),
    path('login/', login),
    path('logout/', logout),
    path('upload/', upload),
    path('upload_model/', upload_to_model),
    path('listview/', viewfg),
    path('kam_comm/', kam_comm),
    path('kam_des_date/', kam_des_date),
    path('kam_des_adv/', kam_des_adv),
    path('kam_sum/', kam_summary),
    path('cus_sum/', cus_summary),
    path('overall_filter/', overall_filter),
    path('kam_det/', kam_det),
    path('cus_det/', cus_det),
    path('', home),


]
