from django.urls import path
from . import views

app_name =  "profiles"

urlpatterns = [
    path("<str:username>/", views.ProfileDetailView.as_view(), name="detail"),
    path("<str:username>/follow", views.FollowView.as_view(), name="follow"),
    path("<int:pk>/myprofile", views.MyProfileView.as_view(), name="myprofile"),
    path("users", views.UsersView.as_view(), name="users"),
]