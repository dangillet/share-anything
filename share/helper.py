import os.path
import sys
from math import ceil

from . import hosts, extensions

def assert_file(path):
    """Check for the existence of the file in `path`.

    If not it prints an error message and quits the program.

    Args:
        path (str): the filename path.

    Returns:
        None

    Raises:
        SystemExit: `path` does not exists.
    """
    if not os.path.isfile(path):
        print("The file {} cannot be found".format(path))
        sys.exit(1)

def find_host(filepath, hostname=None):
    """Find the correct host depending on the hostname or file extension.

    If `hostname` is given, it is used in preference to the file extension.

    Args:
        filepath (str): the file path
        hostname (str): a host among imgur, gist and anonfile (optional)

    Returns:
        host (module): the module with the functions to upload files.
    """
    if hostname:
        if hostname == "imgur":
            return hosts.imgur
        elif hostname == "gist":
            return hosts.gist
        elif hostname == "anonfile":
            return hosts.anonfile
    
    _, file_extension = os.path.splitext(filepath)
    if file_extension in extensions.imgur:
        return hosts.imgur
    elif file_extension in extensions.gist:
        return hosts.gist
    else:
        return hosts.anonfile

def assert_file_size(path, host):
    """Test if the file is smaller than the limit size for the host.

    Args:
        path (str): the file path
        host (module): the module for the host
    """
    size_mb = ceil(os.path.getsize(path) / 1000000)
    if size_mb > host.SIZE_LIMIT:
        print("File is too large ({}MB limit)".format(host.SIZE_LIMIT))
        exit(1)
