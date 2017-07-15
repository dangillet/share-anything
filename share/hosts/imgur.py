from collections import namedtuple
from requests import post, get

SIZE_LIMIT = 10 # MB
client_id = "9c65f969001905d"

Album = namedtuple("Album", "id deletehash")

def upload(file_path, album=None):
    """Upload an image to imgur

    Args:
        file_path (str): the file path to be uploaded
        album (Album): the album to use for uploading (optional)

    Returns:
        link (str): image link url
    """
    url = "https://api.imgur.com/3/image"
    file = {"image": open(file_path, "rb")}
    headers = {"authorization": "Client-ID {0}".format(client_id)}
    
    payload = {"album": album.deletehash} if album else ""

    response = post(url, headers=headers, files=file, data=payload)
    # Need to check for proper response code
    json_data = response.json()["data"]

    link = json_data["link"]
    return link


def create_album():
    """Create an album on imgur.

    Returns:
        album (Album): The Album data
    """
    url = "https://api.imgur.com/3/album"
    headers = {
        "authorization": "Client-ID {0}".format(client_id)
    }

    response = post(url, headers=headers)

    album = Album(**response.json()["data"])
    return album


def get_album_link(album):
    """Return the url to the album

    Args:
        album (Album): the album

    Returns:
        url (str): The album url link
    """
    url = "https://api.imgur.com/3/album/" + album.id
    headers = {
        "authorization": "Client-ID {0}".format(client_id)
    }
    response = get(url, headers=headers)
    link = response.json()["data"]["link"]
    return link


def upload_multiple(file_paths):
    """Create an album and upload all the images into it.

    Args:
        files ([str]): the list of file image paths to be uploaded.

    Returns:
        url (str): The album url link
    """
    album = create_album()
    for file_path in file_paths:
        upload(file_path, album=album)
    return get_album_link(album)

