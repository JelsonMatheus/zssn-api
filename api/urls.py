from django.urls import path, include
from rest_framework import routers

from api import views


router = routers.DefaultRouter()
router.register('survivor', views.SurvivorList, 'suvivor')
router.register('infected-report', views.ReportInfectedView, 'infected-report')

urlpatterns = [
    path('', include(router.urls)),
]

