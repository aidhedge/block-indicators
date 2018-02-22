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
            
        data.append(dict(country=country, rate=interest))
    if _country:
        try:
            _country = [x.lower() for x in _country]
            return [d for d in data if d['country'].lower() in _country][0]
        except:
            return None
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
            
        data.append(dict(country=country, rate=inflation))
    if _country:
        try:
            _country = [x.lower() for x in _country]
            return [d for d in data if d['country'].lower() in _country][0]
        except:
            return None
    else:
        return data


