from django.urls import path, include, register_converter
from rest_framework import routers

from api import views


router = routers.DefaultRouter()
router.register('survivors', views.SurvivorList, 'suvivors')
router.register('report-contamination', views.ReportInfectedView, 'infected-reports')

urlreports = [
    path('infected/', views.InfectedReportsView.as_view(), name='report-infected'),
    path('uninfected/', views.UninfectedReportsView.as_view(), name='report-uninfected'),
    path('avg-resources/', views.AverageResourcesView.as_view(), name='avg-resources'),
    path('lost-points/', views.LostPointsView.as_view(), name='lost-points')
]

urlpatterns = [
    path('', include(router.urls)),
    path('trades/', views.TradeView.as_view(), name='trade'),
    path('reports/', include(urlreports)),
]