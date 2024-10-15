import requests
from bs4 import BeautifulSoup

def scrape_cnpj_data(cnpj):
    url = f"http://consulta.sintegra.es.gov.br/resultado?CNPJ={cnpj}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # Exemplo de extração: obter a razão social
    razao_social = soup.find('label', text='Razão Social').find_next_sibling('value').text
    return {"razao_social": razao_social}