from rest_framework import serializers
from .models import File
from .classes.csvfile import CSVFile


class FileSerializer(serializers.ModelSerializer):
    # class attribute
    csv_file = None
    target_ext = '.xlsx'

    def get_target_name(self, obj):
        global csv_file
        csv_file = CSVFile(obj.file, target_ext=self.target_ext)
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


class CSV2XLSXSerializer(FileSerializer):
    pass


class CSV2TXTSerializer(FileSerializer):
    target_ext = '.txt'

    def get_converted_file(self, obj):
        return csv_file.convert_csv2txt()


class XLSX2CSVSerializer(FileSerializer):
    target_ext = '.csv'

    def get_converted_file(self, obj):
        return csv_file.convert_xlsx_or_xls2csv()


class XLS2XLSXSerializer(FileSerializer):
    target_ext = '.xlsx'

    def get_converted_file(self, obj):
        return csv_file.convert_xls2xlsx()


class TXT2CSVSerializer(FileSerializer):
    target_ext = '.csv'

    def get_converted_file(self, obj):
        return csv_file.convert_txt2csv()


class TXT2XLSXSerializer(FileSerializer):
    target_ext = '.xlsx'

    def get_converted_file(self, obj):
        return csv_file.convert_txt2xlsx()
