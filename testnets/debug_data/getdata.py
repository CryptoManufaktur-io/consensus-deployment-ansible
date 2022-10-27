from re import S
import requests
import pathlib
import calendar
import time
import os
from ansible.parsing.dataloader import DataLoader
from ansible.inventory.manager import InventoryManager

gmt = time.gmtime()
ts = calendar.timegm(gmt)

dir_path = os.path.dirname(os.path.realpath(__file__))
dir_name = dir_path + "/" + str(ts) + "_after_rejoin"
pathlib.Path(dir_name).mkdir(parents=True, exist_ok=True)

data_loader = DataLoader()
inventory = InventoryManager(loader = data_loader, sources=[inventory_file_name])
hostsList = inventory.get_hosts()
print(hostsList)

# for server in servers:
#   url = "http://" + servers[server] + ":4000/eth/v1/debug/beacon/forkchoice"
#   solditems = requests.get(url)
#   pathlib.Path(dir_name + '/data_' + server + '.json').write_bytes(solditems.content)

