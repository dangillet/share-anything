import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pytest
import share.hosts as hosts
from share.helper import find_host, assert_file, assert_file_size

def test_assert_file_false(capsys):
    path = "dummy"
    with pytest.raises(SystemExit):
        assert_file(path)
    out, err = capsys.readouterr()
    assert "The file dummy cannot be found" in out 

def test_assert_file_true():
    path = "../samples/image.jpg"
    output = assert_file(path)
    assert output is None

@pytest.mark.parametrize("hostname, module_host", [
    ("gist", hosts.gist),
    ("anonfile", hosts.anonfile),
    ("imgur", hosts.imgur)])
def test_find_host_with_hostname(hostname, module_host):
    host = find_host("whatever", hostname)
    assert host == module_host

@pytest.mark.parametrize("path, module_host", [
    ("image.jpg", hosts.imgur),
    ("code.cpp", hosts.gist),
    ("other.zip", hosts.anonfile)])
def test_find_host_with_file_extension(path, module_host):
    host = find_host(path)
    assert host == module_host

@pytest.fixture
def dummy_file(request, tmpdir):
    "Make a Dummy file of given size + 1."
    name, size = request.param
    path = tmpdir.mkdir("Dummy_files").join(name)
    with open(str(path), "wb") as f:
        f.seek(size)
        f.write(b"\0")
    return path

@pytest.mark.parametrize("dummy_file, module", [
    (("image.jpg", 1000000 * 10), hosts.imgur),
    (("code.h", 1000000), hosts.gist),
    (("big.zip", 1000000 * 1024), hosts.anonfile),
    ], ids= ["Imgur", "Gist", "Anonfile"], indirect=["dummy_file"])
def test_assert_file_size(dummy_file, module):
    with pytest.raises(SystemExit):
        assert_file_size(str(dummy_file), module)
