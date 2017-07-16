import os.path
from math import ceil
from requests import post

SIZE_LIMIT = 1 # MB
url = "https://api.github.com/gists"
headers = {
    "User-Agent": "tallpants"
}


def _add_file_to_payload(file_path, payload):
    with open(file_path, "r") as f:
        file_contents = f.read()

    file_name = os.path.basename(file_path)

    payload["files"][file_name] = {
        "content": file_contents
    }

def upload(file_path):
    payload = {
        "public": True,
        "files": {}
    }
    _add_file_to_payload(file_path, payload)
    response = post(url, headers=headers, json=payload)
    return response.json()["html_url"]


def upload_multiple(files_path):
    for file_path in files_path:
        _add_file_to_payload(file_path, payload)

    response = post(url, headers=headers, json=payload)
    return response.json()["html_url"]


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
    """Test if the list of files is smaller than the limit size for the host.

    Args:
        path ([str]): the list of files path

    Raises:
        SystemExit: a file is larger than the limit
    """
    for path in paths:
        assert_file_size(path)