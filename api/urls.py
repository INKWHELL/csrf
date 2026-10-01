from django.urls import path
from .views import login_view, csrf_view, change_email_view

urlpatterns = [
    path("api/login/", login_view),
    path("api/csrf/", csrf_view),
    path("api/account/email/", change_email_view),
]
