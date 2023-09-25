from django.urls import path
from . import views

app_name="feed"

urlpatterns = [
    path("", views.HomepageView.as_view(), name="index")
]