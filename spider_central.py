# Importando bibliotecas
from urllib.request import Request, urlopen, urlretrieve
from urllib.error import URLError, HTTPError
from bs4 import BeautifulSoup
import pandas as pd

# Testando Acesso a URL
url = 'https://www.microsoft.com/pt-br/store/deals/games/xbox'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}

try:
    req = Request(url, headers = headers)
    response = urlopen(req)

except HTTPError as e:
    print(e.status, e.reason)

except URLError as e:
    print(e.reason)

# Declarando variável cards
games = []
game = {}

# Obtendo o HTML
response = urlopen(req)
html = response.read().decode('utf-8')
soup = BeautifulSoup(html, 'html.parser')
pages_results = int(soup.find('p', class_= 'c-paragraph-3').getText().split()[-2])
pages = round((pages_results / 90))

# Iterando por Todas as Páginas
for i in range(0, pages*90, 90):
  # Obtendo o HTML
  response = urlopen('https://www.microsoft.com/pt-br/store/deals/games/xbox?s=store&skipitems=' + str(i))
  html = response.read().decode('utf-8')
  soup = BeautifulSoup(html, 'html.parser')
  # Obtendo as TAGs de interesse
  products = soup.find('div', {'id': 'productPlacementList'}).findAll('div', {'class': 'm-channel-placement-item'})

  # Coletando as informações dos Cards
  for product in products:
    game = {}
    # Obtendo a Título
    game['Título'] = product.find('h3', class_='c-subheading-6').getText()
    # Obtendo o Preço
    game['Valor'] = product.find('span', itemprop='price').getText().replace('R$', 'R$ ')
    # Obtendo o Link
    game['Link'] = 'www.microsoft.com' + product.find('a').get('href')
    # Adicionando resultado a lista cards
    games.append(game)

# Criando um DataFrame com os resultados
dataset = pd.DataFrame(games)
dataset.to_excel(r'C:\\Users\\paulo\\Downloads\\games.xlsx', index = False, encoding = 'utf-8')

dataset