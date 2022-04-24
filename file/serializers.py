from rest_framework import serializers
from .models import File
from .classes.csvfile import CSVFile


class FileSerializer(serializers.ModelSerializer):
    # class attribute
    csv_file = None

    def get_target_name(self, obj):
        global csv_file
        csv_file = CSVFile(obj.file, target_ext='.xlsx')
        return csv_file.target_file_name

    def get_file_size(self, obj):
        return csv_file.source_file_size

    def get_file_modified_time(self, obj):
        return csv_file.source_file_mt_time

    def get_converted_file(self, obj):
        return csv_file.convert_csv2xlsx()

    target_name = serializers.SerializerMethodField()
    file_size = serializers.SerializerMethodField()
    file_modified_time = serializers.SerializerMethodField()
    converted_file = serializers.SerializerMethodField()

    class Meta:
        model = File
        fields = ['target_name', 'file_size', 'file',
                  'converted_file', 'file_modified_time']


class CSV2TXTSerializer(FileSerializer):
    def get_converted_file(self, obj):
        return csv_file.convert_csv2txt()

    def get_target_name(self, obj):
        global csv_file

        csv_file = CSVFile(obj.file, target_ext='.txt')
        return csv_file.target_file_name
