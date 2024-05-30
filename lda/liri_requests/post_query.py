import requests
 
headers = {
    "X-API-Key": "487c5d46-a5d9-33b1-b327-2e1db79c1c68",
    "X-API-Secret": "a28bed270853aa08feeed2aee6af534ef0bf7a024846a6c7c0226c68a192b80b"
}
API_BASE_URL = "https://swissdox.linguistik.uzh.ch/api"
API_URL_QUERY = f"{API_BASE_URL}/query"

query_dec = """
    query:
        sources:
            - WEW
            - TA
            - NMZ
            - NZZ
            - BZ
            - BLI
            - BAZ
        dates:
            - from: 1984-01-01
              to: 2023-12-31
        languages:
            - de
        content:
            AND:
                - NOT: Krieg
                - NOT: Kirche
                - NOT: Gottesdienst
                - NOT: Musik
                - NOT: Ukraine
                - NOT: Israel
                - NOT: Fussball*
                - NOT: Eishockey*
                - NOT: Film
                - OR:
                    - Verkehr*
                    - Mobilität*
                    - Fahrzeug*
                - OR:
                    - Velo*
                    - Fahrrad*
                    - SBB
                    - Tram
                    - Eisenbahn*
                    - Fussgägnger
                    - Fluggesellschaft
                    - Postauto
                    - Automobil*
                    - Auto
                    - Swiss
                    - Swissair
                    - Lastwagen
                    - Motorrad
                    - Töff
                    - Flugzeug*
                    - Bus
    result:
        format: TSV
        maxResults: 1000000
        columns:
            - id
            - pubtime
            - medium_code
            - medium_name
            - doctype
            - head
            - subhead
            - content_id
            - content
    version: 1.2
"""

data = {
    "query": query_dec,
    "name": "Verkehrsdokumente 84-23 new 1"
}
 
r = requests.post(
    API_URL_QUERY,
    headers=headers,
    data=data
)
print(r.json()) 