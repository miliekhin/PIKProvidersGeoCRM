from .views import PartnerViewSet, ServiceViewSet, ServedAreaViewSet
from rest_framework.routers import SimpleRouter
from django.urls import path, register_converter
from .views import PartnersView
from .converters import FloatUrlParameterConverter

router = SimpleRouter()
router.register('partners', PartnerViewSet)
router.register('services', ServiceViewSet)
router.register('areas', ServedAreaViewSet)

register_converter(FloatUrlParameterConverter, 'float')

urlpatterns = [
    path('partners/<float:long>/<float:lat>/<int:service_id>/', PartnersView.as_view(), name='partners_by_position'),
]

urlpatterns += router.urls
