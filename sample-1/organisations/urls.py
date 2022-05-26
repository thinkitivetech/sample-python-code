from django.urls import path

from . import views

app_name = "organisations"
urlpatterns = [
    path("list/", views.list, name="list"),
    path("report/<str:organisation_id>", views.report, name="report"),
]
