from rest_framework import serializers
from . import models
from image.classes.image import Image


class ImageSerializer(serializers.ModelSerializer):

    def get_processed_image(self, obj):
        print(obj)
        img = Image(obj.image)
        return img.convert_image2sketch()

    processed_image = serializers.SerializerMethodField()

    class Meta:
        model = models.Image
        fields = ['image', 'processed_image']
