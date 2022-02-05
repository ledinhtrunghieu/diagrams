import requests
from bs4 import BeautifulSoup
import json

URL = "https://www.moderndatastack.xyz/companies/Business-Intelligence-(BI)"
page = requests.get(URL)

print(page.text)