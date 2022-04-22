from django.conf import settings
import os
from django.http import FileResponse, Http404
import pandas as pd
import pathlib

# media_root = .....\media
media_root = settings.MEDIA_ROOT


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


def get_full_path(csv_path):
    return os.path.join(media_root, csv_path)


def convert_csv2xlsx(csv_path):
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
    df.to_excel(excel_writer, index=False)
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
