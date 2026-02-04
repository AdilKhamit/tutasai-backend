from django.urls import include, path

from core import views

urlpatterns = [
    path("", include(views.router.urls)),
    path("dashboard/committee/", views.CommitteeDashboardView.as_view(), name="committee-dashboard"),
]
