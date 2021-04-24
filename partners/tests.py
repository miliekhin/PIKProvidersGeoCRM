from rest_framework.test import APITestCase
from .models import ServedArea, Service, Partner
from django.contrib.gis.geos import Point, Polygon
from django.urls import reverse
from rest_framework import status
import json


class PartnerTests(APITestCase):
    """ Тестирование работы ручки получения поставщика по координатам точки и ID услуги"""
    coords1 = ((37.55350112915039, 55.62382843956678), (37.55581855773926, 55.61587985760705),
               (37.568092346191406, 55.61587985760705), (37.57195472717285, 55.621162936206005),
               (37.566461563110344, 55.62596071175313), (37.55350112915039, 55.62382843956678))
    coords2 = ((37.57401466369629, 55.62373151534754), (37.55959510803223, 55.62130833197216),
               (37.55805015563965, 55.615928329453894), (37.56895065307617, 55.61195343899831),
               (37.57770538330078, 55.61617068778932), (37.57401466369629, 55.62373151534754))
    POLYGON1 = Polygon(coords1)
    POLYGON2 = Polygon(coords2)
    POINT_INSIDE = Point(37.56620407104492, 55.620242083830405)
    POINT_OUTSIDE = Point(37.571868896484375, 55.62528227409462)

    def setUp(self):
        """ Создание поставщиков, услуг, и областей обслуживания"""
        partner1 = Partner.objects.create(id=1, name='Поставщик 1', email='partner1@mail.ru', phone='+74954579826', address='Address 1')
        partner2 = Partner.objects.create(id=2, name='Поставщик 2', email='partner2@mail.ru', phone='+74958792266', address='Address 2')
        service1 = Service.objects.create(id=1, name='Услуга 1', price=111111.11)
        service2 = Service.objects.create(id=2, name='Услуга 2', price=2222.22)
        sa1 = ServedArea.objects.create(id=1, name='Область 1', area=self.POLYGON1, partner=partner1)
        sa2 = ServedArea.objects.create(id=2, name='Область 2', area=self.POLYGON2, partner=partner2)
        sa1.services.add(service1)
        sa2.services.add(service1, service2)

    def test_point_in_area(self):
        """ Точка попадает в один полигон """
        p = Point(37.565860748291016, 55.62445844114975)
        polygon_count = ServedArea.objects.filter(area__contains=p).count()
        self.assertEqual(polygon_count, 1)

    def test_point_in_two_intersected_areas(self):
        """ Точка попадает в два полигона """
        polygon_count = ServedArea.objects.filter(area__contains=self.POINT_INSIDE).count()
        self.assertEqual(polygon_count, 2)

    def test_point_out_of_areas(self):
        """ Точка не попадает в полигоны """
        polygon_count = ServedArea.objects.filter(area__contains=self.POINT_OUTSIDE).count()
        self.assertEqual(polygon_count, 0)

    def test_get_one_partner(self):
        """
        Получение поставщика по координатам точки и ID услуги
        Точка попадает в два полигона, но услуга 2 есть только у одного поставщика
        """
        response = self.client.get(reverse('partners_by_position',
                                           kwargs={
                                               'long': self.POINT_INSIDE.x,
                                               'lat': self.POINT_INSIDE.y,
                                               'service_id': 2}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertJSONEqual(
            """
                [{"id": 2, "name": "Поставщик 2", 
                "area_name": "Область 2", 
                "services": [{"id": 1, "name": "Услуга 1", "price": "111111.11"}, 
                {"id": 2, "name": "Услуга 2", "price": "2222.22"}]}]
            """,
            json.dumps(response.data)
        )

    def test_get_two_partners(self):
        """
        Получение поставщика по координатам точки и ID услуги
        Точка попадает в два полигона, и услуга 1 есть у всех поставщиков (двух)
        """
        response = self.client.get(reverse('partners_by_position',
                                           kwargs={
                                               'long': self.POINT_INSIDE.x,
                                               'lat': self.POINT_INSIDE.y,
                                               'service_id': 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_no_partners(self):
        """
        Получение поставщика по координатам точки и ID услуги
        Точка попадает в два полигона, но услуги 3 нет у поставщиков
        """
        response = self.client.get(reverse('partners_by_position',
                                           kwargs={
                                               'long': self.POINT_INSIDE.x,
                                               'lat': self.POINT_INSIDE.y,
                                               'service_id': 3}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_get_no_partners_out_of_areas(self):
        """
        Получение поставщика по координатам точки и ID услуги
        Точка не попадает в полигоны, но услуга 1 есть у всех поставщиков
        """
        response = self.client.get(reverse('partners_by_position',
                                           kwargs={
                                               'long': self.POINT_OUTSIDE.x,
                                               'lat': self.POINT_OUTSIDE.y,
                                               'service_id': 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
