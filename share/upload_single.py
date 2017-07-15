from . import helper


def upload_single(file_path, hostname):
    helper.assert_file(file_path)
    host = helper.find_host(file_path, hostname)
    helper.assert_file_size(file_path, host)
    link = host.upload(file_path)
    print("File link:", link)
