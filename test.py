import requests

data_url = "data:text/plain;base64,SGVsbG8gV29ybGQhCg=="

response = requests.get(data_url)

if response.status_code == 200:
    content = response.text
    print(content)
else:
    print("Failed to retrieve data from the URL.")