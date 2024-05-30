import requests
 
headers = {
    "X-API-Key": "487c5d46-a5d9-33b1-b327-2e1db79c1c68",
    "X-API-Secret": "a28bed270853aa08feeed2aee6af534ef0bf7a024846a6c7c0226c68a192b80b"
}
API_BASE_URL = "https://swissdox.linguistik.uzh.ch/api"
API_URL_DOWNLOAD = f"{API_BASE_URL}/download/301832e9-4e1c-4c6a-963b-ab80a25b9c16__2024_03_08T12_54_02.tsv.xz"
 
r = requests.get(
    API_URL_DOWNLOAD,
    headers=headers
)
if r.status_code == 200:
    print("Size of file: %.2f KB" % (len(r.content)/1024))
    fp = open("data/dataset_84-23_v6.tsv.xz", "wb")
    fp.write(r.content)
    fp.close()
else:
    print(r.text)