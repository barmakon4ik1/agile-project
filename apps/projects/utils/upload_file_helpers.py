import os
from pathlib import Path

ALLOWED_EXTENSIONS = ['.csv', '.doc', '.pdf', '.xlsx', '.py']


def check_extension(filename):
    extension = Path(filename).suffix

    if extension not in ALLOWED_EXTENSIONS:
        return False

    return True


def check_file_size(file, required_size=2):
    file_size = file.size / (1024 * 1024)

    if file_size > required_size:
        return False

    return True


def create_file_path(file_name):
    new_file_name, file_ext = file_name.split('.')

    file_path = "documents/{}.{}".format(
        new_file_name,
        file_ext
    )

    return file_path


def save_file(file_path, file_content):
    os.makedirs(os.path.dirname('documents/'), exist_ok=True)

    with open(file_path, 'wb') as f:
        for chunk in file_content.chunks():
            f.write(chunk)

    return file_path


def delete_file(file_path):
   os.remove(os.path.realpath(file_path))
