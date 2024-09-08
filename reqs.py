import requests

id = input("ID ngrok: ")
url = f"{id}-3-135-152-169.ngrok-free.app"

txt2img_url = url + "/sdapi/v1/txt2img"

headers = {"ngrok-skip-browser-warning": "true"}

request = requests.get(url, headers=headers)
