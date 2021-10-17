import requests

from settings import API_URL

def get(endpoint: str) -> dict:
  print(f"GET {API_URL + endpoint}")
  response = requests.get(API_URL + endpoint)
  return response.json()
