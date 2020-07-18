# Import libs
from urllib.request import Request, urlopen, urlretrieve
from urllib.error import URLError, HTTPError
from bs4 import BeautifulSoup
import pandas as pd

# Test URL access
url = 'https://www.microsoft.com/pt-br/store/deals/games/xbox'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}

try:
    req = Request(url, headers = headers)
    response = urlopen(req)

except HTTPError as e:
    print(e.status, e.reason)

except URLError as e:
    print(e.reason)

# Create variables
games = []
game = {}

# Get HTML
response = urlopen(req)
html = response.read().decode('utf-8')
soup = BeautifulSoup(html, 'html.parser')

# Identify page total
pages_results = int(soup.find('p', class_= 'c-paragraph-3').getText().split()[-2])
pages = round((pages_results / 90))

# Iterate through all pages
for i in range(0, pages*90, 90):
  # Get HTML and apply page number
  response = urlopen('https://www.microsoft.com/pt-br/store/deals/games/xbox?s=store&skipitems=' + str(i))
  html = response.read().decode('utf-8')
  soup = BeautifulSoup(html, 'html.parser')
  # Get desired objects
  products = soup.find('div', {'id': 'productPlacementList'}).findAll('div', {'class': 'm-channel-placement-item'})

  # Get desired information
  for product in products:
    game = {}
    # Get the title
    game['Title'] = product.find('h3', class_='c-subheading-6').getText()
    # Get the price
    game['Value'] = product.find('span', itemprop='price').getText().replace('R$', 'R$ ')
    # Get the website link
    game['Link'] = 'www.microsoft.com' + product.find('a').get('href')
    # Add results to a list
    games.append(game)

# Create a DataFrame
dataset = pd.DataFrame(games)
# Export to Excel
dataset.to_excel(r'C:\\Users\\games.xlsx', index = False, encoding = 'utf-8')

dataset
