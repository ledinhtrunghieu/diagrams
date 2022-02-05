import requests
from bs4 import BeautifulSoup
import json

URL = "https://www.moderndatastack.xyz/companies/Business-Intelligence-(BI)"
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")

opensource =  soup.find_all(text="Open Source")
print(opensource)