from . import helper 
import sys

def upload_multiple(file_paths, hostname):
    file_hosts = []
    for file_path in file_paths:
        helper.assert_file(file_path)
        host = helper.find_host(file_path, hostname)
        file_hosts.append(host)

    if len(set(file_hosts)) != 1:
        print("Cannot upload files to different hosts at the same time.")
        sys.exit(1)

    host.assert_files_size(file_paths)
    link = host.upload_multiple(file_paths)
    print("Files link:", link)
