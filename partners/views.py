from django.contrib.gis.geos import Point
from rest_framework.viewsets import ModelViewSet
from .serializers import PartnerSerializer, PartnerByPointSerializer, ServiceSerializer, ServedAreaSerializer
from .models import Partner, Service, ServedArea
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from django.db import connection
from django.core.cache import cache


class PartnerViewSet(ModelViewSet):
    """
    list: Список всех поставщиков
    create: Создание поставщика
    retrieve: Получение поставщика по ID
    update: Обновление всех данных поставщика
    partial_update: Частичное обновление данных поставщика
    delete: Удаление поставщика
    """

    serializer_class = PartnerSerializer
    queryset = Partner.objects.all()


class ServiceViewSet(ModelViewSet):
    """
    list: Список всех услуг
    create: Создание услуги
    retrieve: Получение услуги по ID
    update: Обновление всех данных услуги
    partial_update: Частичное обновление данных услуги
    delete: Удаление услуги
    """

    serializer_class = ServiceSerializer
    queryset = Service.objects.all()


class ServedAreaViewSet(ModelViewSet):
    """
    list: Список всех областей
    create: Создание области
    retrieve: Получение области по ID
    update: Обновление всех данных области
    partial_update: Частичное обновление данных области
    delete: Удаление области
    """

    serializer_class = ServedAreaSerializer
    queryset = ServedArea.objects.all()


class PartnersView(ListAPIView):
    """Выборка поставщиков по долготе, широте, и номеру услуги"""

    def list(self, request, long, lat, service_id):
        cache_key = request.get_full_path()
        response = cache.get(cache_key)
        if response:
            return Response(response)
        pnt = Point(long, lat)
        queryset = ServedArea.objects.filter(area__contains=pnt, services=service_id)\
            .select_related('partner')\
            .prefetch_related('services')
        serializer = PartnerByPointSerializer(queryset, many=True)
        data = serializer.data
        print('Queries:', len(connection.queries))
        cache.set(cache_key, data, 16)
        return Response(data)
