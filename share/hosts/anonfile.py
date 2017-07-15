from requests import post

url = "https://anonfile.com/api/upload"
SIZE_LIMIT = 1024 # MB

def upload(file_name, file_path):
    payload = {
        "file": open(file_path, "rb")
    }

    response = post(url, files=payload)
    try:
        print(response.json()["data"]["file"]["url"]["short"])
    except Exception as e:
        print("Upload to anonfile failed")
        print(e)
        exit(1)
