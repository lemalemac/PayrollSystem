from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.contrib.sitemaps.views import sitemap

urlpatterns = [
  path("", views.app, name="app"),
  path("login/", views.login_user, name="login"),
  path("create/", views.create_user, name="create"),
  path("modify/", views.modify, name="modify"),
  path("search/", views.search, name="search"),
  path("delete/", views.delete, name="delete"),
  path('employee/<str:employee_id>/', views.employee_details_view, name='employee_details'),
]
