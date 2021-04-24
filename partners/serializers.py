from rest_framework_gis.serializers import GeoFeatureModelSerializer
from rest_framework import serializers
from .models import Partner, ServedArea, Service


class ServedAreaSerializer(GeoFeatureModelSerializer):
    """Сериализация обслуживаемой области"""

    class Meta:
        model = ServedArea
        geo_field = "area"

        fields = ['partner', 'name', 'services']


class PartnerSerializer(serializers.ModelSerializer):
    """Сериалайзер получения партнера"""

    class Meta:
        model = Partner
        fields = '__all__'


class ServiceSerializer(serializers.ModelSerializer):
    """Сериалайзер получения услуги"""

    class Meta:
        model = Service
        fields = '__all__'


class PartnerByPointSerializer(serializers.ModelSerializer):
    """Сериалайзер получения партнера по точке на карте"""
    name = serializers.SerializerMethodField()
    id = serializers.SerializerMethodField()
    services = ServiceSerializer(many=True)
    area_name = serializers.CharField(source='name')

    class Meta:
        model = ServedArea
        fields = ['id', 'name', 'area_name', 'services']

    def get_name(self, obj):
        return obj.partner.name

    def get_id(self, obj):
        return obj.partner.id
