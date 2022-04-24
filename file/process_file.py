from django.conf import settings
import os
from django.http import FileResponse, Http404
import pandas as pd
import pathlib
from datetime import datetime, timezone
import json
import csv
from xlsxwriter.workbook import Workbook
# media_root = .....\media
media_root = settings.MEDIA_ROOT

# ====================
# File Util Secion
# ====================

def _get_file_deli(file_path):
    """
    empty file returns ','
    """
    file_path = str(file_path)
    full_path = get_full_path(file_path)
    with open(full_path, 'rt') as f:
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


def _get_deli_count(line, deli):
    return len(line.split(deli))


def _valid_deli_count(file_path):
    file_path = str(file_path)
    full_path = get_full_path(file_path)
    expected_count = None
    deli = _get_file_deli(file_path)
    with open(full_path, 'rt') as f:
        lines = f.readlines()
        for line in lines:
            current_deli_count = _get_deli_count(line, deli)
            if not expected_count:
                expected_count = current_deli_count
            if current_deli_count != expected_count:
                return False
    return True


def get_full_path(csv_path):
    return os.path.join(media_root, csv_path)


def handle_file_name(file_path, type):
    file_path = str(file_path)
    file_name = os.path.basename(file_path)
    ext = pathlib.Path(file_name).suffix
    return file_name.replace(ext, type)


def handle_file_size(file_path):
    file_path = str(file_path)
    full_path = get_full_path(file_path)
    file_size = pathlib.Path(full_path).stat().st_size
    units = ['B', 'KB', 'MB', 'GB', 'TB']
    for u in units:
        if abs(file_size) < 1024:
            return f'{file_size:3.1f}{u}'
        file_size /= 1024


def handle_file_mt_time(file_path):
    file_path = str(file_path)
    full_path = get_full_path(file_path)
    st_mtime = pathlib.Path(full_path).stat().st_mtime
    file_mt_datetime = datetime.fromtimestamp(
        st_mtime, timezone.utc)
    return file_mt_datetime


# ==============================
# File Convertion Section
# ==============================

def convert_csv2xlsx(file_path):
    deli = _get_file_deli(file_path)
    valid_deli_count = _valid_deli_count(file_path)
    print(deli)
    print(valid_deli_count)
    if deli != 'unknown' and valid_deli_count:
        return convert_csv2xlsx_pd(file_path)
    else:
        return convert_csv2xlsx_xlsxwriter(file_path)


def convert_csv2xlsx_xlsxwriter(csv_path):
    print('converting using xlsxwriter')
    csv_path = str(csv_path)
    csv_file_path = get_full_path(csv_path)
    xlsx_path = csv_path.replace('csv', 'xlsx')
    xlsx_file_path = os.path.join(media_root, xlsx_path)
    with Workbook(xlsx_file_path) as workbook:
        worksheet = workbook.add_worksheet()
        with open(csv_file_path, 'rt') as f:
            csv_reader = csv.reader(f)
            for r, row in enumerate(csv_reader):
                for c, col in enumerate(row):
                    worksheet.write(r, c, col)
    return os.path.join(settings.API_MEDIA_ROOT_URL, xlsx_path)


def convert_csv2xlsx_pd(csv_path):
    csv_path = str(csv_path)
    csv_file_path = get_full_path(csv_path)
    # xlsx path = file\files\...xlsx
    xlsx_path = csv_path.replace('csv', 'xlsx')
    xlsx_file_path = os.path.join(media_root, xlsx_path)

    print(f'file_path: {csv_file_path}')
    print(f'xlsx_path: {xlsx_path}')
    print(f'xlsx_file_path: {xlsx_file_path}')

    df = pd.read_csv(csv_file_path)
    excel_writer = pd.ExcelWriter(xlsx_file_path)
    df.to_excel(excel_writer, index=False, engine='xlsxwriter')
    excel_writer.save()

    return os.path.join(settings.API_MEDIA_ROOT_URL, xlsx_path)




def download_file(path):
    response = FileResponse()

    file_path = os.path.join(settings.MEDIA_ROOT, path)

    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            response = FileResponse(f.read(), content_type='whatever')
            response[
                'Content-Disposition'] = f'attachment; filename={os.path.basename(file_path)}'
            return response
    raise Http404
