from django.contrib.gis.db import models


class Service(models.Model):
    """ Услуга """
    name = models.CharField(max_length=128, null=False, help_text='Наименование услуги')
    price = models.DecimalField(null=False, decimal_places=2, max_digits=10, help_text='Цена за единицу услуги')


class Partner(models.Model):
    """ Поставщик """
    name = models.CharField(max_length=128, null=False, help_text='Название организации')
    email = models.EmailField(help_text='Электронная почта')
    phone = models.CharField(max_length=32, null=False, help_text='Телефонный номер')
    address = models.CharField(max_length=128, null=False, help_text='Адрес центрального офиса')


class ServedArea(models.Model):
    """ Область обслуживания """

    name = models.CharField(max_length=128, null=False, help_text='Наименование области')
    partner = models.ForeignKey(Partner, related_name="served_area", on_delete=models.CASCADE, help_text='ID поставщика')
    services = models.ManyToManyField(Service, help_text='Массив ID услуг')
    area = models.PolygonField(help_text='Координаты полигона в формате GeoJSON')
    # spatial_index Defaults to True. Using a variant of the R-Tree
