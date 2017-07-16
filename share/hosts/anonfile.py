import os.path
from math import ceil
import os
from zipfile import ZipFile
from requests import post

url = "https://anonfile.com/api/upload"
SIZE_LIMIT = 1024 # MB


def upload(file_path):
    payload = {
        "file": open(file_path, "rb")
    }

    response = post(url, files=payload)
    return response.json()["data"]["file"]["url"]["short"]


def upload_multiple(files_path):
    zip_name = os.getcwd() + ".zip"
    with ZipFile(zip_name, "w") as zip:
        for file_path in files_path:
            zip.write(file_path)

    link = upload(zip_name)
    os.remove(zip_name)
    return link


def assert_file_size(path):
    """Test if the file is smaller than the limit size for the host.

    Args:
        path (str): the file path

    Raises:
        SystemExit: the file is larger than the limit
    """
    size_mb = ceil(os.path.getsize(path) / 1000000)
    if size_mb > SIZE_LIMIT:
        print("File is too large ({}MB limit)".format(SIZE_LIMIT))
        exit(1)


def assert_files_size(paths):
    """Test if the zipped files is smaller than the limit size for the host.

    Args:
        path ([str]): the list of files path

    Raises:
        SystemExit: a file is larger than the limit
    """
    # TODO: Using a class, we could avoid creating twice the ZIP file.
    zip_name = os.getcwd() + ".zip"
    with ZipFile(zip_name, "w") as zip:
        for path in paths:
            zip.write(path)

    try:
        assert_file_size(zip_name)
    finally:
        os.remove(zip_name)