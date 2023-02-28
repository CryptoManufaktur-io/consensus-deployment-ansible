from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import sys, json

def getSoup(url):
  req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
  html = urlopen(req).read().decode("utf-8")
  soup = BeautifulSoup(html, features="html.parser")

  return soup

def getDetails(base_url, transaction_hash):
  soup = getSoup(base_url + "/tx/" + transaction_hash)
  transaction_hash = soup.find(id="spanTxHash").text
  #contract_address = soup.find(id="contractCopy").text
  contract_address = soup.find_all("a", href=lambda href: href and "/address/" in href)[1].text
  block_number = soup.find_all("a", href=lambda href: href and "/block/" in href)[0].text

  soup = getSoup(base_url + "/block/" + block_number)
  block_hash = soup.find(id="collapseContent").find_all("div")[0].find_all("div")[1].text.replace("\n", "")

  return {
    "transaction_hash": transaction_hash, 
    "contract_address": contract_address, 
    "block_number": block_number,
    "block_hash": block_hash
  }

n = len(sys.argv)
if(n != 3):
  print("Script expects 2 arguments only: Example script.py https://goerli.etherscan.io TRANSACTION_HASH")
else:
    print(json.dumps(getDetails(sys.argv[1], sys.argv[2])))
