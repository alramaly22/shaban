from django.urls import path

from . import views

app_name = "coaching"

urlpatterns = [
    path("", views.home, name="home"),
    path("checkout/<slug:slug>/", views.checkout, name="checkout"),
    path("confirmation/<uuid:order_id>/", views.confirmation, name="confirmation"),
    path("contact/", views.contact, name="contact"),
    path("privacy-policy/", views.privacy_policy, name="privacy_policy"),
    path("refund-policy/", views.refund_policy, name="refund_policy"),
    path("terms-and-conditions/", views.terms_and_conditions, name="terms"),
]
