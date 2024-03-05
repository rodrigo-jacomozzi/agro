from django.db import transaction
from rest_framework import serializers

from producer.models import Producer, Crop
from utils.choices import CROPS
from pycpfcnpj import cpfcnpj

class CropSerializer(serializers.ModelSerializer):

    type = serializers.ChoiceField(choices=CROPS)
    label = serializers.SerializerMethodField()

    def validate(self, attrs):
        return attrs

    def get_label(self, instance):
        return instance.get_type_display()

    class Meta:
        model = Crop
        fields = ['id', 'producer', 'type', 'label']
        read_only_fields = ['id', 'producer', 'label']

class ProducerSerializer(serializers.ModelSerializer):

    crops = CropSerializer(many=True, allow_null=False)

    class Meta:
        model = Producer
        fields = [
            'id',
            'url',
            'register_number',
            'name',
            'farm_name',
            'city',
            'state',
            'total_area',
            'arable_area',
            'vegetation_area',
            'crops',
        ]
        read_only_fields = ['id', 'url']

    @staticmethod
    def _greater_than_zero(val):
        return val > 0

    def validate_register_number(self, value):

        if not cpfcnpj.validate(value):
            raise serializers.ValidationError('Invalid CPF/CNPJ number.')

        return value


    def validate_total_area(self, value):
        if not self._greater_than_zero(value):
            raise serializers.ValidationError('Value must be greater than zero.')

        return value

    def validate_arable_area(self, value):
        if not self._greater_than_zero(value):
            raise serializers.ValidationError('Value must be greater than zero.')

        return value

    def validate_vegetation_area(self, value):
        if not self._greater_than_zero(value):
            raise serializers.ValidationError('Value must be greater than zero.')

        return value

    def validate_crops(self, value):
        if not value:
            raise serializers.ValidationError('At least one crop must be provided.')

        return value

    def validate(self, attrs):

        if (
            attrs.get('arable_area') + attrs.get('vegetation_area') > attrs.get('total_area')
        ):
            raise serializers.ValidationError(
                'Área de vegetação somada a área agriculturável não pode ser maior que a área total.'
            )


        return attrs

    def create(self, validated_data):
        crops_list = validated_data.pop('crops')

        with transaction.atomic():
            producer = super(ProducerSerializer, self).create(validated_data)

            new_crops = []

            for crops in crops_list:
                crops['producer'] = producer
                serializer = CropSerializer(data=crops)
                if serializer.is_valid(raise_exception=True):
                    new_crops.append(Crop(**crops))

            Crop.objects.bulk_create(new_crops)

        return producer

    def update(self, instance, validated_data):
        crops_list = validated_data.pop('crops')

        with transaction.atomic():
            instance = super(ProducerSerializer, self).update(instance, validated_data)

            Crop.objects.filter(producer=instance).delete()

            new_crops = []

            for crops in crops_list:
                crops['producer'] = instance
                serializer = CropSerializer(data=crops)
                if serializer.is_valid(raise_exception=True):
                    new_crops.append(Crop(**crops))

            Crop.objects.bulk_create(new_crops)

        return instance
