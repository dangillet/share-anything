import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pytest
import unittest.mock as mock

from share.hosts.imgur import upload, Album

@mock.patch("share.hosts.imgur.post", spec=True, spec_set=True)
@mock.patch("share.hosts.imgur.open", create=True, new_callable=mock.mock_open)
def test_upload_image(mock_open, mock_post):
    mock_response = mock.Mock()
    expected_dict = {
        "data": {
            "link": "Link from imgur"
        }
    }
    mock_response.json.return_value = expected_dict
    mock_post.return_value = mock_response

    link = upload("mock_image.jpg")

    url = "https://api.imgur.com/3/image"
    headers = {"authorization": "Client-ID 9c65f969001905d"}

    mock_post.assert_called_once_with(url, 
                                      files={"image": mock_open.return_value},
                                      headers=headers,
                                      data="")

    assert link == "Link from imgur"
    assert mock_response.json.call_count == 1


@mock.patch("share.hosts.imgur.post", spec=True, spec_set=True)
@mock.patch("builtins.open", new_callable=mock.mock_open)
def test_upload_image_in_album(mock_open, mock_post):
    mock_response = mock.Mock()
    expected_dict = {
        "data": {
            "link": "Link from imgur"
        }
    }
    mock_response.json.return_value = expected_dict
    mock_post.return_value = mock_response

    album = Album(id=10, deletehash=20)
    link = upload("mock_image.jpg", album=album)

    url = "https://api.imgur.com/3/image"
    headers = {"authorization": "Client-ID 9c65f969001905d"}
    payload = {"album": album.deletehash}

    mock_post.assert_called_once_with(url, 
                                      files={"image": mock_open.return_value},
                                      headers=headers,
                                      data=payload)

    assert link == "Link from imgur"
    assert mock_response.json.call_count == 1