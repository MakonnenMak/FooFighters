from django.urls import path

from . import views

urlpatterns = [
    path('getdata/<int:re_id>', views.getData, name="getdata"),
    path('getall/<str:email>', views.getallreceipts, name="getallreceipts"),
    path('senddata/<str:email>', views.sendData, name="senddata"),
    # path('updatedata', views.updateData, name="updatedata")
]