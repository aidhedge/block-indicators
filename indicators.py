from bs4 import BeautifulSoup
from ah_requests import AhRequest
from logger import Logger

LOG = Logger()

requests = AhRequest()


def interest_rate(_country=None):
    res = requests.get('https://tradingeconomics.com/country-list/interest-rate')
    soup = BeautifulSoup(res.text, "lxml")
    data = []
    for row in soup.findAll(True, {'class':['datatable-row', 'datatable-row-alternating']}):
        country = None
        interest = None
        for t in row.findAll('td')[0]:
            country = t.string.strip()
        for t in row.findAll('td')[1]:
            interest = t.string.strip()
        try:
            interest = float(interest)
        except Exception as e:
            LOG.console(e)
            interest = None
            
        data.append(dict(country=country, interest=interest))
    if country:
        return [d for d in data if d['country'].lower() == _country.lower()][0]
    else:
        return data


def inflation(_country=None):
    res = requests.get('https://tradingeconomics.com/country-list/inflation-rate')
    soup = BeautifulSoup(res.text, "lxml")
    data = []
    for row in soup.findAll(True, {'class':['datatable-row', 'datatable-row-alternating']}):
        country = None
        inflation = None
        for t in row.findAll('td')[0]:
            country = t.string.strip()
        for t in row.findAll('td')[1]:
            inflation = t.string.strip()
        try:
            inflation = float(inflation)
        except Exception as e:
            LOG.console(e)
            inflation = None
            
        data.append(dict(country=country, inflation=inflation))
    LOG.console(data)
    if country:
        return [d for d in data if d['country'].lower() == _country.lower()][0]
    else:
        return data

