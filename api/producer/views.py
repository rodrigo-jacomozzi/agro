from django.db.models import Sum, Count
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Producer, Crop
from .serializers import ProducerSerializer


class ProducerViewSet(viewsets.ModelViewSet):
    queryset = Producer.objects.all()
    serializer_class = ProducerSerializer
    allowed_methods = ['get', 'post', 'put', 'delete']


class DashboardDataViewSet(APIView):

    @staticmethod
    def _get_producers_per_state():
        producer_count_by_state = Producer.objects.values('state').annotate(producer_count=Count('state'))

        for item in producer_count_by_state:
            item['count'] = item.pop('producer_count')

        return producer_count_by_state

    @staticmethod
    def _crops_per_type():
        crop_type_counts = Crop.objects.values('type').annotate(type_count=Count('type'))

        for item in crop_type_counts:
            item['count'] = item.pop('type_count')

        return crop_type_counts

    @staticmethod
    def _get_sum(field, model=Producer):
        return model.objects.aggregate(Sum(field))[f'{field}__sum']

    def get(self, _):

        total_producers = Producer.objects.count()
        total_area_sum = self._get_sum('total_area')
        total_crops = Crop.objects.count()

        producers_per_state = self._get_producers_per_state()
        crops_per_type = self._crops_per_type()

        arable_area = self._get_sum('arable_area')
        vegetation_area = self._get_sum('vegetation_area')

        data = {
            'total_producers': total_producers,
            'total_area': total_area_sum,
            'total_crops': total_crops,
            'producers_per_state': producers_per_state,
            'crops_per_type': crops_per_type,
            'area_per_usage': {
                'arable': arable_area,
                'vegetation': vegetation_area,
            }
        }
        return Response(data)
