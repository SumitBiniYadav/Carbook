"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from. import views

urlpatterns = [
    path('index/',views.index,name='index'),
    path('signup/',views.signup,name='signup'),
    path('add/',views.add,name='add'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('changepass/',views.changepass,name='changepass'),
    path('lchangepass/',views.lchangepass,name='lchangepass'),
    path('fpass/',views.fpass,name='fpass'),
    path('otp/',views.otp,name='otp'),
    path('newpass/',views.newpass,name='newpass'),
    path('uprofile/',views.uprofile,name='uprofile'),
    path('luprofile/',views.luprofile,name='luprofile'),
    path('lindex/',views.lindex,name='lindex'),
    path('pricing/',views.pricing,name='pricing'),
    path('lpricing/',views.lpricing,name='lpricing'),
    path('about/',views.about,name='about'),
    path('success/',views.success,name='success'),
    path('labout/',views.labout,name='labout'),
    path('services/',views.services,name='services'),
    path('car/',views.car,name='car'),
    path('lcar/',views.lcar,name='lcar'),
    path('details/<int:pk>',views.details,name='details'),
    path('idetails/<int:pk>',views.idetails,name='idetails'),
    path('updatee/<int:pk>',views.updatee,name='updatee'),
    path('delete/<int:pk>',views.delete,name='delete'),
    path('cart/<int:pk>',views.cart,name='cart'),
    path('summary/<int:pk>',views.summary,name='summary'),
    path('mybooking/',views.mybooking,name='mybooking'),
    path('bookdetail/<int:booking_id>',views.bookdetail,name='bookdetail'),
    path('bookreq/',views.bookreq,name='bookreq'),
    path('approve_req/',views.approve_req,name='approve_req'),
    path('decline_req/',views.decline_req,name='decline_req'),
    path('earning/',views.earning,name='earning'),
    path('download-invoice/<int:booking_id>/', views.download_invoice, name='download_invoice'),

]   
