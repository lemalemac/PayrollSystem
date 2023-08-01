from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.contrib.sitemaps.views import sitemap

urlpatterns = [
  path("login/", views.login_user, name="login"),
]
