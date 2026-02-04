from django.urls import include, path

from core import views

urlpatterns = [
    path("", include(views.router.urls)),
    path("dashboard/committee/", views.CommitteeDashboardView.as_view(), name="committee-dashboard"),
    path("dashboard/inspector/", views.InspectorDashboardView.as_view(), name="inspector-dashboard"),
    path("protocols/<int:work_card_id>/generate/", views.GenerateProtocolView.as_view(), name="generate-protocol"),
    path("protocols/<int:protocol_id>/sign/", views.SignProtocolView.as_view(), name="sign-protocol"),
]
