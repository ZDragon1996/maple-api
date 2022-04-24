from django.conf import settings
from pathlib import Path
from datetime import datetime, timezone
import csv
import os


class File:
    def __init__(self, django_path, target_ext='.xlsx', media_root=settings.MEDIA_ROOT, **kwargs) -> None:
        # django path
        self.django_path = str(django_path)
        self.media_root = media_root

        # file source
        self.source_file_path = self.get_full_path()
        self._source_path_obj = Path(self.source_file_path)
        self.source_file_info = self._source_path_obj.stat()
        self.source_file_ext = self._source_path_obj.suffix
        self.source_file_name = self._source_path_obj.name
        self.source_file_size = self.get_file_size(self.source_file_info)
        self.source_file_mt_time = self.get_file_mt_time()

        # file target
        self.target_file_ext = target_ext
        self.target_file_path = self.source_file_path.replace(
            self.source_file_ext, self.target_file_ext)
        self.target_file_name = self.get_target_file_name()

        # helper path
        #self._file_root = os.path.dirname(self.get_full_path())
        self._original_file_name = os.path.basename(self.get_full_path())
        self.django_target_path = self.django_path.replace(
            self.source_file_ext, self.target_file_ext)
        self.target_file_media_full_path = os.path.join(
            self.media_root, self.target_file_path)
        self.target_url_path = os.path.join(
            settings.API_MEDIA_ROOT_URL, self.django_target_path)

# ===================================
# Get full path for source file
# ===================================
    def get_full_path(self) -> str:
        if os.name == 'nt':
            return os.path.join(self.media_root, self.django_path).replace('/', '\\')
        return os.path.join(self.media_root, self.django_path)

# ===================================
# Get delimiter from source file
# ===================================
    def get_file_deli(self) -> str:
        """
        Use sniffer function from CSV module to guess delimiter.
        If the given file is empty, it returns ','.
        Skip empty line until it finds a non empty string and try to guess delimiter
        Max loop of 100 lines supposes all first 100 lines are empty, and it returns 'unknown.'
        """
        default_deli = ','
        unknown_deli = 'unknown'
        with open(self.source_file_path, 'rt') as f:
            sniffer = csv.Sniffer()
            lines = f.readlines()
            max_loop = 100
            if not lines:
                return default_deli
            for line in lines:
                if max_loop <= 1:
                    return unknown_deli
                max_loop -= 1
                if line.strip():
                    deli = sniffer.sniff(line).delimiter
                    if deli == 't':
                        return '|'
                    return deli
        return unknown_deli

# ==========================================
# Get delimeter count from source file
# ==========================================
    def get_deli_count(self, line: str, deli: str) -> int:
        return len(line.split(deli)) - 1

# ==========================================
# Validate delimiter count from source file
# ==========================================
    def valid_deli_count(self) -> bool:
        '''
        Take the count of the first delimiter occurrence and then compare it with the rest of the lines.
        Returns True if all lines of delimiter count are matched with the first delimiter occurrence; otherwise, False.
        '''
        expected_count = None
        deli = self.get_file_deli()
        with open(self.source_file_path, 'rt') as f:
            lines = f.readlines()
            for line in lines:
                if line:
                    current_deli_count = self.get_deli_count(line, deli)
                    if expected_count is None:
                        expected_count = current_deli_count
                    if current_deli_count != expected_count:
                        return False
        return True

# ==============================
# Get target file name
# ==============================
    def get_target_file_name(self) -> str:
        file_name = os.path.basename(self.source_file_path)
        return file_name.replace(self.source_file_ext, self.target_file_ext)

# ==============================
# Get source file size
# ==============================
    def get_file_size(self, file_info) -> str:
        '''
        Uses pathlib module to get file size info.
        Append the corresponding unit based on the calculation.
        Use format: 3.1f  EX: 300.0B or 101.2KB
        '''
        file_size = file_info.st_size
        units = ['B', 'KB', 'MB', 'GB', 'TB']
        for u in units:
            if abs(file_size) < 1024:
                return f'{file_size:3.1f}{u}'
            file_size /= 1024

# ==============================
# Get source file mt_time
# ==============================
    def get_file_mt_time(self) -> datetime:
        '''
        Uses pathlib module to get file mt_time info.
        Uses datetime module to get datetime obj from the timestamp
        default: UTC timezone 
        '''
        st_mtime = self.source_file_info.st_mtime
        file_mt_datetime = datetime.fromtimestamp(
            st_mtime, timezone.utc)
        return file_mt_datetime
