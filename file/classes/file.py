from django.conf import settings
from pathlib import Path
from datetime import datetime, timezone
import csv
import os


class File:
    def __init__(self, django_path) -> None:
        self.django_path = str(django_path)
        self.media_root = settings.MEDIA_ROOT
        self.full_path = self.get_full_path()
        self.file_info = Path(self.full_path).stat()
        self.file_name = os.path.basename(self.full_path)
        self.file_size = self.handle_file_size()
        self.file_mt_time = self.handle_file_mt_time()
        self.ext = Path(self.file_name).suffix

        # helper
        self._file_root = os.path.dirname(self.get_full_path())
        self._original_file_name = os.path.basename(self.get_full_path())

    def get_full_path(self) -> str:
        return os.path.join(self.media_root, self.django_path)

    def get_file_deli(self):
        """
        empty file returns ','
        """

        with open(self.full_path, 'rt') as f:
            sniffer = csv.Sniffer()
            lines = f.readlines()
            max_loop = 100
            if not lines:
                return ','
            for line in lines:
                if max_loop <= 1:
                    return 'unknown'
                max_loop -= 1
                if line.strip():
                    deli = sniffer.sniff(line).delimiter
                    return deli

    def get_deli_count(self, line, deli):
        return len(line.split(deli))

    def valid_deli_count(self):
        expected_count = None
        deli = self.get_file_deli()
        with open(self.full_path, 'rt') as f:
            lines = f.readlines()
            for line in lines:
                current_deli_count = self.get_deli_count(line, deli)
                if not expected_count:
                    expected_count = current_deli_count
                if current_deli_count != expected_count:
                    return False
        return True

    def handle_file_name(self, type):
        return self.file_name.replace(self.ext, type)

    def handle_file_size(self):
        file_size = self.file_info.st_size
        units = ['B', 'KB', 'MB', 'GB', 'TB']
        for u in units:
            if abs(file_size) < 1024:
                return f'{file_size:3.1f}{u}'
            file_size /= 1024

    def handle_file_mt_time(self):
        st_mtime = self.file_info.st_mtime
        file_mt_datetime = datetime.fromtimestamp(
            st_mtime, timezone.utc)
        return file_mt_datetime
