import pandas as pd
import requests
from bs4 import BeautifulSoup

# df = pd.read_csv('data/data_blog.csv')

res = requests.get('https://understat.com/league/La_liga/2017/')

soup = BeautifulSoup(res.content)
# print(soup.prettify())

table = soup.findAll('script')
table
