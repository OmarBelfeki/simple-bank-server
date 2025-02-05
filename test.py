import requests
from pprint import pprint


url = "http://127.0.0.1:8000/userbalance?token=bar1233"
print(requests.get(url).json())
