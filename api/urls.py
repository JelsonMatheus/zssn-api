from django.urls import path, include
from rest_framework import routers

from api import views


router = routers.DefaultRouter()
router.register('survivors', views.SurvivorList, 'suvivors')
router.register('infected-reports', views.ReportInfectedView, 'infected-reports')

urlpatterns = [
    path('', include(router.urls)),
    path('trades/', views.TradeView.as_view(), name='trade'),
]