import requests
 
headers = {
    "X-API-Key": "487c5d46-a5d9-33b1-b327-2e1db79c1c68",
    "X-API-Secret": "a28bed270853aa08feeed2aee6af534ef0bf7a024846a6c7c0226c68a192b80b"
}
API_BASE_URL = "https://swissdox.linguistik.uzh.ch/api"
API_URL_STATUS = f"{API_BASE_URL}/status/301832e9-4e1c-4c6a-963b-ab80a25b9c16"
 
r = requests.get(
    API_URL_STATUS,
    headers=headers
)
print(r.json())