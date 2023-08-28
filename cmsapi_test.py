import requests

headers = {
    'Authorization': "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY4Nzk0MzQwMSwianRpIjoiNTJlODkwYTktMzAzYS00ZTdhLWFlZTAtOGE0YzY1YjdlMTIyIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IlIzNHBUYXUzSDVtUE1MN2VhMmoyVGMiLCJuYmYiOjE2ODc5NDM0MDEsImV4cCI6MTY4Nzk0NDMwMX0.eFf8QJcA2gSJ8U0nSYRapsYjcmjD9K2KiDPzE4aW6qI"
}
resp = requests.get('http://127.0.0.1:5000/cmsapi',headers=headers)
print(resp.text)