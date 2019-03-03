from django.urls import path

from . import views

urlpatterns = [
    path('receipt/<int:receipt_id>', views.getReceipt, name="getreceipt"),
    path('receipt/create', views.createReceipt, name="postreceipt"),
    # path("/receipt/create/<int:receipt_id>", views.updateReceipt, name="updatereceipt"),
    # path("/receipt/delete/<int:receipt_id>", views.deleteReceipt, name="deletereceipt"),
    # path('/profile/<int:profile_id>', views.getProfile, name="getprofile"),
    # path('/profile/create', views.createProfile, name="postprofile"),
    # path("/profile/create/<int:profile_id>", views.updateProfile, name="updateprofile"),
    # path("/profile/delete/<int:profile_id>", views.deleteProfile, name="deleteprofile"),
    # path('/group/<int:group_id>', views.getGroup, name="getgroup"),
    # path('/group/create', views.createGroup, name="postgroup"),
    # path("/group/create/<int:group_id>", views.updateGroup, name="updategroup"),
    # path("/group/delete/<int:group_id>", views.deleteGroup, name="deletegroup")
]