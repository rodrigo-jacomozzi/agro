from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from producer.views import ProducerViewSet, DashboardDataViewSet

router = DefaultRouter()
router.register(r'producers', ProducerViewSet, basename='producer')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('dashboard-data/', DashboardDataViewSet.as_view(), name='dashboard-data')
]
