import cloudscraper,lxml
from bs4 import BeautifulSoup


def get_price():
   link ='https://opensea.io/collection/crypto-unicorns-market?search[sortAscending]=true&search[sortBy]=UNIT_PRICE&search[stringTraits][0][name]=Game%20Lock&search[stringTraits][0][values][0]=Unlocked'

   scraper = cloudscraper.create_scraper(browser={'browser': 'firefox','platform': 'windows','mobile': False})

   html = scraper.get(link).text

   soup = BeautifulSoup(html, 'lxml')
   mydivs = soup.find("main",id = 'main')
   mydiv = mydivs.find("div", {"class": "sc-6990c3a-0 kezsvr Price--amount"}).text
   return float(mydiv)



def main():
  get_price()


if __name__ == "__main__":
   main()