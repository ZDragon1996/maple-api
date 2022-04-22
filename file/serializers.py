from pyexpat import model
from rest_framework import serializers
from .models import File
from .process_file import convert_csv2xlsx, handle_file_name, handle_file_size


class FileSerializer(serializers.ModelSerializer):
    def get_converted_file(self, file):
        return convert_csv2xlsx(file.file)

    def get_file_name(self, file):
        return handle_file_name(file.file, '.xlsx')

    def get_file_size(self, file):
        return handle_file_size(file.file)

    converted_file = serializers.SerializerMethodField()
    file_name = serializers.SerializerMethodField()
    file_size = serializers.SerializerMethodField()

    class Meta:
        model = File
        fields = ['file_name', 'file_size', 'file', 'converted_file']
