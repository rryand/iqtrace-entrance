import json

import requests

from settings import API_URL

def get(endpoint: str) -> dict:
  print(f"GET {API_URL + endpoint}")
  response = requests.get(API_URL + endpoint)
  print(response.status_code)
  return response.json()

def patch(endpoint: str) -> dict:
  print(f"PATCH {API_URL + endpoint}")

  response = requests.patch(API_URL + endpoint)

  return response.json()

def post(endpoint: str, body: dict) -> dict:
  print(f"POST {API_URL + endpoint}")
  response = requests.post(
    API_URL + endpoint,
    headers={"Content-Type": "application/json; charset=utf-8"},
    json=body
  )
  print(response.status_code)
  print(response.json())
  return response.json()
